import curses
import random
import time

# Snake class
class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = [(x, y)]
        self.direction = curses.KEY_RIGHT

    def move(self):
        # Get the coordinates of the snake's head
        head_x, head_y = self.body[0]

        # Determine the new coordinates of the snake's head based on its direction
        if self.direction == curses.KEY_DOWN:
            new_head = (head_x, head_y + 1)
        elif self.direction == curses.KEY_UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == curses.KEY_RIGHT:
            new_head = (head_x + 1, head_y)
        elif self.direction == curses.KEY_LEFT:
            new_head = (head_x - 1, head_y)

        # Update the coordinates of the snake's head and body
        self.body.insert(0, new_head)
        self.body.pop()

    def change_direction(self, direction):
        # Prevent the snake from reversing its direction completely
        if (direction == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT) or \
                (direction == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT) or \
                (direction == curses.KEY_UP and self.direction == curses.KEY_DOWN) or \
                (direction == curses.KEY_DOWN and self.direction == curses.KEY_UP):
            return

        # Update the direction of the snake
        self.direction = direction

    def eat_food(self, food):
        # Get the coordinates of the snake's head
        head_x, head_y = self.body[0]

        # Check if the snake's head overlaps with the food
        if (head_x, head_y) == (food.x, food.y):
            # Generate new food at a random position
            food.generate()

            # Determine the coordinates of the new tail segment based on the snake's current direction
            if self.direction == curses.KEY_RIGHT:
                new_tail = (self.body[-1][0], self.body[-1][1] + 1)
            elif self.direction == curses.KEY_LEFT:
                new_tail = (self.body[-1][0], self.body[-1][1] - 1)
            elif self.direction == curses.KEY_DOWN:
                new_tail = (self.body[-1][0] + 1, self.body[-1][1])
            elif self.direction == curses.KEY_UP:
                new_tail = (self.body[-1][0] - 1, self.body[-1][1])

            # Add the new tail segment to the snake's body
            self.body.append(new_tail)

    def check_collision(self):
        # Get the coordinates of the snake's head
        head_x, head_y = self.body[0]

        # Check if the snake's head collides with the walls or its body
        if (head_x, head_y) in self.body[1:] or \
                head_x == 0 or head_x == curses.LINES - 1 or \
                head_y == 0 or head_y == curses.COLS - 1:
            return True

        return False

# Food class
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def generate(self):
        self.x = random.randint(1, curses.COLS - 2)
        self.y = random.randint(1, curses.LINES - 2)

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.snake = Snake(10, 10)
        self.food = Food(5, 5)
        self.score = 0

    def setup(self):
        # Initialize the game screen
        curses.curs_set(0)  # Hide the cursor
        self.stdscr.nodelay(1)  # Make getch() non-blocking
        self.stdscr.timeout(100)  # Set a delay of 100 milliseconds

        # Set up initial game state
        self.stdscr.clear()
        self.stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.draw()

    def draw(self):
        # Draw the game grid, snake, food, and score on the screen
        self.stdscr.addstr(0, 2, f"Score: {self.score}")
        self.stdscr.addch(self.food.y, self.food.x, 'O')
        for x, y in self.snake.body:
            self.stdscr.addch(y, x, '#')

    def handle_input(self):
        # Handle user input to change the snake's direction
        key = self.stdscr.getch()
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]:
            self.snake.change_direction(key)

    def update(self):
        # Update the game state, including moving the snake, checking collisions, and handling food
        self.snake.move()

        if self.snake.check_collision():
            self.game_over()

        if (self.snake.body[0][0], self.snake.body[0][1]) == (self.food.x, self.food.y):
            self.snake.eat_food(self.food)
            self.score += 1

    def run(self):
        # Run the game loop
        self.setup()

        while True:
            self.handle_input()
            self.update()
            self.stdscr.clear()
            self.stdscr.border()
            self.draw()
            self.stdscr.refresh()

            # Add a slight delay between frames
            time.sleep(0.1)

    def game_over(self):
        # Display the game over screen with the final score
        self.stdscr.clear()
        game_over_text = "Game Over X_X !"
        score_text = f"Your score: {self.score}"
        retry_text = "Press 'R' to play again or 'Q' to quit"
        self.stdscr.addstr(curses.LINES // 2 - 1, curses.COLS // 2 - len(game_over_text) // 2, game_over_text)
        self.stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - len(score_text) // 2, score_text)
        self.stdscr.addstr(curses.LINES // 2 + 1, curses.COLS // 2 - len(retry_text) // 2, retry_text)
        self.stdscr.refresh()

        while True:
            key = self.stdscr.getch()
            if key in [ord('r'), ord('R')]:
                self.reset()
                self.run()
                break
            elif key in [ord('q'), ord('Q')]:
                return #need to be finished

    def reset(self):
        # Reset the game state for a new game
        self.snake = Snake(10, 10)
        self.food = Food(5, 5)
        self.score = 0

# Main function
def main(stdscr):
    game = Game(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)
