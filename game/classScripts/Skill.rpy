init python:
    class Skills_list:
        def __init__(self):
            self.forced_compression_used = False
            self.masterpiece_build_skill_used = False

        def forced_compression(self):
            rows = grid.grid_size // grid.icons_per_row
            center_row = rows // 2 
            start_index = center_row * grid.icons_per_row
            end_index = start_index + grid.icons_per_row

            for i in range(start_index, end_index):
                tile = grid.icons[i]
                if tile is not None:
                    if tile.sprite:
                        tile.sprite.child = crush_anim
                    tile.destroy()  
                    grid.icons[i] = None

            self.forced_compression_used = True

            grid.shift_icons(mouse_event=True)
            grid.refill_grid()

        def blueprint_swap(self, index1, index2):
            if 0 <= index1 < len(grid.icons) and 0 <= index2 < len(grid.icons):
                grid.icons[index1], grid.icons[index2] = grid.icons[index2], grid.icons[index1]
                grid.icons[index1].index, grid.icons[index2].index = index1, index2
                icon.start_drag(icon.x, icon.y)

        def masterpiece_build(self, center_index):
            icons_per_row = grid.icons_per_row
            total_rows = grid.grid_size // icons_per_row
            center_row = center_index // icons_per_row
            center_col = center_index % icons_per_row

            if center_row < 1 or center_col < 1 or center_row > total_rows - 2 or center_col > icons_per_row - 2:
                renpy.notify("Cannot use Masterpiece here — not enough space around the tile.")
                return

            for r in range(center_row - 1, center_row + 2):
                for c in range(center_col - 1, center_col + 2):
                    index = r * icons_per_row + c
                    if 0 <= index < len(grid.icons):
                        tile = grid.icons[index]
                        if tile:
                            if grid.fixed_positions and (c, r) in grid.fixed_positions:
                                grid.fixed_positions.remove((c, r))
                                tile.chain_locked = False
                                if tile.chain_overlay:
                                    tile.chain_overlay.destroy()
                                    tile.chain_overlay = None

                            if tile.sprite:
                                tile.sprite.child = crush_anim
                            tile.destroy()
                            grid.icons[index] = None

            self.masterpiece_used = True
            grid.shift_icons(mouse_event=True)
            grid.refill_grid()
            self.masterpiece_build_skill_used = True


