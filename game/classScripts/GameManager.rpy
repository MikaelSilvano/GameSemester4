init python:
    from collections import Counter
    
    class GameManager:
        def __init__(self, moves, target_score):
            self.score = 0
            self.moves = moves
            self.base_points = 5
            self.target_score = target_score
            self.initializing = True  # <-- New flag to indicate startup state
        
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
            # Fade out the matched tiles using a transition.
            renpy.transition(Dissolve(0.5))
            multiplier = len(matches) / 4
            if check:
                for icon in matches:
                    grid.icons[icon.index] = None
                    icon.destroy()
                self.score += round(self.base_points * (len(matches) + multiplier))
            
            grid.sprite_manager.redraw(0)
            renpy.restart_interaction()
            grid.shift_icons(mouse_event=True)
            self.check_target_score()


        def check_target_score(self):
            if (self.moves <= 0):
                print(self.score)
                self.score *= round((self.moves/self.score + 1))
                renpy.call_in_new_context("win_screen")
        
        def decrement_moves(self):
            self.moves -= 1