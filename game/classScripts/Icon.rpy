init python:
    class Icon:
        def __init__(self, index, x, y, icon_type, sprite):
            self.index = index
            self.x = x
            self.y = y
            self.icon_type = icon_type
            self.sprite = sprite
            # Shortcut to grid list and grid settings
            self.grid = grid.icons  
            self.tile_size = grid.icon_size

            self.is_dragging = False
            self.locked_axis = None

            self.drag_offset_x = 0
            self.drag_offset_y = 0
            # We'll record the original grid position at drag start.
            self.orig_position = None  # (x, y)
            self.orig_index = None

            self.swap_attempted = False

        def compute_grid_position(self):
            """Compute the correct (x, y) position for this tile based on its grid index."""
            col = self.index % grid.icons_per_row
            row = self.index // grid.icons_per_row
            new_x = col * (grid.icon_size + grid.icon_padding)
            new_y = row * (grid.icon_size + grid.icon_padding)
            return new_x, new_y

        def snap_to_grid(self):
            """Snap this tile’s position to the computed grid cell."""
            new_x, new_y = self.compute_grid_position()
            self.x = new_x
            self.y = new_y
            if self.sprite:
                self.sprite.child = move_anim(new_x, new_y)

        def update_sprite(self):
            """Update the sprite’s image based on the tile’s icon_type."""
            idle_image = Image("Icons/{}.png".format(self.icon_type))
            if self.sprite:
                self.sprite.child = Transform(child=idle_image, zoom=0.08)

        def start_drag(self, mouse_x, mouse_y):
            """Called when the tile is first picked up.
            Record the tile’s original grid position and index."""
            game.initializing = False
            self.is_dragging = True
            self.drag_offset_x = mouse_x
            self.drag_offset_y = mouse_y
            # Record the proper grid position and grid index at start.
            self.orig_position = self.compute_grid_position()
            self.orig_index = self.index
            self.locked_axis = None
            self.swap_attempted = False

        def update_drag(self, mouse_x, mouse_y):
            """Called as the tile is dragged.
            Updates the tile’s position along a locked axis and attempts a swap."""
            if not self.is_dragging:
                return

            dx = mouse_x - self.drag_offset_x
            dy = mouse_y - self.drag_offset_y
            lock_threshold = 15
            snap_threshold = 85

            if self.locked_axis is None:
                if abs(dx) >= lock_threshold or abs(dy) >= lock_threshold:
                    self.locked_axis = "x" if abs(dx) >= abs(dy) else "y"

            # Instead of using the original drag offsets alone, base our
            # update on the original grid position.
            orig_x, orig_y = self.orig_position
            if self.locked_axis == "x":
                self.x = orig_x + dx
                if abs(dx) >= snap_threshold:
                    self.stop_drag(animate=True)
            elif self.locked_axis == "y":
                self.y = orig_y + dy
                if abs(dy) >= snap_threshold:
                    self.stop_drag(animate=True)

            # Attempt a swap only once.
            if not self.swap_attempted:
                swap_index = self.get_swap_index()
                if swap_index is not None:
                    self.swap_attempted = True
                    self.try_swap(swap_index)
                    self.stop_drag(animate=True)

        def try_swap(self, neighbor_index):
            """
            Attempt to swap this tile with the neighbor at neighbor_index.
            Records the current (grid-computed) positions and indices,
            performs the swap, checks for a match, and if invalid, reverts.
            """
            neighbor = grid.icons[neighbor_index]
            # Record original grid positions and indices from drag start.
            orig_self_pos = self.orig_position
            orig_neighbor_pos = neighbor.compute_grid_position()
            orig_self_index = self.orig_index
            orig_neighbor_index = neighbor.index

            # Perform the swap.
            self.swap_with_neighbor(neighbor_index, animate=True)

            # Check if a valid match results.
            if not grid.check_for_match():
                # Invalid swap: revert the swap.
                self.swap_with_neighbor(neighbor_index, animate=False)
                # Restore original grid indices.
                self.index = orig_self_index
                neighbor.index = orig_neighbor_index
                grid.icons[self.index] = self
                grid.icons[neighbor.index] = neighbor
                # Snap both tiles back to their proper grid positions.
                self.x, self.y = orig_self_pos
                neighbor.x, neighbor.y = orig_neighbor_pos
                self.snap_to_grid()
                neighbor.snap_to_grid()
                self.update_sprite()
                neighbor.update_sprite()
                self.is_dragging = False
                neighbor.is_dragging = False
                return False
            else:
                # Valid swap: update the original state to the new grid cell.
                self.orig_position = self.compute_grid_position()
                self.orig_index = self.index
                neighbor.orig_position = neighbor.compute_grid_position()
                # Disable further dragging.
                self.is_dragging = False
                neighbor.is_dragging = False
                return True

        def stop_drag(self, animate=False):
            """Stop the drag and snap the tile back to its grid cell."""
            if animate:
                self.snap_to_grid()
            self.is_dragging = False
            self.locked_axis = None
            self.swap_attempted = False
            return self.get_swap_index()

        def get_swap_index(self):
            """Return the index of a neighbor tile eligible for swapping, or None."""
            right_index = self.index + 1
            bot_index = self.index + grid.icons_per_row
            left_index = self.index - 1
            top_index = self.index - grid.icons_per_row

            valid_swaps = []
            # Right neighbor (only if not at the far right)
            if self.index % grid.icons_per_row < grid.icons_per_row - 1:
                if right_index < grid.grid_size and grid.icons[right_index] is not None and self.is_inside(grid.icons[right_index]):
                    valid_swaps.append(right_index)
            # Bottom neighbor.
            if bot_index < grid.grid_size and grid.icons[bot_index] is not None and self.is_inside(grid.icons[bot_index]):
                valid_swaps.append(bot_index)
            # Left neighbor (only if not at the far left)
            if self.index % grid.icons_per_row > 0:
                if left_index >= 0 and grid.icons[left_index] is not None and self.is_inside(grid.icons[left_index]):
                    valid_swaps.append(left_index)
            # Top neighbor.
            if top_index >= 0 and grid.icons[top_index] is not None and self.is_inside(grid.icons[top_index]):
                valid_swaps.append(top_index)
            return valid_swaps[0] if valid_swaps else None

        def is_inside(self, neighbor):
            """
            Check if the neighbor tile overlaps the current tile's area
            sufficiently to allow a swap.
            """
            # This check can be simplified: if the neighbor's center is within our bounds.
            center_x = neighbor.x + grid.icon_size / 2
            center_y = neighbor.y + grid.icon_size / 2
            return (self.x <= center_x <= self.x + grid.icon_size and
                    self.y <= center_y <= self.y + grid.icon_size)

        def check_corners(self):
            # Retain your corner checking if needed.
            top_left_index = self.index - grid.icons_per_row - 1
            top_right_index = self.index - grid.icons_per_row + 1
            bottom_left_index = self.index + grid.icons_per_row - 1
            bottom_right_index = self.index + grid.icons_per_row + 1

            top_left = (top_left_index >= 0 and self.index % grid.icons_per_row != 0 and
                        grid.icons[top_left_index] is not None and self.is_inside(grid.icons[top_left_index]) and
                        grid.icons[top_left_index].icon_type == self.icon_type)
            top_right = (self.index % grid.icons_per_row != grid.icons_per_row - 1 and top_right_index >= 0 and
                        grid.icons[top_right_index] is not None and self.is_inside(grid.icons[top_right_index]) and
                        grid.icons[top_right_index].icon_type == self.icon_type)
            bot_left = (self.index % grid.icons_per_row != 0 and bottom_left_index < grid.grid_size and
                        grid.icons[bottom_left_index] is not None and self.is_inside(grid.icons[bottom_left_index]) and
                        grid.icons[bottom_left_index].icon_type == self.icon_type)
            bot_right = (self.index % grid.icons_per_row != grid.icons_per_row - 1 and bottom_right_index < grid.grid_size and
                        grid.icons[bottom_right_index] is not None and self.is_inside(grid.icons[bottom_right_index]) and
                        grid.icons[bottom_right_index].icon_type == self.icon_type)
            
            print(top_left, top_right, bot_right, bot_left)
            if top_left or bot_left:
                print("Can switch left")
            if top_left or top_right:
                print("Can switch up")
            if top_right or bot_right:
                print("Can switch right")
            if bot_right or bot_left:
                print("Can switch down")
            return True

        def swap_with_neighbor(self, neighbor_index, animate=False):
            """Swap this tile with the neighbor at neighbor_index in grid data and positions."""
            neighbor = grid.icons[neighbor_index]
            # Swap in the grid array.
            grid.icons[self.index], grid.icons[neighbor_index] = grid.icons[neighbor_index], grid.icons[self.index]
            # Swap positions.
            self.x, neighbor.x = neighbor.x, self.x
            self.y, neighbor.y = neighbor.y, self.y
            # Swap grid indices.
            self.index, neighbor.index = neighbor.index, self.index
            if animate:
                self.sprite.child = move_anim(self.x, self.y)
                neighbor.sprite.child = move_anim(neighbor.x, neighbor.y)

        def destroy(self):
            if self.sprite:
                self.sprite.destroy()
