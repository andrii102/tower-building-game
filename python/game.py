import sys

sys.path.append('../build/Debug')

import pygame
import physics 
from camera import Camera
from render import Render
from constants import *
from button import *
from SoundEffects import SoundEffects

def manageAttempts(attempts, running):
    attempts -= 1
    print("Attempts failed: ", attempts)
    if attempts <= 0:
        running[0] = False
    return attempts

def cranePickUpBlock(crane, target_offset_y):
    block = physics.Block(230, 50-target_offset_y, BWIDTH, BHEIGHT) # x, y, width, height
    crane.pickUpBlock(block)
    return block

def game(screen):
    clock = pygame.time.Clock()

    camera = Camera()

    target_offset_y = 0
    camera.move(200)

    crane_x, crane_y = WIDTH//2, -400

    tower = physics.Tower()
    crane = physics.Crane(crane_x, crane_y, 328) # crane.length = hook_image / 2 - 5

    render=Render(screen)
    sound = SoundEffects()

    #Variables for Failed attempts
    attempts = 3

    running = [True]
    block = cranePickUpBlock(crane, target_offset_y)
    sound.play_background()
    
    while running[0]:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = [False]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Drop")
                    crane.dropBlock()

        if crane.carrying: 
            crane.update(clock.get_time() / 1000.0)
        
        if not crane.carrying:
            block.updateFallSpeed()
            if block.checkCollision(block, tower.blocks[tower.height - 1]):
                print("Collision!")
                stable, direction = block.isBlockStable(block, tower.blocks[tower.height - 1])
                if not stable:
                    print("Block is unstable!") 
                    sound.play('rotate')
                    render.animate_falling_block((tower.blocks[-1].x, tower.blocks[-1].y+target_offset_y+200),
                                            block, render.block_image, crane, tower, attempts, 
                                             target_offset_y, crane_y, camera, direction)
                    attempts = manageAttempts(attempts, running)
                    block = cranePickUpBlock(crane, target_offset_y)
                    continue
                sound.play('drop-perfect' if block.perfect else 'drop')
                tower.addBlock(block)
                crane.modifyVelocityMaxAngle(0.08, 0.015)
                
                if tower.height == 2:
                    camera.move(scroll_step+120)
                    target_offset_y += scroll_step+120
                else:
                    camera.move(scroll_step)
                    target_offset_y += scroll_step 
                block = cranePickUpBlock(crane, target_offset_y)
                continue
            if block.y > HEIGHT-target_offset_y:
                print("Miss!")
                attempts = manageAttempts(attempts, running)
                block = cranePickUpBlock(crane, target_offset_y)
                continue

        camera.update()
        render.draw(crane, block, tower,attempts, target_offset_y, crane_y, camera)
        pygame.display.flip()
        clock.tick(60)  # Frame rate
    sound.stop_background()
    sound.play('game-over')
    game_over(screen, render, tower.score)


def game_over(screen, render, score):
    clock = pygame.time.Clock()
    render.draw_game_over()
    game_over_score_image = pygame.image.load(GAME_OVER_SCORE_IMG).convert_alpha()
    game_over_score=dynamic_resize(game_over_score_image, new_width=300)
    replay_image = pygame.image.load(REPLAY_BUTTON_IMG).convert_alpha()
    leaderboard_img = pygame.image.load(LEADERBOARD_BUTTON_IMG).convert_alpha()
    more_games_img = pygame.image.load(MORE_GAMES_BUTTON_IMG).convert_alpha()
    replay_button = Button(replay_image, WIDTH // 2 - 165, HEIGHT // 2 - 20, width=330)
    leaderboard_button = Button(leaderboard_img, WIDTH // 2 - 165, HEIGHT // 2 + 90, width=330)
    more_games_button = Button(more_games_img, WIDTH // 2 - 165, HEIGHT // 2 + 2*100, width=330)

    game_over_running = True
    while game_over_running:
        screen.blit(game_over_score, (WIDTH // 2 - 150, 130))
        render.draw_text(str(score), WIDTH // 2 - render.getTextSize(str(score), 72)[0]//2, 250, 72, (255, 130, 90))
        replay_button.draw(screen)
        leaderboard_button.draw(screen)
        more_games_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.is_clicked(event.pos):
                    print("Replay button clicked!")
                    game(screen)
                    game_over_running = False
                elif leaderboard_button.is_clicked(event.pos):
                    print("Leaderboard button clicked!")
                    game_over_running = False
                elif more_games_button.is_clicked(event.pos):
                    print("More games button clicked!")
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()
        clock.tick(60)
    

def menu(screen):
    clock = pygame.time.Clock()
    render=Render(screen)
    camera=Camera()

    # Load Button Images
    start_img = pygame.image.load(START_BUTTON_IMG).convert_alpha() 
    leaderboard_img = pygame.image.load(LEADERBOARD_BUTTON_IMG).convert_alpha()
    more_games_img = pygame.image.load(MORE_GAMES_BUTTON_IMG).convert_alpha()
    
    # Create Buttons (x, y, scale)
    start_button = Button(start_img, WIDTH // 2 - 165 , HEIGHT // 2, width=330)
    leaderboard_button = Button(leaderboard_img, WIDTH // 2 - 165, HEIGHT // 2 + 120, width=330)
    more_games_button = Button(more_games_img, WIDTH // 2 - 165, HEIGHT // 2 + 2*120, width=330)

    menu_running = True
    while menu_running:
        render.draw_background(camera)
        render.draw_logo()
        start_button.draw(screen)
        leaderboard_button.draw(screen)
        more_games_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    print("Start Game!")
                    game(screen)
                    menu_running = False
                elif leaderboard_button.is_clicked(event.pos):
                    print("Leaderboard button clicked!")
                    # Placeholder
                elif more_games_button.is_clicked(event.pos):
                    print("More games button clicked!")
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    menu(screen)
    pygame.quit()

main()

#   TODO 
#   1. Make crane more dynamic   
#   2. Background effects
