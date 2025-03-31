init python:
    class GridManager:
        def __init__(self, icons_per_row, grid_size):
            self.icons = []
            self.sprite_manager = None
            self.icon_size = 100
            self.icon_padding = 10
            self.icons_per_row = icons_per_row
            self.grid_size = grid_size
            self.icon_images = ["brick", "glass", "rocks", "steel", "wood"]

        def has_initial_match(self):
            # For every icon in the grid, use the flood-fill method to get the connected group.
            for index, icon in enumerate(self.icons):
                if icon is not None:
                    if len(self.get_cluster(index)) >= 3:
                        return True
            return False

        def initialize_grid(self):
            valid_grid = False
            # Keep regenerating until no match is found.
            while not valid_grid:
                self.icons = [None] * self.grid_size
                for index in range(self.grid_size):
                    # Calculate grid position.
                    col = index % self.icons_per_row
                    row = index // self.icons_per_row
                    x = col * (self.icon_size + self.icon_padding)
                    y = row * (self.icon_size + self.icon_padding)
                    
                    allowed_types = self.icon_images[:]  # Start with all types allowed.
                    valid = False
                    # Try candidates until one does not cause a local cluster.
                    while not valid and allowed_types:
                        tile_type = renpy.random.choice(allowed_types)
                        temp_icon = Icon(index=index, x=x, y=y, icon_type=tile_type, sprite=None)
                        self.icons[index] = temp_icon
                        # Use your flood-fill helper to check the connected group.
                        cluster = self.get_cluster(index)
                        if len(cluster) < 3:
                            valid = True
                        else:
                            allowed_types.remove(tile_type)
                    if not valid:
                        # Fallback (should rarely happen with several types available).
                        tile_type = renpy.random.choice(self.icon_images)
                        self.icons[index] = Icon(index=index, x=x, y=y, icon_type=tile_type, sprite=None)
                # After the full grid is built, check for any horizontal or vertical matches.
                if not self.has_initial_match():
                    valid_grid = True

        def get_cluster(self, index):
            # Flood fill to collect all connected cells with the same icon_type.
            start_icon = self.icons[index]
            if start_icon is None:
                return []
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
                # Left neighbor.
                if col > 0:
                    neighbors.append(cur - 1)
                # Right neighbor.
                if col < self.icons_per_row - 1:
                    neighbors.append(cur + 1)
                # Top neighbor.
                if row > 0:
                    neighbors.append(cur - self.icons_per_row)
                # Bottom neighbor.
                if row < (self.grid_size // self.icons_per_row) - 1:
                    neighbors.append(cur + self.icons_per_row)
                for n in neighbors:
                    if self.icons[n] is not None and self.icons[n].icon_type == start_icon.icon_type and n not in cluster:
                        to_check.append(n)
            return list(cluster)
        
        def create_sprite_manager(self):
            self.sprite_manager = SpriteManager(update=self.update_icon, event=self.handle_event)
            return self.sprite_manager
        
        def update_icon(self, st):
            for icon in self.icons:
                if icon and icon.sprite:
                    icon.sprite.x = icon.x
                    icon.sprite.y = icon.y
            return 0  # Required for Ren'Py SpriteManager
        
        def handle_event(self, event, x, y, st):
            self.shift_icons(mouse_event=False)
            game.find_match(mouse_event=False)
            
            if event.type == 1024:
                for icon in self.icons:
                    if icon and icon.is_dragging:
                        icon.update_drag(x, y)

            if event.type == 1025 and event.button == 1:
                for icon in self.icons:
                    if icon and icon.x <= x <= (icon.x + self.icon_size) and icon.y <= y <= (icon.y + self.icon_size):
                        icon.start_drag(x, y)
                        break

            if event.type == 1026 and event.button == 1:
                for icon in self.icons:
                    if icon and icon.x <= x <= (icon.x + self.icon_size) and icon.y <= y <= (icon.y + self.icon_size) and icon.is_dragging:
                        icon.stop_drag()
                        break
        
        def shift_icons(self, mouse_event):
            # Shift left/right
            for i in range(self.grid_size - self.icons_per_row):
                if self.icons[i]:
                    col = i % self.icons_per_row
                    row = i // self.icons_per_row
                    bottom_left = i + self.icons_per_row - 1 if col > 0 else None
                    bottom_right = i + self.icons_per_row + 1 if col < self.icons_per_row - 1 else None
                    
                    can_shift_left = bottom_left and not self.icons[bottom_left]
                    can_shift_right = bottom_right and not self.icons[bottom_right]
                    
                    if can_shift_left or can_shift_right:
                        direction = renpy.random.randint(0, 1) if can_shift_left and can_shift_right else 0 if can_shift_left else 1
                        
                        if direction == 0:
                            self.icons[bottom_left] = self.icons[i]
                            self.icons[i] = None
                            self.icons[bottom_left].x -= (self.icon_size + self.icon_padding)
                            self.icons[bottom_left].y += (self.icon_size + self.icon_padding)
                            self.icons[bottom_left].index = bottom_left
                        else:
                            self.icons[bottom_right] = self.icons[i]
                            self.icons[i] = None
                            self.icons[bottom_right].x += (self.icon_size + self.icon_padding)
                            self.icons[bottom_right].y += (self.icon_size + self.icon_padding)
                            self.icons[bottom_right].index = bottom_right

            # Shift down
            for i in range(self.grid_size - 1, self.icons_per_row - 1, -1):
                if not self.icons[i]:
                    row = i // self.icons_per_row
                    col = i % self.icons_per_row
                    row_mult = 1
                    source_index = i - (self.icons_per_row * row_mult)
                    
                    while source_index >= 0 and not self.icons[source_index]:
                        row_mult += 1
                        source_index = i - (self.icons_per_row * row_mult)
                    
                    if source_index >= 0 and self.icons[source_index]:
                        self.icons[i] = self.icons[source_index]
                        self.icons[source_index] = None
                        self.icons[i].y += (self.icon_size + self.icon_padding) * row_mult
                        self.icons[i].index = i

            if mouse_event:
                pass
                # game.decrement_moves()
            
            self.sprite_manager.redraw(0)
            renpy.show_screen("Score_UI")
            renpy.retain_after_load()
        
        def refill_grid(self):
            # Iterate over every cell in reading order.
            for i in range(self.grid_size):
                if self.icons[i] is None:
                    # Determine the cell's row and column.
                    col = i % self.icons_per_row
                    row = i // self.icons_per_row
                    x = col * (self.icon_size + self.icon_padding)
                    y = row * (self.icon_size + self.icon_padding)
                    
                    # Start with all available tile types.
                    allowed = self.icon_images[:]  
                    
                    # Check horizontally: if there are two filled cells to the left.
                    if col >= 2:
                        left1 = self.icons[i - 1]
                        left2 = self.icons[i - 2]
                        if left1 is not None and left2 is not None:
                            if left1.icon_type == left2.icon_type:
                                forbidden = left1.icon_type
                                if forbidden in allowed:
                                    allowed.remove(forbidden)
                    
                    # Check vertically: if there are two filled cells above.
                    if row >= 2:
                        above1 = self.icons[i - self.icons_per_row]
                        above2 = self.icons[i - 2 * self.icons_per_row]
                        if above1 is not None and above2 is not None:
                            if above1.icon_type == above2.icon_type:
                                forbidden = above1.icon_type
                                if forbidden in allowed:
                                    allowed.remove(forbidden)
                    
                    # Choose a candidate tile type from allowed types.
                    if not allowed:
                        candidate = renpy.random.choice(self.icon_images)
                    else:
                        candidate = renpy.random.choice(allowed)
                    
                    # Create the new sprite for this tile.
                    idle_image = Image("Icons/{}.png".format(candidate))
                    new_sprite = self.sprite_manager.create(Transform(child=idle_image, zoom=0.08))
                    # For refill, spawn the new tile above the visible grid so it drops in.
                    new_sprite.x = x
                    new_sprite.y = - (self.icon_size + self.icon_padding)
                    
                    # Finally, assign the new Icon to the grid.
                    self.icons[i] = Icon(index=i, x=x, y=y, icon_type=candidate, sprite=new_sprite)


        def clear_grid(self):
            renpy.hide_screen("result", immediately=True)
            game.score = 0
            for icon in self.icons:
                if icon:
                    icon.destroy()
            self.icons.clear()
            self.sprite_manager.redraw(0)

        def check_for_match(self):
            # Determine the number of rows.
            rows = self.grid_size // self.icons_per_row
            # Check for horizontal matches.
            for row in range(rows):
                for col in range(self.icons_per_row - 2):  # need at least 3 in a row
                    index = row * self.icons_per_row + col
                    if self.icons[index] is not None:
                        icon_type = self.icons[index].icon_type
                        if (self.icons[index + 1] is not None and self.icons[index + 1].icon_type == icon_type and
                            self.icons[index + 2] is not None and self.icons[index + 2].icon_type == icon_type):
                            return True
            # Check for vertical matches.
            for col in range(self.icons_per_row):
                for row in range(rows - 2):  # need at least 3 in a column
                    index = row * self.icons_per_row + col
                    if self.icons[index] is not None:
                        icon_type = self.icons[index].icon_type
                        if (self.icons[index + self.icons_per_row] is not None and self.icons[index + self.icons_per_row].icon_type == icon_type and
                            self.icons[index + 2 * self.icons_per_row] is not None and self.icons[index + 2 * self.icons_per_row].icon_type == icon_type):
                            return True
            return False

