init python:
    chain_image = Image("Icons/Chain.png")

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
            self.swap_attempted = False

            self.drag_offset_x = 0
            self.drag_offset_y = 0
            self.orig_position = None
            self.orig_index = None

            # For chain locking:
            self.chain_locked = False
            self.chain_overlay = None

        def compute_grid_position(self):
            """Compute the correct (x, y) coordinates based on the tile's grid index."""
            col = self.index % grid.icons_per_row
            row = self.index // grid.icons_per_row
            new_x = col * (grid.icon_size + grid.icon_padding)
            new_y = row * (grid.icon_size + grid.icon_padding)
            return new_x, new_y

        def snap_to_grid(self):
            """Force the tile's position to its proper grid cell based on its index."""
            new_x, new_y = self.compute_grid_position()
            self.x = new_x
            self.y = new_y
            if self.sprite:
                # Animate to the correct position.
                self.sprite.child = move_anim(new_x, new_y)
            # Update the chain overlay position if present.
            if self.chain_overlay:
                self.chain_overlay.x = new_x
                self.chain_overlay.y = new_y

        def update_sprite(self):
            """Reassign the sprite's image so that it reflects the tile's current type."""
            idle_image = Image("Icons/{}.png".format(self.icon_type))
            if self.sprite:
                self.sprite.child = Transform(child=idle_image, zoom=0.08)

        def update_chain_overlay(self):
            """Creates or updates the chain overlay if the tile is locked.
            If the tile is unlocked and an overlay exists, destroys it."""
            if self.chain_locked:
                if grid.sprite_manager is not None:
                    # Create the chain overlay if it does not already exist.
                    if not self.chain_overlay:
                        self.chain_overlay = grid.sprite_manager.create(
                            Transform(child=chain_image, zoom=0.05))
                    # Set its position to match the tile.
                    self.chain_overlay.x = self.x
                    self.chain_overlay.y = self.y
                else:
                    renpy.log("Warning: sprite_manager not available when updating chain overlay.")
            else:
                # If the tile is not locked but an overlay exists, destroy it.
                if self.chain_overlay:
                    self.chain_overlay.destroy()
                    self.chain_overlay = None

        def start_drag(self, mouse_x, mouse_y):
            """Called when the tile is picked up. Record its original grid position and index.
            If this tile is chain locked (and we’re in Level 3 or 4), block the drag."""
            # Only enforce chain lock in levels 3 and 4.
            if self.chain_locked:
                return  # Do nothing if the tile is locked.
            game.initializing = False
            self.is_dragging = True
            self.drag_offset_x = mouse_x
            self.drag_offset_y = mouse_y
            # Record the original grid position and index.
            self.orig_position = self.compute_grid_position()
            self.orig_index = self.index
            self.locked_axis = None
            self.swap_attempted = False

        def update_drag(self, mouse_x, mouse_y):
            """Called while dragging. Updates the tile's position and attempts a swap if possible."""
            if not self.is_dragging:
                return

            dx = mouse_x - self.drag_offset_x
            dy = mouse_y - self.drag_offset_y
            lock_threshold = 15
            snap_threshold = 120

            # Determine drag axis.
            if self.locked_axis is None:
                if abs(dx) >= lock_threshold or abs(dy) >= lock_threshold:
                    self.locked_axis = "x" if abs(dx) >= abs(dy) else "y"

            # Base the movement on the original grid cell.
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
                    # IMPORTANT: also check if the neighbor is chain-locked.
                    neighbor = grid.icons[swap_index]
                    if neighbor and not neighbor.chain_locked:
                        self.swap_attempted = True
                        self.try_swap(swap_index)
                        self.stop_drag(animate=True)
                    else:
                        # Do nothing if neighbor is locked.
                        self.snap_to_grid()
                        self.is_dragging = False

        def try_swap(self, neighbor_index):
            """
            Attempt to swap this tile with the neighbor at neighbor_index.
            Record the current (grid-computed) positions and indices, perform the swap,
            check for a valid match, and if invalid, revert the swap.
            """
            neighbor = grid.icons[neighbor_index]
            # If either tile is chain-locked, skip the swap.
            if self.chain_locked or neighbor.chain_locked:
                return False

            # Record original grid positions.
            orig_self_pos = self.orig_position
            orig_neighbor_pos = neighbor.compute_grid_position()
            orig_self_index = self.orig_index
            orig_neighbor_index = neighbor.index

            # Perform the swap (update grid and positions, animate).
            self.swap_with_neighbor(neighbor_index, animate=True)

            # Check for a valid match.
            if not grid.check_for_match():
                # Invalid swap: revert it.
                self.swap_with_neighbor(neighbor_index, animate=False)
                # Restore original grid indices.
                self.index = orig_self_index
                neighbor.index = orig_neighbor_index
                grid.icons[self.index] = self
                grid.icons[neighbor.index] = neighbor
                # Snap both tiles back to their original grid positions.
                self.x, self.y = orig_self_pos
                neighbor.x, neighbor.y = orig_neighbor_pos
                self.snap_to_grid()
                neighbor.snap_to_grid()
                # Update sprites so the visuals match.
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
                # Disable dragging.
                self.is_dragging = False
                neighbor.is_dragging = False
                return True

        def stop_drag(self, animate=False):
            """Ends the drag operation. If animate is True, snap back to grid cell."""
            if animate:
                self.snap_to_grid()
            self.is_dragging = False
            self.locked_axis = None
            self.swap_attempted = False
            return self.get_swap_index()

        def get_swap_index(self):
            """Return the index of an adjacent neighbor eligible for swapping, or None."""
            right_index = self.index + 1
            bot_index = self.index + grid.icons_per_row
            left_index = self.index - 1
            top_index = self.index - grid.icons_per_row

            valid_swaps = []
            # Right neighbor (if not at far right)
            if self.index % grid.icons_per_row < grid.icons_per_row - 1:
                if right_index < grid.grid_size and grid.icons[right_index] is not None and self.is_inside(grid.icons[right_index]):
                    valid_swaps.append(right_index)
            # Bottom neighbor.
            if bot_index < grid.grid_size and grid.icons[bot_index] is not None and self.is_inside(grid.icons[bot_index]):
                valid_swaps.append(bot_index)
            # Left neighbor (if not at far left)
            if self.index % grid.icons_per_row > 0:
                if left_index >= 0 and grid.icons[left_index] is not None and self.is_inside(grid.icons[left_index]):
                    valid_swaps.append(left_index)
            # Top neighbor.
            if top_index >= 0 and grid.icons[top_index] is not None and self.is_inside(grid.icons[top_index]):
                valid_swaps.append(top_index)
            return valid_swaps[0] if valid_swaps else None

        def is_inside(self, neighbor):
            """
            Check if the neighbor tile's center is within this tile's bounds.
            This is used to determine if a swap is allowed.
            """
            center_x = neighbor.x + grid.icon_size / 2
            center_y = neighbor.y + grid.icon_size / 2
            return (self.x <= center_x <= self.x + grid.icon_size and
                    self.y <= center_y <= self.y + grid.icon_size)

        def check_corners(self):
            # (Optional) Debug method to print diagonal swap possibilities.
            top_left_index = self.index - grid.icons_per_row - 1
            top_right_index = self.index - grid.icons_per_row + 1
            bottom_left_index = self.index + grid.icons_per_row - 1
            bottom_right_index = self.index + grid.icons_per_row + 1

            top_left = (top_left_index >= 0 and self.index % grid.icons_per_row != 0 and
                        grid.icons[top_left_index] is not None and self.is_inside(grid.icons[top_left_index]) and
                        grid.icons[top_left_index].icon_type == self.icon_type)
            top_right = (self.index % grid.icons_per_row != grid.icons_per_row - 1 and top_right_index >= 0 and
                        grid.icons[top_right_index] is not None and self.is_inside(grid.icon[top_right_index]) and
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
            """
            Swap this tile with the neighbor at neighbor_index.
            This method updates the grid data, the tile positions, and optionally animates the swap.
            """
            neighbor = grid.icons[neighbor_index]
            # Swap in the grid list.
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
            if self.chain_overlay:
                self.chain_overlay.destroy()
                self.chain_overlay = None
