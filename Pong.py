# Pong.py
# Author: Karl Moritz
# Date: 2015-11-23
# Pong clone I made when I was bored and learning python and pygame.
# Really simple game but the code is kind of messy and needs some clean-up and bug fixing.
# Start the game either by calling the Pong() class or by running Pong.py
# Controls:
# Restart: R
# Start: Space
# Player 1:
# Up: W, Down: S
# Player 2:
# Up: Up arrow, Down: Down Arrow

import pygame
from pygame.locals import *
import sys
import random
import math


# Paddle is a pygame rectangle with a few extra methods added on top
class Paddle:
    def __init__(self, player, x, y, width, height):
        self.player = player
        self.pos = pygame.Rect(x, y, width, height)

    def get_player(self):
        return self.player

    def get_x(self):
        return self.pos.x

    def get_y(self):
        return self.pos.y

    def update_paddle(self, offset):
        self.pos = self.pos.move(0, offset)

    def draw_paddle(self, surface):
        pygame.draw.rect(surface, [255, 255, 255], self.pos, 0)


# Square ball
class Ball:
    def __init__(self, x, y, side, velocity):
        self.Xvelocity = velocity[0]
        self.Yvelocity = velocity[1]
        self.pos = pygame.Rect(x, y, side, side)
        self.side = side

    def get_x(self):
        return self.pos.x

    def get_y(self):
        return self.pos.y

    def get_side(self):
        return self.side

    def get_x_velocity(self):
        return self.Xvelocity

    def get_y_velocity(self):
        return self.Yvelocity

    def set_position(self, x, y):
        self.pos = pygame.Rect(x, y, self.side, self.side)

    def update_position(self, time):
        self.pos = self.pos.move(int(self.Xvelocity * time), int(self.Yvelocity * time))

    def update_velocity(self, direction, change):
        self.Xvelocity += math.copysign(change[0], self.Xvelocity)
        self.Yvelocity += math.copysign(change[1], self.Yvelocity)
        self.Xvelocity *= direction[0]
        self.Yvelocity *= direction[1]

    def draw_ball(self, surface):
        pygame.draw.rect(surface, [255, 255, 255], self.pos, 0)


