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
            self.is_dragging = True

            self.drag_offset_x = mouse_x
            self.drag_offset_y = mouse_y

            self.original_x = self.x
            self.original_y = self.y

            self.locked_axis = None

        def update_drag(self, mouse_x, mouse_y):
            if self.is_dragging:
                # print(self.index, self.icon_type)
                dx = mouse_x - self.drag_offset_x
                dy = mouse_y - self.drag_offset_y
                lock_threshold = 15
                snap_threshold = 120

                if self.locked_axis is None:
                    if abs(dx) >= lock_threshold or abs(dy) >= lock_threshold:
                        self.locked_axis = "x" if abs(dx) >= abs(dy) else "y"
                        
                if self.locked_axis == "x":
                    # Allow horizontal movement only. The direction (positive or negative) follows the mouse.
                    self.x = self.original_x + dx
                    if abs(dx) >= snap_threshold:
                        self.stop_drag()
                elif self.locked_axis == "y":
                    # Allow vertical movement only.
                    self.y = self.original_y + dy
                    if abs(dy) >= snap_threshold:
                        self.stop_drag()

                swap_index = self.get_swap_index()
                if swap_index is not None:
                    self.swap_with_neighbor(swap_index)
                    self.stop_drag()

        def stop_drag(self):
            if self.x != self.original_x or self.y != self.original_y:
                self.x = self.original_x
                self.y = self.original_y
            self.is_dragging = False
            self.locked_axis = None
            return self.get_swap_index()

        def get_swap_index(self):
            # print(self.icon_type)
            # Find neighbors (left, right, up, down)
            right_index = self.index + 1
            bot_index   = self.index + grid.icons_per_row
            left_index  = self.index - 1
            top_index   = self.index - grid.icons_per_row

            valid_swaps = []
            # Check Right
            if (right_index < grid.grid_size and grid.icons[right_index] is not None and self.index % grid.icons_per_row != grid.icons[right_index].index % grid.icons_per_row and self.is_inside(grid.icons[right_index])):
                print("Right:", self.is_inside(grid.icons[right_index]))
                # self.check_corners()
                valid_swaps.append(right_index)

            # Check Bottom
            if (bot_index < grid.grid_size and grid.icons[bot_index] is not None and self.is_inside(grid.icons[bot_index])):
                print("Bot:", self.is_inside(grid.icons[bot_index]))
                # self.check_corners()
                valid_swaps.append(bot_index)

            # Check Left
            if (left_index >= 0 and grid.icons[left_index] is not None and self.index % grid.icons_per_row != 0 and self.is_inside(grid.icons[left_index])):
                print("Left:", self.is_inside(grid.icons[left_index]))
                # self.check_corners()
                valid_swaps.append(left_index)

            # Check Top
            if (top_index >= 0 and grid.icons[top_index] is not None and self.is_inside(grid.icons[top_index])):
                print("Top:", self.is_inside(grid.icons[top_index]))
                # self.check_corners()
                valid_swaps.append(top_index)

            return valid_swaps[0] if valid_swaps else None  # No valid swap

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

        def swap_with_neighbor(self, neighbor_index):
            neighbor = grid.icons[neighbor_index]

            # Swap the positions
            grid.icons[self.index], grid.icons[neighbor_index] = (
                grid.icons[neighbor_index], grid.icons[self.index]
            )
            self.x, neighbor.x = neighbor.x, self.x
            self.y, neighbor.y = neighbor.y, self.y

            # Swap the indices
            self.index, neighbor.index = neighbor.index, self.index
            self.stop_drag()

        def destroy(self):
            if self.sprite:
                self.sprite.destroy()