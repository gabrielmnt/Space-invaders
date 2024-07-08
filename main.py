import time
import pygame
import random

pygame.init()
# font
font = pygame.font.SysFont('Courier New', 50)
font.render('Courier New', True, (255, 255, 255))
print(pygame.font.get_fonts())

# sounds
bullet_snd = pygame.mixer.Sound("midia/shoot.mp3.")
bullet_snd.set_volume(0.05)
hit_snd = pygame.mixer.Sound("midia/hit.mp3.wav")
hit_snd.set_volume(0.05)
game_over_snd = pygame.mixer.Sound("midia/gameover.mp3.wav")
game_over_snd.set_volume(0.05)

# screen
screen_x = 1280
screen_y = 720
initial_screen = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
surface = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Space invader")
menu_screen = pygame.image.load('midia/Space INvaders.png')
menu_screen = pygame.transform.scale(menu_screen, (screen_x - 360, screen_y))

# player
player = pygame.image.load('midia/space.user.png')
player = pygame.transform.scale(player, (55, 60))
player_rect = player.get_rect()
player_rect.topleft = (570, 640)
vel = 6
life = 3

# player bullet
bullets = []
bullet_w = 3
bullet_h = 10
bullet_color = (255, 0, 0)
bullet_speed = 8
bullet_cdw = 700
last_bullet_time = pygame.time.get_ticks()
bullets_to_remove = []

# enemy
enemy = pygame.image.load('midia/enemy.png')
enemy = pygame.transform.scale(enemy, (40, 40))
enemy1 = pygame.image.load('midia/enemy1.png')
enemy1 = pygame.transform.scale(enemy1, (40, 40))
enemy2 = pygame.image.load('midia/enemy2.png')
enemy2 = pygame.transform.scale(enemy2, (40, 40))
enemy_types = [enemy2, enemy, enemy, enemy1, enemy1]
enemy_x = enemy.get_width() + 10
enemy_y = enemy.get_height() + 10
enemy_vel = .5
e_space_x = 5
e_space_y = 5
num_c = 18
num_l = 5
first_enemy_y = 70
pos_x = [i * (enemy_x + e_space_x) for i in range(num_c) for j in range(num_l)]
pos_y = [first_enemy_y + j * (enemy_y + e_space_y) for i in range(num_c) for j in range(num_l)]
direction = [1] * (num_c * num_l)
enemy_images = [enemy_types[j % len(enemy_types)] for i in range(num_c) for j in range(num_l)]
enemies_to_remove = []

# enemy bullet
enemy_blt = []
enemy_blt_w = 3
enemy_blt_h = 10
enemy_blt_color = (255, 255, 255)
enemy_blt_speed = 8
enemy_blt_cdw = 1000
enemy_last_blt_time = pygame.time.get_ticks()

# nav bonus
bonus_nav = pygame.image.load('midia/bonusnav.png')
bonus_nav = pygame.transform.scale(bonus_nav, (50, 40))
x_navb = -50
y_navb = 60
bonus_nav_vel = 4
bonus_nav_appeared = False

# general game
score = 0
p_cdw = 500
initial_time = pygame.time.get_ticks()
initial_time_navb = pygame.time.get_ticks()
pause = False
win = False
defeat = False
initial_game = False
start_game = True
reset_game = True
main_menu = True
quit_game = True
bullet = True
event = True
navb_drw = True
enemies_destroyed = 0

# Score and lifes
lives_txt = font.render(f'VIDAS 00{life}', True, (255, 255, 255))
score_txt = font.render(f'SCORE 00{score}', True, (255, 255, 255))
pause_txt = font.render('Press "ESC" to unpause', True, (255, 255, 255))
end_txt = font.render('CONGRATULATIONS,You won!!', True, (255, 255, 255))
defeat_txt = font.render('You Lost! Would you like to try again?', True, (255, 255, 255))


def draw_initial():
    press_screen = pygame.draw.rect(screen, (0, 0, 0), [0, 0, screen_x, screen_y])
    screen.blit(menu_screen, (180, 0))
    return press_screen


def draw_pause():
    global reset_game, main_menu, quit_game
    pygame.mouse.set_visible(True)

    pygame.draw.rect(surface, (255, 255, 255, 10), [0, 0, screen_x, screen_y])
    pygame.draw.rect(surface, (120, 255, 120, 20), [435, 240, 400, 300], 0, 30)
    pygame.draw.rect(surface, (126, 217, 87, 99), [0, 50, screen_x, 55], 0, 00)
    reset_game = pygame.draw.rect(surface, (126, 217, 87, 99), [520, 290, 220, 50], 0, 10)
    main_menu = pygame.draw.rect(surface, (126, 217, 87, 99), [520, 365, 220, 50], 0, 10)
    quit_game = pygame.draw.rect(surface, (126, 217, 87, 99), [520, 440, 220, 50], 0, 10)
    surface.blit(font.render('RESTART', True, (255, 255, 255)), (525, 290))
    surface.blit(font.render('MENU', True, (255, 255, 255)), (570, 365))
    surface.blit(font.render('QUIT', True, (255, 255, 255)), (570, 440))
    screen.blit(surface, (0, 0))
    if not win and not defeat and not initial_game:
        screen.blit(pause_txt, (screen_x / 4, screen_y - screen_y + 50))
    return reset_game, quit_game, main_menu


