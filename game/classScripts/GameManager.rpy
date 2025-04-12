init python:
    class GameManager:
        def __init__(self, moves, target_score, level, sublevel):
            self.score = 0
            self.moves = moves
            self.base_points = 5
            self.target_score = target_score
            self.level = level        # current level (1 through 4)
            self.sublevel = sublevel  # current sublevel (starting at 1)
            self.initializing = True  # flag to indicate start-up state
            self.forced_compression_used = False

        def advance_sublevel(self):
            """
            Advances to the next sublevel using a naming convention. If the current
            sublevel is the final one in the current level, mark the sublevel complete
            (and unlock the next level, if applicable) and return to level selection.
            """
            # Determine max sublevels and label prefix by level.
            if self.level == 1:
                max_sub = 4
                label_prefix = "hut_sublevel_"
            elif self.level == 2:
                max_sub = 5
                label_prefix = "house_sublevel_"
            elif self.level == 3:
                max_sub = 8
                label_prefix = "mansion_sublevel_"
            elif self.level == 4:
                max_sub = 12
                label_prefix = "apartment_sublevel_"
            else:
                renpy.jump("level_selection")
                return

            if self.sublevel < max_sub:
                self.sublevel += 1
                new_label = label_prefix + str(self.sublevel)
            else:
                # Last sublevel of the level has been completed.
                complete_sublevel(self.level, self.sublevel)
                new_label = "level_selection"
            renpy.jump(new_label)

        def retry_sublevel(self):
            renpy.jump("start_game")
        
        def find_match(self, mouse_event):
            # Do nothing if we are still in the initial state.
            while True:
                if self.initializing:
                    return
                processed = set()
                all_matches = []

                # Loop over every icon in the grid.
                for icon in grid.icons:
                    # Skip if there’s no icon or it was already processed.
                    if icon is None or icon.index in processed:
                        continue

                    # Start the cluster with the current icon.
                    matches = [icon]
                    idx = 0
                    while idx < len(matches):
                        current = matches[idx]
                        # Check the four adjacent directions.
                        right_index = current.index + 1
                        bot_index   = current.index + grid.icons_per_row
                        left_index  = current.index - 1
                        top_index   = current.index - grid.icons_per_row

                        # Check Right
                        if (right_index < grid.grid_size and grid.icons[right_index] is not None and current.index % grid.icons_per_row != grid.icons[right_index].index % grid.icons_per_row and grid.icons[right_index].icon_type == icon.icon_type and grid.icons[right_index] not in matches):
                            matches.append(grid.icons[right_index])

                        # Check Bottom
                        if (bot_index < grid.grid_size and grid.icons[bot_index] is not None and grid.icons[bot_index].icon_type == icon.icon_type and grid.icons[bot_index] not in matches):
                            matches.append(grid.icons[bot_index])

                        # Check Left
                        if (left_index >= 0 and grid.icons[left_index] is not None and current.index % grid.icons_per_row != 0 and grid.icons[left_index].icon_type == icon.icon_type and grid.icons[left_index] not in matches):
                            matches.append(grid.icons[left_index])

                        # Check Top
                        if (top_index >= 0 and grid.icons[top_index] is not None and grid.icons[top_index].icon_type == icon.icon_type and grid.icons[top_index] not in matches):
                            matches.append(grid.icons[top_index])

                        idx += 1

                    # If the cluster is large enough, add it to the overall matches.
                    if len(matches) >= 10:
                        self.delete_matches(all_matches, check=False)
                        grid.shift_icons(mouse_event=False)

                    if len(matches) >= 3:
                        all_matches.extend(matches)

                    # Mark all icons in this cluster as processed.
                    for m in matches:
                        processed.add(m.index)

                # If any matches were found, process them.
                if all_matches:
                    print("Matched:", len(all_matches), all_matches[0].icon_type)
                    self.delete_matches(all_matches, True)
                    grid.shift_icons(mouse_event=True)
                    renpy.restart_interaction()
                else:
                    print("No Matches")
                    break

            grid.refill_grid()

        
        def delete_matches(self, matches, check):
            # Update objectives first (before clearing icons)
            if current_objectives:
                icon_counts = {}

                for icon in matches:
                    icon_type = icon.icon_type
                    icon_counts[icon_type] = icon_counts.get(icon_type, 0) + 1

                for icon_type, count in icon_counts.items():
                    decrement_amount = count // 3
                    if decrement_amount > 0:
                        print(f"AimsMet: {icon_type} x{decrement_amount}")
                        current_objectives.AimsMet(icon_type, decrement_amount)

                renpy.restart_interaction()
            # Schedule the fade-out transition in a new context.if current_objectives:
            renpy.call_in_new_context("delete_matches_callback", self, matches, check)


        def _delete_matches_callback(self, matches, check):
            renpy.transition(Dissolve(0.5))
            if check:
                # Filter out chain-locked icons so they aren’t destroyed.
                deletable_icons = [icon for icon in matches if not icon.chain_locked]
                for icon in deletable_icons:
                    grid.icons[icon.index] = None
                    icon.destroy()
                # Update score using only deletable icons.
                multiplier = len(deletable_icons) / 4
                self.score += round(self.base_points * (len(deletable_icons) + multiplier))
            grid.sprite_manager.redraw(0)
            renpy.restart_interaction()
            grid.shift_icons(mouse_event=True)
            self.check_target_score(conditions=False)


        def forced_compression(self):
            """
            Forced Compression: clears the middle row from the grid.
            Applies crush animation, updates objectives, shifts and refills.
            """
            rows = grid.grid_size // grid.icons_per_row
            center_row = rows // 2
            start_index = center_row * grid.icons_per_row
            end_index = start_index + grid.icons_per_row

            # Count the icons removed for objective update
            icon_counts = {}

            for i in range(start_index, end_index):
                tile = grid.icons[i]
                if tile is not None:
                    # Collect type for objectives
                    icon_type = tile.icon_type
                    icon_counts[icon_type] = icon_counts.get(icon_type, 0) + 1

                    # Animate and destroy
                    if tile.sprite:
                        tile.sprite.child = crush_anim
                    tile.destroy()
                    grid.icons[i] = None

            if current_objectives:
                for icon_type, count in icon_counts.items():
                    decrement_amount = count
                    if decrement_amount > 0:
                        current_objectives.AimsMet(icon_type, decrement_amount)

            # Mark skill as used
            self.forced_compression_used = True

            # Shift and refill the grid
            grid.shift_icons(mouse_event=True)
            grid.refill_grid()
            renpy.restart_interaction()
            

        def check_target_score(self, conditions):
            if (self.moves <= 0 or conditions):
                print(self.score)
                self.score *= round((self.moves/self.score + 1))
                renpy.call_in_new_context("win_screen")
                time.sleep(2)
        