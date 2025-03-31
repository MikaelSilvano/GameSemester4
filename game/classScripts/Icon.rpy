init python:
    class Icon:
        def __init__(self, index, x, y, icon_type, sprite):
            self.index = index
            self.x = x
            self.y = y
            self.icon_type = icon_type
            self.sprite = sprite
            self.grid = grid.icons
            self.tile_size = grid.icon_size

            self.is_dragging = False
            self.locked_axis = None

            self.drag_offset_x = 0
            self.drag_offset_y = 0
            self.original_x = None
            self.original_y = None
        
        def start_drag(self, mouse_x, mouse_y):
            game.initializing = False
            self.is_dragging = True

            self.drag_offset_x = mouse_x
            self.drag_offset_y = mouse_y

            self.original_x = self.x
            self.original_y = self.y

            self.locked_axis = None

        def update_drag(self, mouse_x, mouse_y):
            if self.is_dragging:
                dx = mouse_x - self.drag_offset_x
                dy = mouse_y - self.drag_offset_y
                lock_threshold = 15
                snap_threshold = 120

                if self.locked_axis is None:
                    if abs(dx) >= lock_threshold or abs(dy) >= lock_threshold:
                        self.locked_axis = "x" if abs(dx) >= abs(dy) else "y"

                # Update position along the locked axis
                if self.locked_axis == "x":
                    self.x = self.original_x + dx
                    if abs(dx) >= snap_threshold:
                        self.stop_drag(animate=True)
                elif self.locked_axis == "y":
                    self.y = self.original_y + dy
                    if abs(dy) >= snap_threshold:
                        self.stop_drag(animate=True)

                swap_index = self.get_swap_index()
                if swap_index is not None:
                    self.swap_with_neighbor(swap_index, animate=True)
                    # After swapping, check if a valid match was created.
                    # (Assume grid.check_for_match() returns True if a match exists.)
                    if not grid.check_for_match():
                        # No match? Then revert the swap with an animation.
                        self.swap_with_neighbor(swap_index, animate=True, revert=True)
                    # End dragging regardless.
                    self.stop_drag(animate=False)

                #if not grid.check_for_match():
                    #self.swap_with_neighbor(swap_index, animate=True, revert=True)



        def stop_drag(self, animate=False):
            if animate and (self.x != self.original_x or self.y != self.original_y):
                self.sprite.child = move_anim(self.original_x, self.original_y)
            self.x = self.original_x
            self.y = self.original_y
            self.is_dragging = False
            self.locked_axis = None
            return self.get_swap_index()


        def get_swap_index(self):
            # Look for neighbors in four directions.
            right_index = self.index + 1
            bot_index = self.index + grid.icons_per_row
            left_index = self.index - 1
            top_index = self.index - grid.icons_per_row

            valid_swaps = []
            if (right_index < grid.grid_size and grid.icons[right_index] is not None and
                self.index % grid.icons_per_row != grid.icons[right_index].index % grid.icons_per_row and
                self.is_inside(grid.icons[right_index])):
                valid_swaps.append(right_index)
            if (bot_index < grid.grid_size and grid.icons[bot_index] is not None and
                self.is_inside(grid.icons[bot_index])):
                valid_swaps.append(bot_index)
            if (left_index >= 0 and grid.icons[left_index] is not None and
                self.index % grid.icons_per_row != 0 and
                self.is_inside(grid.icons[left_index])):
                valid_swaps.append(left_index)
            if (top_index >= 0 and grid.icons[top_index] is not None and
                self.is_inside(grid.icons[top_index])):
                valid_swaps.append(top_index)

            return valid_swaps[0] if valid_swaps else None

        def check_corners(self):
            ##
            ## Check Diagonals / Corners
            ##

            top_left_index = self.index - grid.icons_per_row - 1
            top_right_index = self.index - grid.icons_per_row + 1
            bottom_left_index = self.index + grid.icons_per_row - 1
            bottom_right_index = self.index + grid.icons_per_row + 1

            top_left = top_left_index >= 0 and self.index % grid.icons_per_row != 0 and grid.icons[top_left_index] is not None and self.is_inside(grid.icons[top_left_index]) and grid.icons[top_left_index].icon_type == self.icon_type
            top_right = self.index % grid.icons_per_row != grid.icons_per_row - 1 and top_right_index >= 0 and grid.icons[top_right_index] is not None and self.is_inside(grid.icons[top_right_index]) and grid.icons[top_right_index].icon_type == self.icon_type
            bot_left = self.index % grid.icons_per_row != 0 and bottom_left_index < grid.grid_size and grid.icons[bottom_left_index] is not None and self.is_inside(grid.icons[bottom_left_index]) and grid.icons[bottom_left_index].icon_type == self.icon_type
            bot_right = self.index % grid.icons_per_row != grid.icons_per_row - 1 and bottom_right_index < grid.grid_size and grid.icons[bottom_right_index] is not None and self.is_inside(grid.icons[bottom_right_index]) and grid.icons[bottom_right_index].icon_type == self.icon_type
            
            print(top_left, top_right, bot_right, bot_left)
            # Check for left
            if (top_left or bot_left):
                print("Can switch left")
            
            if (top_left or top_right):
                print("Can switch up")

            if (top_right or bot_right):
                print("Can switch right")

            if (bot_right or bot_left):
                print("Can switch down")
            return True

        def is_inside(self, neighbor):
            if self.locked_axis == "y":
                return (neighbor.y < self.y < neighbor.y + grid.icon_size)
            if self.locked_axis == "x":
                return (neighbor.x < self.x < neighbor.x + grid.icon_size)
            return False

        def swap_with_neighbor(self, neighbor_index, animate=False, revert=False):
            neighbor = grid.icons[neighbor_index]

            # Swap the two icons in the grid.
            grid.icons[self.index], grid.icons[neighbor_index] = grid.icons[neighbor_index], grid.icons[self.index]
            # Swap positions.
            self.x, neighbor.x = neighbor.x, self.x
            self.y, neighbor.y = neighbor.y, self.y
            # Swap indices.
            self.index, neighbor.index = neighbor.index, self.index

            if animate:
                # Use our custom move_anim transform for smooth movement.
                self.sprite.child = move_anim(self.x, self.y)
                neighbor.sprite.child = move_anim(neighbor.x, neighbor.y)
            return


        def destroy(self):
            if self.sprite:
                self.sprite.destroy()