init python:
    class Icon:
        def __init__(self, index, x, y, icon_type, sprite):
            self.index = index
            self.x = x
            self.y = y
            self.icon_type = icon_type
            self.sprite = sprite

            self.is_dragging = False
            self.locked_axis = None

            self.drag_offset_x = 0
            self.drag_offset_y = 0
            self.original_x = 0
            self.original_y = 0
        
        def start_drag(self, mouse_x, mouse_y):
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
                lock_threshold = 5
                snap_threshold = 50

                if self.locked_axis is None:
                    if abs(dx) >= lock_threshold or abs(dy) >= lock_threshold:
                        self.locked_axis = "x" if abs(dx) >= abs(dy) else "y"
                        
                if self.locked_axis == "x":
                    # Allow horizontal movement only. The direction (positive or negative) follows the mouse.
                    self.x = self.original_x + dx
                    if abs(dx) >= snap_threshold:
                        self.x = self.original_x
                        self.stop_drag()
                elif self.locked_axis == "y":
                    # Allow vertical movement only.
                    self.y = self.original_y + dy
                    if abs(dy) >= snap_threshold:
                        self.y = self.original_y
                        self.stop_drag()

        def stop_drag(self):
            self.is_dragging = False
            self.locked_axis = None

        def destroy(self):
            if self.sprite:
                self.sprite.destroy()