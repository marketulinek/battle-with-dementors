import pygame
import random


pygame.init()

# Screen
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Battle with Dementors')

# Settings
fps = 60
clock = pygame.time.Clock()


# Classes
class Game:
    def __init__(self, our_player, group_of_dementors):
        self.score = 0
        self.round_number = 0

        self.rount_time = 0
        self.slow_down_cycle = 0

        self.our_player = our_player
        self.group_of_dementors = group_of_dementors

        # Background music
        pygame.mixer.music.load('media/bg-music-hp.wav')
        pygame.mixer.music.play(-1, 0.0)

        # Fonts
        self.hp_font = pygame.font.Font('fonts/Harry.ttf', 24)
        self.hp_font_big = pygame.font.Font('fonts/Harry.ttf', 45)

        self.background_image = pygame.image.load('img/bg-dementors.png')
        self.background_image_rect = self.background_image.get_rect()
        self.background_image_rect.topleft = (0, 0)

        # Pictures
        blue_img = pygame.image.load('img/mozkomor-modry.png')
        green_img = pygame.image.load('img/mozkomor-zeleny.png')
        pink_img = pygame.image.load('img/mozkomor-ruzovy.png')
        yellow_img = pygame.image.load('img/mozkomor-zluty.png')
        self.dementor_imgs = [blue_img, green_img, pink_img, yellow_img]

        # Generates wanted dementor type (when game starts)
        self.dementor_catch_type = random.randint(0, 3)
        self.dementor_catch_img = self.dementor_imgs[self.dementor_catch_type]

        self.dementor_catch_rect = self.dementor_catch_img.get_rect()
        self.dementor_catch_rect.centerx = width//2
        self.dementor_catch_rect.top = 25

    # This method is being called over and over again
    def update(self):
        self.slow_down_cycle += 1
        if self.slow_down_cycle == fps:
            self.rount_time += 1
            self.slow_down_cycle = 0

        self.check_collisions()

    # Drawing everything in game
    def draw(self):
        dark_yellow = pygame.Color('#938f0c')
        blue = (21, 31, 217)
        green = (24, 194, 38)
        purple = (195, 23, 189)
        yellow = (195, 181, 23)

        colors = [blue, green, purple, yellow]

        # Text setting
        catch_text = self.hp_font.render('Catch this dementor', True, dark_yellow)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = width//2
        catch_text_rect.top = 5

        score_text = self.hp_font.render(f'Score: {self.score}', True, dark_yellow)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, 4)

        lives_text = self.hp_font.render(f'Life: {self.our_player.lives}', True, dark_yellow)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (10, 30)

        round_text = self.hp_font.render(f'Round: {self.round_number}', True, dark_yellow)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (10, 60)

        time_text = self.hp_font.render(f'Time: {self.rount_time}', True, dark_yellow)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (width-5, 5)

        back_safe_zone_text = self.hp_font.render(f'Safe zone: {self.our_player.enter_safe_zone}', True, dark_yellow)
        back_safe_zone_text_rect = back_safe_zone_text.get_rect()
        back_safe_zone_text_rect.topright = (width - 5, 35)

        # Blitting
        screen.blit(catch_text, catch_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(lives_text, lives_text_rect)
        screen.blit(round_text, round_text_rect)
        screen.blit(time_text, time_text_rect)
        screen.blit(back_safe_zone_text, back_safe_zone_text_rect)
        # Blit dementor to catch
        screen.blit(self.dementor_catch_img, self.dementor_catch_rect)

        # Shapes
        pygame.draw.rect(screen, colors[self.dementor_catch_type], (0, 100, width, height - 200), 4)

    # Checking player's collision with dementor
    def check_collisions(self):
        # get dementor hit by a player
        collided_mozkomor = pygame.sprite.spritecollideany(self.our_player, self.group_of_dementors)

        if collided_mozkomor:
            # hitted dementor with the correct type?
            if collided_mozkomor.type == self.dementor_catch_type:
                self.our_player.catch_sound.play()
                self.score += 10 * self.round_number
                collided_mozkomor.remove(self.group_of_dementors)

                if self.group_of_dementors:
                    self.choose_new_target()
                else:
                    self.our_player.reset()
                    self.start_new_round()
            else:
                self.our_player.wrong_sound.play()
                self.our_player.lives -= 1

                if self.our_player.lives < 1:
                    self.pause_game(f'Obtained score: {self.score}', 'Hit the enter to play again!')
                    self.resert_game()

                self.our_player.reset()

    # Start new round with higher number of dementors in game
    def start_new_round(self):
        self.score += int(100 * (self.round_number / (1 + self.rount_time)))

        self.rount_time = 0
        self.slow_down_cycle = 0
        self.round_number += 1
        self.our_player.enter_safe_zone += 1

        for deleted_dementor in self.group_of_dementors:
            self.group_of_dementors.remove(deleted_dementor)

        for i in range(self.round_number):
            self.group_of_dementors.add(Dementor(random.randint(0, width - 64), random.randint(100, height - 164), self.dementor_imgs[0], 0))
            self.group_of_dementors.add(Dementor(random.randint(0, width - 64), random.randint(100, height - 164), self.dementor_imgs[1], 1))
            self.group_of_dementors.add(Dementor(random.randint(0, width - 64), random.randint(100, height - 164), self.dementor_imgs[2], 2))
            self.group_of_dementors.add(Dementor(random.randint(0, width - 64), random.randint(100, height - 164), self.dementor_imgs[3], 3))

        self.choose_new_target()

    # Choose new dementor which should be cought next
    def choose_new_target(self):
        new_dementor_to_catch = random.choice(self.group_of_dementors.sprites())
        self.dementor_catch_type = new_dementor_to_catch.type
        self.dementor_catch_img = new_dementor_to_catch.image

    # The pause before new game and at the start of app
    def pause_game(self, main_text, subheading_text):
        dark_yellow = pygame.Color('#938f0c')
        black = (0, 0, 0)

        main_text_create = self.hp_font_big.render(main_text, True, dark_yellow)
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (width//2, height//2)

        subheading_text_create = self.hp_font_big.render(subheading_text, True, dark_yellow)
        subheading_text_create_rect = subheading_text_create.get_rect()
        subheading_text_create_rect.center = (width//2, (height//2) + 60)

        screen.fill(black)
        screen.blit(main_text_create, main_text_create_rect)
        screen.blit(subheading_text_create, subheading_text_create_rect)

        pygame.display.update()

        paused = True
        while paused:
            for one_event in pygame.event.get():
                if one_event.type == pygame.KEYDOWN:
                    if one_event.key == pygame.K_RETURN:
                        paused = False
                    if one_event.key == pygame.QUIT:
                        paused = False

    # Resets game to default
    def resert_game(self):
        self.score = 0
        self.round_number = 0

        self.our_player.lives = 5
        self.our_player.enter_safe_zone = 3
        self.start_new_round()

        pygame.mixer.music.play(-1, 0.0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/potter-icon.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2
        self.rect.bottom = height

        self.lives = 5
        self.enter_safe_zone = 3
        self.speed = 8

        self.catch_sound = pygame.mixer.Sound('media/expecto-patronum.mp3')
        self.catch_sound.set_volume(0.1)
        self.wrong_sound = pygame.mixer.Sound('media/wrong.wav')
        self.wrong_sound.set_volume(0.1)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < height - 100:
            self.rect.y += self.speed

    def back_to_safe_zone(self):
        if self.enter_safe_zone > 0:
            self.rect.bottom = height
            self.enter_safe_zone -= 1

    # Put player back to the default position (safe zone)
    def reset(self):
        self.rect.centerx = width//2
        self.rect.bottom = height


class Dementor(pygame.sprite.Sprite):
    def __init__(self, x, y, image, dementor_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Dementor types:
        # 0 - blue
        # 1 - green
        # 2 - pink
        # 3 - yellow
        self.type = dementor_type
        self.x = random.choice([-1, 1])
        self.y = random.choice([-1, 1])
        self.speed = random.randint(1, 5)

    def update(self):
        # movement
        self.rect.x += self.x * self.speed
        self.rect.y += self.y * self.speed

        # bounce
        if self.rect.left < 0 or self.rect.right > width:
            self.x = self.x * -1
        if self.rect.top < 100 or self.rect.bottom > height-100:
            self.y = self.y * -1


# Dementors group
dementor_group = pygame.sprite.Group()

# Players group
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

# Object Game
my_game = Game(player, dementor_group)
my_game.pause_game('Harry Potter and the battle with dementors', 'Hit enter to play!')
my_game.start_new_round()

# Playing game
lets_continue = True

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.back_to_safe_zone()

    screen.fill((0, 0, 0))
    screen.blit(my_game.background_image, my_game.background_image_rect)

    dementor_group.draw(screen)
    dementor_group.update()

    player_group.draw(screen)
    player_group.update()

    my_game.update()
    my_game.draw()

    pygame.display.update()

    clock.tick(fps)

pygame.quit()
