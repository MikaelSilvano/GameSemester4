init python:
    import random  

    class GridManager:
        def __init__(self, icons_per_row, grid_size):
            self.icons = []
            self.sprite_manager = None
            self.icon_size = 100
            self.icon_padding = 10
            self.icons_per_row = icons_per_row
            self.grid_size = grid_size
            self.icon_images = icon_image_use
            self.fixed_positions = None

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
            global grid
            grid = self

        def get_cluster(self, index):
            start_icon = self.icons[index]
            if start_icon is None:
                return []
            if start_icon.chain_locked:
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

        def handle_event(self, event, x, y, st):
            self.shift_icons(mouse_event=False)
            game.find_match(mouse_event=False)
            
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
                        if game.level == 3:
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
                            elif game.level == 4:
                                icon_skill_collected.append(icon.index)
                                if len(icon_skill_collected) == required_targets:
                                    skill.masterpiece_build(icon_skill_collected[0])
                                    store.time_countdown_left = 20
                                    store.non_violatable_time = 20
                                    store.icon_skill_collected.clear()
                                    renpy.show_screen("countdown")
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
            for i in range(self.grid_size - self.icons_per_row):
                if self.icons[i] and self.icons[i].chain_locked:
                    continue

                if self.icons[i]:
                    col = i % self.icons_per_row
                    row = i // self.icons_per_row
                    bottom_left = i + self.icons_per_row - 1 if col > 0 else None
                    bottom_right = i + self.icons_per_row + 1 if col < self.icons_per_row - 1 else None

                    def can_shift(target_index):
                        if target_index is None or target_index < 0 or target_index >= self.grid_size:
                            return False
                        if self.icons[target_index] is not None:
                            return False
                        if self.fixed_positions and ((target_index % self.icons_per_row),
                                                    (target_index // self.icons_per_row)) in self.fixed_positions:
                            return False
                        return True

                    shift_left = can_shift(bottom_left)
                    shift_right = can_shift(bottom_right)

                    if shift_left or shift_right:
                        direction = renpy.random.randint(0, 1) if (shift_left and shift_right) else (0 if shift_left else 1)
                        if direction == 0 and bottom_left is not None:
                            self.icons[bottom_left] = self.icons[i]
                            self.icons[i] = None
                            self.icons[bottom_left].x -= (self.icon_size + self.icon_padding)
                            self.icons[bottom_left].y += (self.icon_size + self.icon_padding)
                            self.icons[bottom_left].index = bottom_left
                        elif direction == 1 and bottom_right is not None:
                            self.icons[bottom_right] = self.icons[i]
                            self.icons[i] = None
                            self.icons[bottom_right].x += (self.icon_size + self.icon_padding)
                            self.icons[bottom_right].y += (self.icon_size + self.icon_padding)
                            self.icons[bottom_right].index = bottom_right

            for i in range(self.grid_size - 1, self.icons_per_row - 1, -1):
                if not self.icons[i]:
                    col = i % self.icons_per_row
                    row = i // self.icons_per_row
                    if self.fixed_positions and (col, row) in self.fixed_positions:
                        continue

                    row_mult = 1
                    source_index = i - (self.icons_per_row * row_mult)
                    while source_index >= 0 and not self.icons[source_index]:
                        row_mult += 1
                        source_index = i - (self.icons_per_row * row_mult)
                    if source_index >= 0 and self.icons[source_index]:
                        if self.icons[source_index].chain_locked:
                            continue
                        self.icons[i] = self.icons[source_index]
                        self.icons[source_index] = None
                        self.icons[i].y += (self.icon_size + self.icon_padding) * row_mult
                        self.icons[i].index = i

            if mouse_event:
                pass

        def refill_grid(self):
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
