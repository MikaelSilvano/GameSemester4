init python:
    import random
    from typing import List
    import pygame
    import math

    class GridManager:
        def __init__(self, icons_per_row, grid_size):
            self.icons = []
            self.sprite_manager = SpriteManager(layer = "match3")
            self.icon_size = 100
            self.icon_padding = 10
            self.icons_per_row = icons_per_row
            self.grid_size = grid_size
            self.icon_images = icon_image_use
            self.fixed_positions = None
            self.current_checked_index = None

        def has_initial_match(self):
            for index, icon in enumerate(self.icons):
                if icon is not None:
                    if len(self.get_cluster(index)) >= 3:
                        return True
            return False

        def initialize_grid(self, fixed_positions=None):
            if fixed_positions is None and game.level in (3,4):
                total = self.grid_size
                chain_count = int(total * 0.15)
                rows = self.grid_size // self.icons_per_row
                all_positions = [(col, row) for row in range(rows) for col in range(self.icons_per_row)]
                fixed_positions = random.sample(all_positions, chain_count)

            self.fixed_positions = fixed_positions 

            valid_grid = False
            print ("valid grid:", valid_grid)
            while not valid_grid:
                self.icons = [None] * self.grid_size
                for index in range(self.grid_size):
                    col = index % self.icons_per_row
                    row = index // self.icons_per_row
                    x = col * (self.icon_size + self.icon_padding)
                    y = row * (self.icon_size + self.icon_padding)
                    
                    allowed_types = self.icon_images[:] 
                    valid = False
                    while not valid and allowed_types:
                        tile_type = renpy.random.choice(allowed_types)
                        fixed_chain = False
                        if fixed_positions is not None and (col, row) in fixed_positions:
                            fixed_chain = True
                        self.icons[index] = Icon(index=index, x=x, y=y,
                                                icon_type=tile_type, sprite=None,
                                                chain_locked=fixed_chain)
                        cluster = self.get_cluster(index)
                        if len(cluster) < 3:
                            valid = True
                        else:
                            allowed_types.remove(tile_type)
                    if not valid:
                        tile_type = renpy.random.choice(self.icon_images)
                        fixed_chain = False
                        if fixed_positions is not None and (col, row) in fixed_positions:
                            fixed_chain = True
                        self.icons[index] = Icon(index=index, x=x, y=y,
                                                icon_type=tile_type, sprite=None,
                                                chain_locked=fixed_chain)
                if not self.has_initial_match():
                    valid_grid = True
                    sprite_manager = self.create_sprite_manager()
            global grid
            grid = self

        def get_cluster(self, index):
            start_icon = self.icons[index]
            if start_icon is None:
                return []
            # if start_icon.chain_locked:
            #     return []
            cluster = set()
            to_check = [index]
            while to_check:
                cur = to_check.pop()
                if cur in cluster:
                    continue
                cluster.add(cur)
                col = cur % self.icons_per_row
                row = cur // self.icons_per_row
                neighbors = []
                if col > 0:
                    neighbors.append(cur - 1)
                if col < self.icons_per_row - 1:
                    neighbors.append(cur + 1)
                if row > 0:
                    neighbors.append(cur - self.icons_per_row)
                if row < (self.grid_size // self.icons_per_row) - 1:
                    neighbors.append(cur + self.icons_per_row)
                for n in neighbors:
                    if (self.icons[n] is not None and
                        not self.icons[n].chain_locked and
                        self.icons[n].icon_type == start_icon.icon_type and
                        n not in cluster):
                        to_check.append(n)
            return list(cluster)

        def create_sprite_manager(self):
            self.sprite_manager = SpriteManager(update=self.update_icon,
                                                event=self.handle_event)
            return self.sprite_manager

        def update_icon(self, st):
            for icon in self.icons:
                if icon and icon.sprite:
                    icon.sprite.x = icon.x
                    icon.sprite.y = icon.y
                if icon and icon.chain_locked and icon.chain_overlay:
                    icon.chain_overlay.x = icon.x
                    icon.chain_overlay.y = icon.y
            return 0

        def is_mouse_within_grid(self, x: float, y: float) -> bool:
            """
            Hit‑test: returns True if the given (x, y) coordinate
            lies within the current grid bounds, False otherwise.
            """
            # If there are no icons laid out, there’s no valid grid area
            if not self.icons:
                return False

            # Derive the grid’s extents from icon positions + icon_size
            xs = [icon.x for icon in self.icons if icon is not None]
            ys = [icon.y for icon in self.icons if icon is not None]

            min_x = min(xs)
            min_y = min(ys)
            max_x = max(xs) + self.icon_size
            max_y = max(ys) + self.icon_size

            # Return True only if the point lies within those bounds
            return (min_x <= x <= max_x) and (min_y <= y <= max_y)

        def handle_event(self, event, x, y, st):
            if not self.is_mouse_within_grid(x, y):
                return
            self.shift_icons(mouse_event=False)
            game.find_match(mouse_event=False)
            
            # make me a condition so that if the mouse is outside the grid, it doesn't start dragging, use only existing variables
            # --- compute the grid's bounding rectangle from your icons ---

            if event.type == 1024:
                for icon in self.icons:
                    if icon and icon.is_dragging:
                        icon.update_drag(x, y)
            if event.type == 1025 and event.button == 1:
                for icon in self.icons:
                    if skill_active == True and icon.x <= x <= (icon.x + self.icon_size) and icon.y <= y <= (icon.y + self.icon_size):            
                        if len(store.icon_skill_collected) != 0:
                            if store.In_stored == 0:
                                store.icon_skill_collected.clear()
                        store.In_stored = 0
                        if persistent.current_skill == 3:
                        # append into YOUR manager’s list
                            store.icon_skill_collected.append(icon.index)
                            store.In_stored+=1

                            # once you have two picks, try the swap
                            if len(store.icon_skill_collected) == required_targets:
                                i1, i2 = store.icon_skill_collected
                                store.icon_skill_collected.clear()

                                success = skill.blueprint_swap(i1, i2)

                                if success:
                                    store.time_countdown_left = 10
                                    store.non_violatable_time = 10
                                    renpy.show_screen("countdown")
                                else:
                                    break
                        elif persistent.current_skill == 4:
                            store.icon_skill_collected.append(icon.index)
                            if len(store.icon_skill_collected) == required_targets:
                                if (skill.masterpiece_build(store.icon_skill_collected[0])):
                                    store.time_countdown_left = 20
                                    store.non_violatable_time = 20
                                    store.icon_skill_collected.clear()
                                    renpy.show_screen("countdown")
                                else:
                                    store.icon_skill_collected.clear()
                                    continue
                    elif icon and icon.x <= x <= (icon.x + self.icon_size) and icon.y <= y <= (icon.y + self.icon_size):
                        store.icon_skill_collected.clear()
                        icon.start_drag(x, y)
                        break
            if event.type == 1026 and event.button == 1:
                for icon in self.icons:
                    if icon and (icon.x <= x <= (icon.x + self.icon_size) and
                                icon.y <= y <= (icon.y + self.icon_size)) and icon.is_dragging:
                        store.icon_skill_collected.clear()
                        icon.stop_drag()
                        break

        def shift_icons(self, mouse_event):
            moved = False
            icons_per_col = self.grid_size // self.icons_per_row

            # Go column by column, bottom to top
            for col in range(self.icons_per_row):
                for row in reversed(range(icons_per_col)):
                    index = row * self.icons_per_row + col
                    icon = self.icons[index]

                    # skip empty or locked icons
                    if icon is None or icon.chain_locked:
                        continue

                    # find the lowest available empty cell below this icon
                    target_row = row
                    while (
                        target_row + 1 < icons_per_col and
                        self.icons[(target_row + 1) * self.icons_per_row + col] is None
                    ):
                        target_row += 1

                    # only move if there's an empty space below
                    if target_row != row:
                        new_index = target_row * self.icons_per_row + col
                        self.icons[new_index] = icon
                        self.icons[index] = None

                        new_y = target_row * (self.icon_size + self.icon_padding)
                        move_sprite(icon.sprite, icon.x, new_y, duration=0.4)
                        icon.y = new_y
                        icon.index = new_index
                        moved = True

            # after all icons fall, check for new matches
            matches = []
            for i, icon in enumerate(self.icons):
                if icon is not None:
                    cluster = self.get_cluster(i)
                    if len(cluster) >= 3:
                        for idx in cluster:
                            if self.icons[idx] not in matches:
                                matches.append(self.icons[idx])

            # if matches are found, delete them and update objectives
            if matches:
                game.delete_matches(matches, True)

            # return whether any movement occurred
            return moved

        def refill_grid(self):
        
            store.idle_player = True
            for i in range(self.grid_size):
                if self.icons[i] is not None:
                    continue
                col = i % self.icons_per_row
                row = i // self.icons_per_row
                if self.fixed_positions and (col, row) in self.fixed_positions:
                    continue

                allowed = self.icon_images[:]
                if col >= 2:
                    left1 = self.icons[i - 1]
                    left2 = self.icons[i - 2]
                    if left1 is not None and left2 is not None and left1.icon_type == left2.icon_type:
                        forbidden = left1.icon_type
                        if forbidden in allowed:
                            allowed.remove(forbidden)
                if row >= 2:
                    above1 = self.icons[i - self.icons_per_row]
                    above2 = self.icons[i - 2 * self.icons_per_row]
                    if above1 is not None and above2 is not None and above1.icon_type == above2.icon_type:
                        forbidden = above1.icon_type
                        if forbidden in allowed:
                            allowed.remove(forbidden)

                if not allowed:
                    candidate = renpy.random.choice(self.icon_images)
                else:
                    candidate = renpy.random.choice(allowed)
                
                idle_image = Image("Icons/{}.png".format(candidate))
                new_sprite = self.sprite_manager.create(Transform(child=idle_image, zoom=0.08))
                new_sprite.x = col * (self.icon_size + self.icon_padding)
                new_sprite.y = -(self.icon_size + self.icon_padding)
                
                self.icons[i] = Icon(
                    index=i,
                    x=col * (self.icon_size + self.icon_padding),
                    y=row * (self.icon_size + self.icon_padding),
                    icon_type=candidate,
                    sprite=new_sprite,
                    chain_locked=False
                )
        
            store.idle_player = False
            
        def clear_grid(self):
            renpy.hide_screen("result", immediately=True)
            game.score = 0
            for icon in self.icons:
                if icon:
                    icon.destroy()
            self.icons.clear()
            self.sprite_manager.redraw(0)

        def check_for_match(self):
            rows = self.grid_size // self.icons_per_row
            for row in range(rows):
                for col in range(self.icons_per_row - 2):
                    index = row * self.icons_per_row + col
                    if self.icons[index] is not None:
                        icon_type = self.icons[index].icon_type
                        if (self.icons[index + 1] is not None and self.icons[index + 1].icon_type == icon_type and
                            self.icons[index + 2] is not None and self.icons[index + 2].icon_type == icon_type):
                            return True
            for col in range(self.icons_per_row):
                for row in range(rows - 2):
                    index = row * self.icons_per_row + col
                    if self.icons[index] is not None:
                        icon_type = self.icons[index].icon_type
                        if (self.icons[index + self.icons_per_row] is not None and self.icons[index + self.icons_per_row].icon_type == icon_type and
                            self.icons[index + 2 * self.icons_per_row] is not None and self.icons[index + 2 * self.icons_per_row].icon_type == icon_type):
                            return True
            return False

        