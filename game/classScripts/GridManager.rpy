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
            game.find_match()
            
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
                    if icon and icon.x <= x <= (icon.x + self.icon_size) and icon.y <= y <= (icon.y + self.icon_size):
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


            # Refill grid
            for i in range(self.icons_per_row):
                if self.icons[i] is None:
                    rand_image = self.icon_images[renpy.random.randint(0, 4)]
                    idle_image = Image("Icons/{}.png".format(rand_image))
                    new_sprite = self.sprite_manager.create(Transform(child=idle_image, zoom=0.08))
                    
                    col = i % self.icons_per_row
                    xp = (self.icon_size * col) + (self.icon_padding * col)

                    new_sprite.x = xp
                    new_sprite.y = - (self.icon_size + self.icon_padding)

                    self.icons[i] = Icon(
                        index=i,
                        x=xp,
                        y=0,
                        icon_type=rand_image,
                        sprite=new_sprite
                    )

            if mouse_event:
                pass
                # game.decrement_moves()
            
            self.sprite_manager.redraw(0)
            renpy.show_screen("Score_UI")
            renpy.retain_after_load()
                        
        def clear_grid(self):
            renpy.hide_screen("result", immediately=True)
            game.score = 0
            game.moves = 10
            for icon in self.icons:
                if icon:
                    icon.destroy()
            self.icons.clear()
            self.sprite_manager.redraw(0)