class Pong:
    CAPTION = "PONG"

    FRAMERATE = 120
    SCREENHEIGHT = 600
    SCREENWIDTH = 600

    SCORELIMIT = 10

    SCOREPOS = [SCREENWIDTH // 2, 40]
    WINNERPOS = [SCREENWIDTH // 2, SCREENHEIGHT // 2]

    PADDLEWIDTH = 10
    PADDLEHEIGHT = 80
    PADDLESPEED = int(1000 / FRAMERATE)

    BALLDIAMETER = 10

    def __init__(self):
        pygame.init()
        # initialize screen
        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        pygame.display.set_caption(self.CAPTION)
        # initialize font
        self.w_message = pygame.font.Font(None, 50)
        self.scores = pygame.font.Font(None, 50)
        # Initialize paddle and ball
        self.paddle_1 = Paddle(1, 0, (self.SCREENHEIGHT - self.PADDLEHEIGHT) // 2, self.PADDLEWIDTH, self.PADDLEHEIGHT)
        self.paddle_2 = Paddle(2, self.SCREENWIDTH - self.PADDLEWIDTH, (self.SCREENHEIGHT - self.PADDLEHEIGHT) // 2,
                               self.PADDLEWIDTH, self.PADDLEHEIGHT)
        self.ball_1 = Ball(self.SCREENWIDTH / 2, self.SCREENHEIGHT / 2, self.BALLDIAMETER,
                           self.get_random_velocities())

        # Initialize score
        self.score = [0, 0]
        self.scoretext = str(self.score[0]) + " - " + str(self.score[1])
        self.winner = "Winning player: "

        self.start()

    def start(self):
        self.draw_objects()  # Draw the board before the game starts gives a better feel for the players when it starts
        self.pause()
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Game sequence: Listen for key presses
            # Update the ball position
            # Calculate boundary conditions
            # Draw all the objects

            self.get_keypresses()
            self.ball_1.update_position(int(1000 / self.FRAMERATE))
            self.collide()

            self.draw_objects()

            pygame.time.wait(int(1000 / self.FRAMERATE))

    def draw_objects(self):

        self.screen.fill([0, 0, 0])
        self.paddle_1.draw_paddle(self.screen)
        self.paddle_2.draw_paddle(self.screen)
        self.ball_1.draw_ball(self.screen)
        self.screen.blit(self.scores.render(self.scoretext, 0, [255, 255, 255], None), self.scores.size(self.scoretext))

        if self.check_score():
            self.screen.blit(self.w_message.render(self.winner, 0, [255, 255, 255], None),
                             self.w_message.size(self.winner))
            self.new_game()
        pygame.display.flip()

    def get_keypresses(self):
        # Controls Paddle 1: W: up; S: down; Paddle 2: up arrow: up; down arrow: down; r: new game

        press = pygame.key.get_pressed()
        if press[pygame.K_w] != 0 and self.paddle_1.get_y() > 0:
            self.paddle_1.update_paddle(-self.PADDLESPEED)
        elif press[pygame.K_s] != 0 and self.paddle_1.get_y() + self.PADDLEHEIGHT < self.SCREENHEIGHT:
            self.paddle_1.update_paddle(self.PADDLESPEED)
        if press[pygame.K_UP] != 0 and self.paddle_2.get_y() > 0:
            self.paddle_2.update_paddle(-self.PADDLESPEED)
        elif press[pygame.K_DOWN] != 0 and self.paddle_2.get_y() + self.PADDLEHEIGHT < self.SCREENHEIGHT:
            self.paddle_2.update_paddle(self.PADDLESPEED)

        if press[pygame.K_r] != 0:
            self.new_game()

    def new_game(self):
        self.score = [0, 0]
        self.scoretext = str(self.score[0]) + " - " + str(self.score[1])
        self.winner = "Winning player: "

    def collide(self):
        # Get the positions of the sides, for when the ball reaches the edge of the screens ( technically I could draw 4
        # black rectangles outside the screen and check for collisions but I feel that this is a lot cleaner of a
        # solution.
        x_lim = (self.ball_1.get_x(),
                 self.ball_1.get_x() + self.ball_1.get_side())
        y_lim = (self.ball_1.get_y(),
                 self.ball_1.get_y() + self.ball_1.get_side())

        if y_lim[0] < 0 or y_lim[1] > self.SCREENHEIGHT:  # On collision with top or bottom side reverse the y-velocity
            # with no added velocity
            self.ball_1.update_velocity((1, -1), (0, 0))

        if self.paddle_1.pos.colliderect(self.ball_1.pos) or \
                self.paddle_2.pos.colliderect(self.ball_1.pos):  # Check if the ball is within the paddle
            self.ball_1.update_velocity((-1, 1), (0.01, 0))  # On collision with the paddle reverse the x-velocity and
            # increase it slightly (for added difficulty)

            # Next two statements checks if the ball is within any of the paddles and if it is moves the ball 1 pixel
            # out from the paddle. This prevents a bug where the ball gets stuck in a paddle if the angle to the paddle
            # and velocity are really low. it's not a perfect solution. For some reason moving the ball to the impact
            # point still allowed the bug to happen, probably due to how the colliderect() function works so 1 pixel
            # offset it is
            if self.ball_1.get_x() < self.PADDLEWIDTH:
                self.ball_1.set_position(self.PADDLEWIDTH + self.ball_1.get_side() + 1,
                                         self.ball_1.get_y())
            elif self.ball_1.get_x() > self.SCREENWIDTH - self.PADDLEWIDTH:
                self.ball_1.set_position(self.SCREENWIDTH - self.PADDLEWIDTH - self.ball_1.get_side() - 1,
                                         self.ball_1.get_y())
        # Scoring mechanic
        elif x_lim[0] < 0:
            self.score[1] += 1
            self.scoretext = str(self.score[0]) + " - " + str(self.score[1])
            self.reset()
        elif x_lim[1] > self.SCREENWIDTH:
            self.score[0] += 1
            self.scoretext = str(self.score[0]) + " - " + str(self.score[1])
            self.reset()

    # Checks for a winner
    def check_score(self):

        if self.score[0] == self.SCORELIMIT:
            self.winner += "1"
            return True
        elif self.score[1] == self.SCORELIMIT:
            self.winner += "2"
            return True
        return False

    # Resets the game board and pauses the game. Could probably do this by added a set_position method to the paddle
    # class but it would work basically the same way, with just a few bytes of memory saved.
    def reset(self):
        self.paddle_1 = Paddle(1, 0, (self.SCREENHEIGHT - self.PADDLEHEIGHT) // 2, self.PADDLEWIDTH, self.PADDLEHEIGHT)
        self.paddle_2 = Paddle(2, self.SCREENWIDTH - self.PADDLEWIDTH, (self.SCREENHEIGHT - self.PADDLEHEIGHT) // 2,
                               self.PADDLEWIDTH, self.PADDLEHEIGHT)
        self.ball_1 = Ball(self.SCREENWIDTH / 2, self.SCREENHEIGHT / 2, self.BALLDIAMETER,
                           self.get_random_velocities())

        self.draw_objects()
        self.pause()

    # Pauses the game until the space bar is pressed
    def pause(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    return

    # When the game starts the ball needs a random velocity in a certain direction, the velocity cannot be 0 however
    # except maybe in the y-direction though that would make for a boring game
    @staticmethod
    def get_random_velocities():
        velocities = list(range(-4, -2)) + list(range(2, 4))
        x_vel = random.choice(velocities) / 10
        y_vel = random.choice(velocities) / 20
        return x_vel, y_vel


if __name__ == "__main__":
    Pong()
