import os
import pygame
import math

from constants import *

class Render:
    def __init__(self, screen):
        self.screen = screen
        self.offset_height = 0
        self.previous_camera_y = 0
        self.animating = False
        self.angle = 0  # Starting angle
        self.rotation_speed = 0.06
        self.max_angle = 5
        self.direction = 1 
        self.load_assets()
        

    def load_assets(self):
        assets_dir = 'assets/images'
        self.block_image = pygame.image.load(os.path.join(assets_dir, 'block.png')).convert_alpha()
        self.block_perfect_iamge = pygame.image.load(os.path.join(assets_dir, 'block-perfect.png')).convert_alpha()
        self.hook_image = pygame.image.load(os.path.join(assets_dir, 'hook.png')).convert_alpha()
        self.block_rope_image = pygame.image.load(os.path.join(assets_dir, 'block-rope.png')).convert_alpha()
        self.heart_image = pygame.image.load(os.path.join(assets_dir, 'heart.png')).convert_alpha()
        self.score_image = pygame.image.load(os.path.join(assets_dir, 'score.png')).convert_alpha()
        self.background_image = pygame.image.load(os.path.join(assets_dir, 'background-o.png')).convert_alpha()
        self.game_over_bg = pygame.image.load(os.path.join(assets_dir, 'game-over-bg.png')).convert_alpha()
        self.logo = pygame.image.load(os.path.join(assets_dir, 'logo.png')).convert_alpha()

        # Resize images as needed
        self.heart_image = dynamic_resize(self.heart_image, 40, 40)
        self.block_image = dynamic_resize(self.block_image, BWIDTH, BHEIGHT)
        self.block_perfect_iamge = dynamic_resize(self.block_perfect_iamge, BWIDTH, BHEIGHT)
        self.hook_image = dynamic_resize(self.hook_image, new_width=30) # 24
        self.block_rope_image = dynamic_resize(self.block_rope_image, new_width=BWIDTH)
        self.score_image = dynamic_resize(self.score_image, new_width=180)
        self.background_image = dynamic_resize(self.background_image, new_width=WIDTH)
        self.game_over_bg = dynamic_resize(self.game_over_bg, new_width=WIDTH-100, new_height=HEIGHT-100)
        self.logo = dynamic_resize(self.logo, new_width=WIDTH//2-50)
    
        self.logo_rect = self.logo.get_rect(center=(WIDTH // 2, -5))
    
    def draw_background(self, camera):
        color_arr = [
            (200, 255, 150),  # Light yellowish-greenish blue (start)
            (105, 230, 240),  # Light cyan
            (90, 190, 240),   # Light blue
            (85, 100, 190),   # Deep blue
            (45, 35, 105),    # Darker blue
            (25, 20, 55),     # Darker blue, near navy
            (15, 10, 30)]      # Dark blue, near black
        if self.previous_camera_y != camera.offset_y:
            delta_y = self.previous_camera_y - camera.offset_y
            self.previous_camera_y = camera.offset_y
            self.offset_height += -delta_y * 1.1
            self.offset_height = max(0, self.offset_height)

        draw_background_gradient(self.screen, HEIGHT, WIDTH, color_arr, self.offset_height)
        background_rect = pygame.Rect(0, HEIGHT-self.background_image.get_height(), WIDTH, HEIGHT)
        self.screen.blit(self.background_image, camera.apply(background_rect))

    def draw_block(self, block_rect, camera):
            self.screen.blit(self.block_image, camera.apply(block_rect))

    def draw_block_rope(self, block_rect, camera):
            self.screen.blit(self.block_rope_image, camera.apply(block_rect))

    def draw_tower(self, tower, camera):
        for block in tower.blocks[1:]:  # Skip the first block
            block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
            self.screen.blit(self.block_image if not block.perfect else self.block_perfect_iamge, camera.apply(block_rect))

    def draw_hearts_and_score(self, attempts, score):
        self.screen.blit(self.score_image, (WIDTH-self.score_image.get_width()-10, 10))
        self.draw_text(str(score), WIDTH-self.score_image.get_width()+95, 20, font_size=30, font_color=(255, 65, 0))
        for i in range(attempts):
            x_pos = WIDTH - (i + 1) * (self.heart_image.get_width() + 10)
            y_pos = 70  # Top margin
            self.screen.blit(self.heart_image, (x_pos, y_pos))

    def draw_crane(self, crane_x, crane_y, angle, camera):
        rotated_image = pygame.transform.rotate(self.hook_image, angle)
        rotated_rect = rotated_image.get_rect(center=(crane_x, crane_y))

        rotated_rect = camera.apply(rotated_rect)

        self.screen.blit(rotated_image, rotated_rect.topleft)

    def draw_text(self, text, x, y, font_size=36, font_color=(255, 255, 255)):
        font = pygame.font.Font(os.path.join('assets/fonts', 'Fox5.ttf'), font_size) 
        text_surface = font.render(text, True, font_color, None)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def getTextSize(self,text, font_size):
        font = pygame.font.Font(os.path.join('assets/fonts', 'Fox5.ttf'), font_size)
        return font.size(text)

    def draw(self, crane, block, tower, attempts, target_offset_y, crane_y, camera):
        self.screen.fill((200, 200, 200)) 
        self.draw_background(camera)

        if crane.carrying: 
            crane.y=-target_offset_y+crane_y
            self.draw_crane(crane.x, crane.y,math.degrees(crane.angle), camera)
        
        block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
        
        if crane.carrying:   
            crane.updateBlockPosition(block)
            self.draw_block_rope(block_rect, camera)
        elif not self.animating:
            self.draw_block(block_rect,camera)
        # pygame.draw.circle(self.screen, (0, 0, 0), (tower.blocks[tower.height-1].x, tower.blocks[tower.height-1].y+tower.blocks[-1].height), 5)
        self.draw_tower(tower, camera)
        self.draw_hearts_and_score(attempts, tower.score)
        self.draw_text(str(tower.height-1), 25, 20, 72 , (255,65,0))

    def animate_falling_block(self, pivot, block, block_image, crane, tower, attempts,
                             target_offset_y, crane_y, camera, direction=None):
        self.animating = True
        speed = 5
        fps = 60
        clock = pygame.time.Clock()
        angle = 0  # Initial rotation angle
        velocity_y = 0  # Vertical speed (for gravity)
        velocity_x = -speed if direction == "left" else speed  # Horizontal velocity
        rotation_sign = 1 if direction == "left" else -1

        if direction == "right":
            pivot = (pivot[0] + block_image.get_width(), pivot[1])

        falling = True
        while falling:
            self.draw(crane, block, tower, attempts, target_offset_y, crane_y, camera)

            # OFFSET CENTER PIVOT
            # offset = block.x - tower.blocks[tower.height - 1].x
            
            # Rotate the block and apply movement
            rotated_image = pygame.transform.rotate(block_image, angle * rotation_sign)
            # rotated_rect = rotated_image.get_rect(bottom=pivot[1])      #TODO OFFSET
            # rotated_rect.left = pivot[0] - offset
            rotated_rect = rotated_image.get_rect(midbottom=pivot)
            pivot = (pivot[0] + velocity_x, pivot[1] + velocity_y)

            # Apply gravity (adjust vertical velocity)
            velocity_y += 0.5

            # Draw the rotated block
            self.screen.blit(rotated_image, rotated_rect.topleft)
            pygame.display.flip()

            # Check if the block has reached a stopping condition
            if pivot[1] > self.screen.get_height() or pivot[0] < 0 or pivot[0] > self.screen.get_width():
                falling = False  # Stop if out of bounds

            # Update angle and frame rate
            if angle < 90:
                angle += speed
            clock.tick(fps)

        self.animating = False

    def draw_logo(self):
        self.angle += self.direction * self.rotation_speed
        if self.angle > self.max_angle or self.angle < -self.max_angle:
            self.direction *= -1  # Reverse direction at the limits

        rotated_logo = pygame.transform.rotate(self.logo, self.angle)
        rotated_logo_rect = rotated_logo.get_rect(center=self.logo_rect.center)  # Keep center alignment

        self.screen.blit(rotated_logo, rotated_logo_rect.topleft)

   
    def draw_game_over(self):
        print("Game Over!")
        self.screen.blit(self.game_over_bg, (WIDTH/2-self.game_over_bg.get_width()/2, HEIGHT/2-self.game_over_bg.get_height()/2))


def dynamic_resize(image,new_width=None, new_height=None):
     if new_width is not None and new_height is not None:
        return pygame.transform.scale(image, (new_width, new_height))
     elif new_width is not None:
        aspect_ratio = image.get_height() / image.get_width()
        new_height = int(new_width * aspect_ratio)
        return pygame.transform.scale(image, (new_width, new_height))
     elif new_height is not None:
        aspect_ratio = image.get_width() / image.get_height()
        new_width = int(new_height * aspect_ratio)
        return pygame.transform.scale(image, (new_width, HEIGHT))
     else:
        return image
     

def get_linear_gradient_color_rgb(color_arr, color_index, proportion):
    current_index = min(color_index, len(color_arr) - 1)
    color_current = color_arr[current_index]
    next_index = min(current_index + 1, len(color_arr) - 1)
    color_next = color_arr[next_index]
    
    def calculate_rgb_value(index):
        current = color_current[index]
        next = color_next[index]
        return round(current + ((next - current) * proportion))
    
    return (
        calculate_rgb_value(0),  # Red
        calculate_rgb_value(1),  # Green
        calculate_rgb_value(2),  # Blue
    )


def draw_background_gradient(screen, height, width, color_arr, offset_height):
    gradient_height = height
    color_index = int(offset_height // gradient_height)
    cal_offset_height = offset_height % gradient_height
    proportion = cal_offset_height / gradient_height

    # Get the two colors to blend
    color_base = get_linear_gradient_color_rgb(color_arr, color_index, proportion)
    color_top = get_linear_gradient_color_rgb(color_arr, color_index + 1, proportion)

    # Draw the gradient
    for y in range(height):
        t = y / height  # Interpolation factor for this line
        interpolated_color = (
            int(color_top[0] * (1 - t) + color_base[0] * t),
            int(color_top[1] * (1 - t) + color_base[1] * t),
            int(color_top[2] * (1 - t) + color_base[2] * t),
        )
        pygame.draw.line(screen, interpolated_color, (0, y), (width, y))