def draw_end():
    pygame.mouse.set_visible(True)
    if not initial_game:
        screen.blit(end_txt, (screen_x / 4, screen_y - screen_y + 50))


def draw_defeat():
    pygame.mouse.set_visible(True)
    if not initial_game:
        screen.blit(defeat_txt, (70, screen_y - screen_y + 50))


# game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.mouse.set_visible(False)
    screen.fill((0, 0, 0))

    # commands
    commands = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    # pause button
    if current_time - initial_time > p_cdw:
        if commands[pygame.K_ESCAPE]:
            initial_time = current_time
            if pause:
                pause = False
            else:
                pause = True
    # draw pause and its functions
    if pause:
        reset_game, quit_game, main_menu, = draw_pause()
        if initial_game:
            draw_initial()

    # pause game when start the loop
    if start_game:
        pause = True
        initial_game = True

    # pause if defeat
    if defeat:
        pause = True

    # lr and shoot player commands
    if (commands[pygame.K_a] and player_rect.left > 0 or
            commands[pygame.K_LEFT] and player_rect.left > 0) and not pause:
        player_rect.x -= vel

    elif (commands[pygame.K_d] and player_rect.right < screen_x
          or commands[pygame.K_RIGHT] and player_rect.right < screen_x) and not pause:
        player_rect.x += vel

    if commands[pygame.K_w] or commands[pygame.K_UP]:
        current_time = pygame.time.get_ticks()

        # bullet initial pos, cdw and sound
        if current_time - last_bullet_time > bullet_cdw and not pause:
            bullet = pygame.Rect(player_rect.centerx - bullet_w // 2, player_rect.top, bullet_w, bullet_h)
            bullets.append(bullet)
            last_bullet_time = current_time
            pygame.mixer.Sound.play(bullet_snd)
            pygame.mixer.music.stop()

    if event.type == pygame.MOUSEBUTTONDOWN and pause:
        # collision with reset button and default values to restart or start game
        if (event.button == 1 and reset_game.collidepoint(event.pos) and not initial_game) or (
                initial_game and event.button == 1):
            # player
            player_rect.topleft = (570, 640)
            vel = 6
            if bullets:
                bullet.y = 0

            # enemy
            e_space_y = 5
            num_c = 18
            num_l = 5
            first_enemy_y = 70
            enemy_vel = .5
            pos_x = [i * (enemy_x + e_space_x) for i in range(num_c) for j in range(num_l)]
            pos_y = [first_enemy_y + j * (enemy_y + e_space_y) for i in range(num_c) for j in range(num_l)]
            direction = [1] * (num_c * num_l)

            # nav bonus
            enemies_destroyed = 0

            # score and lives
            life = 3
            lives_txt = font.render(f'VIDAS 00{life}', True, (255, 255, 255))
            score = 0
            score_txt = font.render(f'SCORE 00{score}', True, (255, 255, 255))

            # general game
            defeat = False
            reset_game = True
            pause = False
            initial_game = False
            start_game = False
            time.sleep(.3)
            x_navb = screen_x + 50
            enemy_images = [enemy_types[j % len(enemy_types)] for i in range(num_c) for j in range(num_l)]

        # quit button collision
        if event.button == 1 and quit_game.collidepoint(event.pos) and not initial_game:
            running = False

        # menu button collision
        if event.button == 1 and main_menu.collidepoint(event.pos):
            pygame.mouse.set_pos(300, 500)
            pause = True
            initial_game = True

    # lists for the objects to remove
    bullets_to_remove = []
    enemies_to_remove = []

    # cooldown enemy bullet
    current_time_navb = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    if current_time - enemy_last_blt_time > enemy_blt_cdw and not pause:
        # enemy who will shoot
        if pos_x:
            random_enemy_index = random.randint(0, len(pos_x) - 1)

            # create enemy shot and add to removal list
            enemy_bullet = pygame.Rect(pos_x[random_enemy_index] + enemy_x // 2 - enemy_blt_w // 2,
                                       pos_y[random_enemy_index] + enemy_y, enemy_blt_w, enemy_blt_h)
            enemy_blt.append(enemy_bullet)
            enemy_last_blt_time = current_time

    # draw enemy shot and define their moves
    for enemy_bullet in enemy_blt:
        if not pause:
            pygame.draw.rect(screen, enemy_blt_color, enemy_bullet)
        enemy_bullet.y += enemy_blt_speed
        if pause:
            enemy_bullet.y -= enemy_blt_speed
        # remove enemy shot from off-screen
        if enemy_bullet.y > screen_y:
            enemy_blt.remove(enemy_bullet)
        # remove shot after restart
        if reset_game:
            enemy_blt.remove(enemy_bullet)
            reset_game = False

        # collision with player
        if enemy_bullet.colliderect(player_rect):
            enemy_blt.remove(enemy_bullet)
            pygame.mixer.Sound.play(game_over_snd)
            pygame.mixer.music.stop()
            life -= 1
            lives_txt = font.render(f'VIDAS 00{life}', True, (255, 255, 255))
            time.sleep(2)
            if life == 0:
                defeat = True
                if reset_game:
                    defeat = False

    # draw and bullet trajectory
    for bullet in bullets:
        if not pause:
            pygame.draw.rect(screen, bullet_color, bullet)
        bullet.y -= bullet_speed
        if pause:
            bullet.y += bullet_speed
        # remove player shot from off-screen
        if bullet.y < 0:
            bullets.remove(bullet)

        # collision of the player's shot with the enemy
        for i in range(len(pos_x)):
            enemy_rect = pygame.Rect(pos_x[i], pos_y[i], enemy_x, enemy_y)
            if bullet.colliderect(enemy_rect):
                score += 5
                bullets_to_remove.append(bullet)
                enemies_to_remove.append(i)
                pygame.mixer.Sound.play(hit_snd)
                pygame.mixer.music.stop()
                enemy_vel += 0.05  # more speed to enemy when player bullet colliding with an enemy
            if pos_x and pos_y == 0:
                draw_end()

        # bonus ship collision
        if bullet.colliderect(navb_drw):
            bullets_to_remove.append(bullet)
            enemy_vel -= 0.20  # slows down enemy when navb is hit           
            score += 40
            pygame.mixer.Sound.play(hit_snd)
            pygame.mixer.music.stop()
            x_navb = screen_x + 50
            if life <= 3:
                life += 1
            # score
            initial_time_navb = pygame.time.get_ticks()
            lives_txt = font.render(f'VIDAS 00{life}', True, (255, 255, 255))
        score_txt = font.render(f'SCORE 00{score}', True, (255, 255, 255))
        if score >= 100:
            score_txt = font.render(f'SCORE 0{score}', True, (255, 255, 255))
            if score >= 1000:
                score_txt = font.render(f'SCORE {score}', True, (255, 255, 255))

    # remove bullets
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    # remove collided enemy
    for index in reversed(enemies_to_remove):
        pos_x.pop(index)
        pos_y.pop(index)
        enemy_images.pop(index)
        enemies_destroyed += 1  # bonus ship appearance calculation
        if enemies_destroyed % 15 == 0:
            bonus_nav_appeared = True
            x_navb = -50

    # enemy collision with player
    for i in range(len(pos_x)):
        enemy_rect = pygame.Rect(pos_x[i], pos_y[i], enemy_x, enemy_y)
        if player_rect.colliderect(enemy_rect):
            life -= 1
            if life == 0:
                defeat = True
                if reset_game:
                    defeat = False

    #  hit the edge and go back in the opposite direction
    if any(pos_x[i] < 0 or pos_x[i] > screen_x - enemy_x for i in range(len(pos_x))):
        for i in range(len(pos_x)):
            direction[i] *= -1
            pos_y[i] += 10
    # draw enemies and movements
    for i in range(len(pos_x)):
        if not pause:
            screen.blit(enemy_images[i], (pos_x[i], pos_y[i]))
        pos_x[i] += direction[i] * enemy_vel  # velocity of enemy's
        if pause:
            pos_x[i] -= direction[i] * enemy_vel  # stop enemies when game paused

    # bonus nav/ action time and moves
    if bonus_nav_appeared:
        if not pause:
            x_navb += bonus_nav_vel
        # Check if bonus nav is off-screen and reset
        if x_navb >= screen_x + 50:
            bonus_nav_appeared = False

    # check if player win
    if not pos_x:
        win = True
        draw_end()
        pause = True

    # defeat message
    if defeat:
        draw_defeat()

    # objects
    if not pause:
        navb_drw = screen.blit(bonus_nav, (x_navb, y_navb))
        screen.blit(lives_txt, (20, 10))
        screen.blit(score_txt, (950, 10))
        screen.blit(player, player_rect.topleft)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
