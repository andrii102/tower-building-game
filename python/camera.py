class Camera:
    def __init__(self):
        self.offset_y = 0
        self.target_offset_y = 0
        self.scroll_speed = 4  # Speed of camera scrolling
        self.max_scroll = 0  # This will keep track of the maximum scroll height

    def move(self, dy):
        self.target_offset_y += dy
        # Update the maximum scroll limit based on the tower height
        self.max_scroll = max(self.max_scroll, self.target_offset_y)

    def update(self):
        # Smoothly interpolate the camera offset towards the target
        if self.offset_y < self.target_offset_y:
            self.offset_y += self.scroll_speed
            if self.offset_y > self.target_offset_y:
                self.offset_y = self.target_offset_y
        elif self.offset_y > self.target_offset_y:
            self.offset_y -= self.scroll_speed
            if self.offset_y < self.target_offset_y:
                self.offset_y = self.target_offset_y

        # Debugging output
        #print(f"Camera offset: {self.offset_y}, Target offset: {self.target_offset_y}, Max scroll: {self.max_scroll}")

    def apply(self, obj_rect):
        return obj_rect.move(0, self.offset_y)

    