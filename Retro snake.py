import pygame
import time
import random

# Initialize the game
pygame.init()

# Set the Dimensions and Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (168, 177, 141)
blue = (155, 188, 15)
border_color = (48, 98, 48)
border_color2 = (15, 56, 15)

# Dimensions
width = 800
height = 400

# Function to draw the edge of the screen
def desenhar_borda():
    pygame.draw.rect(screen, border_color2, [0, 0, width, height], 20) # darker border
    pygame.draw.rect(screen, border_color, [0, 0, width, height], 10) #lighter border

# Function to draw checkered background 
def desenhar_fundo_quadriculado():
    tile_size = 20  # square size
    cor1 = (155, 188, 15)  # clight color
    cor2 = (139, 172, 15)  # dark color

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            cor = cor1 if (x // tile_size + y // tile_size) % 2 == 0 else cor2
            pygame.draw.rect(screen, cor, (x, y, tile_size, tile_size))

# Create the display
screen = pygame.display.set_mode((width, height))

# Name the window
pygame.display.set_caption("Retro Snake")

# Define the clock
clock = pygame.time.Clock()

        #Game elements

# Function to create the snake
def snake(snake_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, white, [x[0], x[1], snake_size, snake_size])

# Create the message score
def message(score):
    font_style = pygame.font.SysFont("Early GameBoy Regular", 30)
    message = font_style.render("Score: " + str(score), True, white)
    screen.blit(message, [35, 35])

# Main function
def game():
    end_the_game = False
    game_over = False

    # Snake starting position
    x1 = width / 2
    y1 = height / 2

    # Change of snake position
    x1_change = 0
    y1_change = 0

    # Snake size
    snake_size = 10

    # List that will store the snake's position
    list_snake = []
    length_snake = 1

    # Apple position
    food_position = [round(random.randrange(0, width - snake_size) / 10.0) * 10.0,
                     round(random.randrange(0, height - snake_size) / 10.0) * 10.0]

    while not end_the_game:

        while game_over:
            screen.fill(blue)
            desenhar_fundo_quadriculado()
            desenhar_borda()

            font = pygame.font.SysFont("Early GameBoy Regular", 25)
            message_game_over = font.render("Game Over! Press C to play again", True, white)
            screen.blit(message_game_over, [width / 20, height / 2.5])
            message(length_snake - 1)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_the_game = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        end_the_game = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game()  # Recursive call, causing the issue

        # Snake movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_the_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_size
                    x1_change = 0

        # Check if the snake is out of the screen
        if x1 < 35 or x1 > width - 35 - snake_size or y1 < 35 or y1 > height - 35 - snake_size:
            game_over = True

        x1 += x1_change
        y1 += y1_change
        desenhar_fundo_quadriculado()
        desenhar_borda()

        # Draw the food
        pygame.draw.rect(screen, red, [food_position[0], food_position[1], snake_size, snake_size])

        # Position snake
        list_snake.append([x1, y1])

        if len(list_snake) > length_snake:
            del list_snake[0]

        # Check collision with own body
        for segment in list_snake[:-1]:
            if segment == [x1, y1]:
                game_over = True

        snake(snake_size, list_snake)
        message(length_snake - 1)

        # Check if the food has been eaten
        if x1 == food_position[0] and y1 == food_position[1]:
            # Garante que a nova comida fique dentro da borda de 40px
            food_position = [
                round(random.randrange(40, width - 40 - snake_size) / 10.0) * 10.0,
                round(random.randrange(40, height - 40 - snake_size) / 10.0) * 10.0
            ]
            length_snake += 1


        # Update the screen
        pygame.display.update()

        # Check if the snake eats the apple
        if x1 == food_position[0] and y1 == food_position[1]:
            food_position = [round(random.randrange(0, width - snake_size) / 10.0) * 10.0,
                             round(random.randrange(0, height - snake_size) / 10.0) * 10.0]
            length_snake += 1

        clock.tick(15)  # Control the speed of the snake

    # Quit the game
    pygame.quit()
    quit()

# Run the game
game()