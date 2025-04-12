init python:
    # Make sure you have the chain image in "Icons/Chain.png".
    chain_image = Image("Icons/Chain.png")

    class Icon:
        def __init__(self, index, x, y, icon_type, sprite, chain_locked=False):
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

            # Add chain_locked as a constructor parameter.
            self.chain_locked = chain_locked
            self.chain_overlay = None

            # Create/update overlay immediately if locked:
            self.update_chain_overlay()

        def compute_grid_position(self):
            """Compute the correct (x, y) coordinates based on the tile's grid index."""
            col = self.index % grid.icons_per_row
            row = self.index // grid.icons_per_row
            new_x = col * (grid.icon_size + grid.icon_padding)
            new_y = row * (grid.icon_size + grid.icon_padding)
            return new_x, new_y

        def snap_to_grid(self):
            """Snap the tile to its grid cell based on index."""
            new_x, new_y = self.compute_grid_position()
            self.x = new_x
            self.y = new_y
            if self.sprite:
                # Animate to the correct position.
                self.sprite.child = move_anim(new_x, new_y)
            # Also move the chain overlay if it exists.
            if self.chain_overlay:
                self.chain_overlay.x = new_x
                self.chain_overlay.y = new_y

        def update_sprite(self):
            """Change the tile's displayed image if icon_type changes."""
            idle_image = Image("Icons/{}.png".format(self.icon_type))
            if self.sprite:
                self.sprite.child = Transform(child=idle_image, zoom=0.08)

        def update_chain_overlay(self):
            """
            If chain_locked is True, display a chain overlay.
            If chain_locked is False, remove any existing overlay.
            """
            if self.chain_locked:
                if grid.sprite_manager is not None:
                    # Create the overlay if it doesn't exist yet.
                    if not self.chain_overlay:
                        self.chain_overlay = grid.sprite_manager.create(
                            Transform(child=chain_image, zoom=0.05)
                        )
                    self.chain_overlay.x = self.x
                    self.chain_overlay.y = self.y
                else:
                    renpy.log("Warning: sprite_manager not available for chain overlay.")
            else:
                # If not locked, ensure no overlay remains.
                if self.chain_overlay:
                    self.chain_overlay.destroy()
                    self.chain_overlay = None

        def start_drag(self, mouse_x, mouse_y):
            """
            Called when the tile is picked up.
            If chain_locked is True, immediately return so it can't be moved.
            """
            if self.chain_locked:
                return
            game.initializing = False
            self.is_dragging = True
            self.drag_offset_x = mouse_x
            self.drag_offset_y = mouse_y
            self.orig_position = self.compute_grid_position()
            self.orig_index = self.index
            self.locked_axis = None
            self.swap_attempted = False

        def update_drag(self, mouse_x, mouse_y):
            """Called while dragging. Updates position & tries swap if threshold is met."""
            if not self.is_dragging:
                return

            dx = mouse_x - self.drag_offset_x
            dy = mouse_y - self.drag_offset_y
            lock_threshold = 15
            snap_threshold = 120

            # Determine whether we lock movement horizontally or vertically.
            if self.locked_axis is None:
                if abs(dx) >= lock_threshold or abs(dy) >= lock_threshold:
                    self.locked_axis = "x" if abs(dx) >= abs(dy) else "y"

            orig_x, orig_y = self.orig_position
            if self.locked_axis == "x":
                self.x = orig_x + dx
                if abs(dx) >= snap_threshold:
                    self.stop_drag(animate=True)
            elif self.locked_axis == "y":
                self.y = orig_y + dy
                if abs(dy) >= snap_threshold:
                    self.stop_drag(animate=True)

            # Attempt one swap.
            if not self.swap_attempted:
                swap_index = self.get_swap_index()
                if swap_index is not None:
                    neighbor = grid.icons[swap_index]
                    # If neighbor is locked, skip swapping.
                    if neighbor and not neighbor.chain_locked:
                        self.swap_attempted = True
                        self.try_swap(swap_index)
                        self.stop_drag(animate=True)
                    else:
                        # If neighbor is locked, revert.
                        self.snap_to_grid()
                        self.is_dragging = False

        def try_swap(self, neighbor_index):
            """
            Swap this tile with the neighbor at neighbor_index.
            If no valid match, revert the swap.
            """
            neighbor = grid.icons[neighbor_index]
            # If either is locked, do nothing.
            if self.chain_locked or neighbor.chain_locked:
                return False

            orig_self_pos = self.orig_position
            orig_neighbor_pos = neighbor.compute_grid_position()
            orig_self_index = self.orig_index
            orig_neighbor_index = neighbor.index

            self.swap_with_neighbor(neighbor_index, animate=True)

            # If no match, revert.
            if not grid.check_for_match():
                self.swap_with_neighbor(neighbor_index, animate=False)
                self.index = orig_self_index
                neighbor.index = orig_neighbor_index
                grid.icons[self.index] = self
                grid.icons[neighbor.index] = neighbor
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
                # Successful swap.
                self.orig_position = self.compute_grid_position()
                self.orig_index = self.index
                neighbor.orig_position = neighbor.compute_grid_position()
                self.is_dragging = False
                neighbor.is_dragging = False
                return True

        def stop_drag(self, animate=False):
            """Stop dragging and snap back to the grid if animate is True."""
            if animate:
                self.snap_to_grid()
            self.is_dragging = False
            self.locked_axis = None
            self.swap_attempted = False
            return self.get_swap_index()

        def get_swap_index(self):
            """
            Return the index of an adjacent neighbor whose center lies inside this tile's bounding box.
            """
            right_index = self.index + 1
            bot_index = self.index + grid.icons_per_row
            left_index = self.index - 1
            top_index = self.index - grid.icons_per_row

            valid_swaps = []
            # Right
            if self.index % grid.icons_per_row < grid.icons_per_row - 1:
                if right_index < grid.grid_size and grid.icons[right_index] is not None and self.is_inside(grid.icons[right_index]):
                    valid_swaps.append(right_index)
            # Bottom
            if bot_index < grid.grid_size and grid.icons[bot_index] is not None and self.is_inside(grid.icons[bot_index]):
                valid_swaps.append(bot_index)
            # Left
            if self.index % grid.icons_per_row > 0:
                if left_index >= 0 and grid.icons[left_index] is not None and self.is_inside(grid.icons[left_index]):
                    valid_swaps.append(left_index)
            # Top
            if top_index >= 0 and grid.icons[top_index] is not None and self.is_inside(grid.icons[top_index]):
                valid_swaps.append(top_index)

            return valid_swaps[0] if valid_swaps else None

        def is_inside(self, neighbor):
            """
            Check whether neighbor's center is within this tile's rectangle.
            """
            center_x = neighbor.x + grid.icon_size / 2
            center_y = neighbor.y + grid.icon_size / 2
            return (self.x <= center_x <= self.x + grid.icon_size and
                    self.y <= center_y <= self.y + grid.icon_size)

        def swap_with_neighbor(self, neighbor_index, animate=False):
            """Swap positions with the neighbor at neighbor_index."""
            neighbor = grid.icons[neighbor_index]
            grid.icons[self.index], grid.icons[neighbor_index] = neighbor, self
            self.x, neighbor.x = neighbor.x, self.x
            self.y, neighbor.y = neighbor.y, self.y
            self.index, neighbor.index = neighbor.index, self.index
            if animate:
                if self.sprite:
                    self.sprite.child = move_anim(self.x, self.y)
                if neighbor.sprite:
                    neighbor.sprite.child = move_anim(neighbor.x, neighbor.y)

        def destroy(self):
            """
            Destroy the icon unless chain_locked is True.
            Locked icons (and their chain overlay) remain indefinitely.
            """
            if self.chain_locked:
                return  # Do nothing; preserve locked icon.
            if self.sprite:
                self.sprite.destroy()
            if self.chain_overlay:
                self.chain_overlay.destroy()
                self.chain_overlay = None
