init python:
    from collections import Counter
    import time
    class GameManager:
        def __init__(self, moves, target_score, level, sublevel):
            self.score = 0
            self.moves = moves
            self.base_points = 5
            self.target_score = target_score
            self.level = level      
            self.sublevel = sublevel 
            self.initializing = True

        def advance_sublevel(self):
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
                complete_sublevel(self.level, self.sublevel)
                new_label = "level_selection"
            renpy.jump(new_label)

        def retry_sublevel(self):
            renpy.jump("start_game")
        
        def find_match(self, mouse_event):
            while True:
                if self.initializing:
                    return
                processed = set()
                all_matches = []

                for icon in grid.icons:
                    if icon is None or icon.index in processed:
                        continue

                    matches = [icon]
                    idx = 0
                    while idx < len(matches):
                        current = matches[idx]
                        right_index = current.index + 1
                        bot_index   = current.index + grid.icons_per_row
                        left_index  = current.index - 1
                        top_index   = current.index - grid.icons_per_row

                        if (right_index < grid.grid_size and grid.icons[right_index] is not None and current.index % grid.icons_per_row != grid.icons[right_index].index % grid.icons_per_row and grid.icons[right_index].icon_type == icon.icon_type and grid.icons[right_index] not in matches):
                            matches.append(grid.icons[right_index])

                        if (bot_index < grid.grid_size and grid.icons[bot_index] is not None and grid.icons[bot_index].icon_type == icon.icon_type and grid.icons[bot_index] not in matches):
                            matches.append(grid.icons[bot_index])

                        if (left_index >= 0 and grid.icons[left_index] is not None and current.index % grid.icons_per_row != 0 and grid.icons[left_index].icon_type == icon.icon_type and grid.icons[left_index] not in matches):
                            matches.append(grid.icons[left_index])

                        if (top_index >= 0 and grid.icons[top_index] is not None and grid.icons[top_index].icon_type == icon.icon_type and grid.icons[top_index] not in matches):
                            matches.append(grid.icons[top_index])

                        idx += 1

                    if len(matches) >= 10:
                        self.delete_matches(all_matches, check=False)
                        grid.shift_icons(mouse_event=False)

                    if len(matches) >= 3:
                        all_matches.extend(matches)

                    for m in matches:
                        processed.add(m.index)

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
            renpy.call_in_new_context("delete_matches_callback", self, matches, check)


        def _delete_matches_callback(self, matches, check):
            renpy.transition(Dissolve(0.5))
            if check:
                deletable_icons = [icon for icon in matches if not icon.chain_locked]
                for icon in deletable_icons:
                    grid.icons[icon.index] = None
                    icon.destroy()
                multiplier = len(deletable_icons) / 4
                self.score += round(self.base_points * (len(deletable_icons) + multiplier))
            grid.sprite_manager.redraw(0)
            renpy.restart_interaction()
            grid.shift_icons(mouse_event=True)
            self.check_target_score(conditions=False)

        def check_target_score(self, conditions):
            if self.moves <= 0 or conditions:
                print("Score:", self.score)
                
                if self.score > 0:
                    multiplier = round((self.moves / self.score) + 1)
                    self.score *= multiplier

                complete_sublevel(self.level, self.sublevel)

                max_sub = len(persistent.level_progress.get(self.level, []))

                if self.sublevel >= max_sub:
                    renpy.call_in_new_context("win_level_screen")
                else:
                    renpy.call_in_new_context("win_sublevel_screen")

                renpy.pause(2)

        