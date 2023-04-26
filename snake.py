import pygame
import sys
import random

# set up colors
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)

class SnakeGame:
    def __init__(self):
        pygame.init() # initialize pygame
        # set up display window
        self.WIDTH, self.HEIGHT = 640, 480
        self.FPS = 10 # Frames Per Seconds 
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food(self.WIDTH, self.HEIGHT)
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.is_game_over = False

    def draw_grid(self):
        # draw grid lines on the screen
        grid_color = (100,100,100)
        for x in range(0, self.WIDTH, 20):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, 20):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.WIDTH, y))
    
    def draw_length(self):
        # draw the current length of the snake on the screen.
        my_font = pygame.font.SysFont("monospace", 20)
        length_surface = my_font.render(f"Length: {len(self.snake.body)}", True, WHITE)
        length_rect = length_surface.get_rect()
        length_rect.topleft = (10,10)
        self.screen.blit(length_surface, length_rect)

    def process_keys(self, key):
        # process the user's input and update the snake's directions
        if key == pygame.K_UP and self.direction != "DOWN":
            self.change_to = "UP"
        elif key == pygame.K_DOWN and self.direction != "UP":
            self.change_to = "DOWN"
        elif key == pygame.K_LEFT and self.direction != "RIGHT":
            self.change_to = "LEFT"
        elif key == pygame.K_RIGHT and self.direction != "LEFT":
            self.change_to = "RIGHT"
        
        # ignore the jey press if it would cause the snake to reverse its direction completely
        if (self.direction == "UP" and self.change_to == "DOWN") or \
        (self.direction == "DOWN" and self.change_to == "UP") or \
        (self.direction == "LEFT" and self.change_to == "RIGHT") or \
        (self.direction == "RIGHT" and self.change_to == "LEFT"):
            return
        
        self.direction = self.change_to

    def handle_events(self, event):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.update_direction(event)

    def update_direction(self, event):
        if event.key == pygame.k_UP and self.direction !="DOWN":
            self.change_to = "UP"
        if event.key == pygame.k_DOWN and self.direction !="UP":
            self.change_to = "DOWN"
        if event.key == pygame.k_LEFT and self.direction !="RIGHT":
            self.change_to = "LEFT"
        if event.key == pygame.k_RIGHT and self.direction !="LEFT":
            self.change_to = "RIGHT"

        self.direction = self.change_to

    def is_collision(self):
        head = self.snake.head()
        # check if the head is outside the screen walls
        if head[0] < 0 or head[0] >= self.WIDTH or head[1] < 0 or head[1] >= self.HEIGHT:
            return True
        
        # check if the head collides with the body
        for block in self.snake.body[1:]: 
            if head == block:
                return True
        # otherwise there is no collision            
        return False
        
    def check_collision(self):
        if self.is_collision(): 
            self.is_game_over=True

    def update_game(self):
        new_head = self.snake.body[0].copy()

        if self.direction == "UP":
            new_head[1] -= self.snake.size
        elif self.direction == "DOWN":
            new_head[1] += self.snake.size
        elif self.direction == "LEFT":
            new_head[0] -= self.snake.size
        elif self.direction == "RIGHT":
            new_head[0] += self.snake.size

        if new_head[0] < 0 or new_head[0] >= self.WIDTH or new_head[1] < 0 or new_head[1] >= self.HEIGHT:
            self.is_game_over = True
        else:
            if new_head != self.food.position:
                self.snake.body.pop()
            self.snake.body.insert(0, new_head)
            if new_head == self.food.position:
                self.food.respawn(self.WIDTH, self.HEIGHT)
                self.snake.grow()

        self.check_collision()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.process_keys(event.key)

            if self.is_game_over:
                self.game_over()
            else:
                self.update_game()
                self.draw()
                self.clock.tick(self.FPS)

    def game_over(self):
        my_font = pygame.font.SysFont("monospace", 40)
        game_over_surface = my_font.render("Game Over!", True, RED)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.WIDTH//2, self.HEIGHT//4)
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.delay(2000) # wait 2 seconds
        pygame.quit()
        sys.exit()


    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.draw_length()
        pygame.display.flip()


class Snake:
    def __init__(self):
        self.size = 20
        self.speed = 12
        self.body = [
            [100,60],
            [80,60],
            [60,60]
        ]
    
    def move(self, direction):
        if direction=="UP":
            self.body.insert(0, self.body[0][0], self.body[0][1]-self.size)
        if direction=="DOWN":
            self.body.insert(0, self.body[0][0], self.body[0][1]+self.size)
        if direction=="LEFT":
            self.body.insert(0, self.body[0][0]-self.size, self.body[0][1])
        if direction=="RIGHT":
            self.body.insert(0, self.body[0][0]+self.size, self.body[0][1])

    def grow(self):
        tail= self.body[-1]
        tail_prev= self.body[-2]
        dx = tail_prev[0] - tail[0]
        dy = tail_prev[1] - tail[1]
        new_tail = [tail[0] - dx, tail[1] - dy]
        self.body.append(new_tail)

    def head(self):
        return self.body[0]

    def draw(self, screen):
        for pos in self.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], self.size, self.size))


class Food:
    def __init__(self, width, height):
        self.size = 20
        self.position = [random.randrange(1,(width // 20)) * 20, random.randrange(1,(height // 20)) * 20]

    def respawn(self, width, height):
        self.position = [random.randrange(1,(width // 20)) * 20, random.randrange(1,(height // 20)) * 20]        

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.position[0], self.position[1], self.size, self.size))

if __name__ == "__main__":
    game = SnakeGame()
    game.run()