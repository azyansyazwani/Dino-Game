#Azyan Syazwani Binti Setia(215014)

import pygame
import os
import random

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dinosaur Game")

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def start_screen():
    """
    Display the start screen with a "Press any KEY to START" message.
    """
    font = pygame.font.Font('freesansbold.ttf', 40)
    run = True

    while run:
        SCREEN.fill((255, 255, 255))  # Clear the screen with white color

        # Render the start text
        text = font.render("Press any KEY to START", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(text, text_rect)

        # Render an image or icon of the dinosaur (optional)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 50))

        pygame.display.update()

        # Wait for the user to press any key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:  # If any key is pressed
                run = False  # Exit the start screen loop


def display_question(question_count):
    """
    Display a question when the user loses and provide feedback on the answer.
    """
    questions = [
        ("The command to view the network interface in Ubuntu is ___ or ___.", "ifconfig,ip a"),
        ("The loopback interface is identified as ___", "lo"),
        ("The address ___ for IPv4 is AF_INET", "family"),
        ("Dictionary key __ in the ifaddresses() function is for IPv6.", "10"),
        ("There are no broadcast address and MAC address for ___.", "lo")
    ]
    font = pygame.font.Font('freesansbold.ttf', 30)
    small_font = pygame.font.Font('freesansbold.ttf', 20)
    question, correct_answer = random.choice(questions)
    answer = ""
    feedback = ""
    feedback_color = (0, 0, 0)  # Default feedback text color (black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if answer.lower() == correct_answer.lower():
                        feedback = "Good, your answer is correct!"
                        feedback_color = (0, 128, 0)  # Green for correct answer
                        pygame.time.delay(1000)  # Show feedback for 1 second
                        return True, question_count + 1
                    else:
                        feedback = "Wrong answer, try again"
                        feedback_color = (255, 0, 0)  # Red for incorrect answer
                elif event.key == pygame.K_BACKSPACE:
                    answer = answer[:-1]
                else:
                    answer += event.unicode

        SCREEN.fill((255, 255, 255))

        # Render the instruction text
        instruction_text = small_font.render("Answer the question to continue", True, (0, 0, 255))
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(instruction_text, instruction_rect)

        # Render question text
        question_text = font.render(question, True, (0, 0, 0))
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        SCREEN.blit(question_text, question_rect)

        # Render user answer text
        user_answer_text = font.render("Your Answer: " + answer, True, (0, 0, 0))
        user_answer_rect = user_answer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(user_answer_text, user_answer_rect)

        # Render feedback text
        if feedback:  # Only render feedback if it's not empty
            feedback_text = small_font.render(feedback, True, feedback_color)
            feedback_rect = feedback_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            SCREEN.blit(feedback_text, feedback_rect)

        pygame.display.update()


def final_score_screen(final_score):
    """
    Display the final score and a congratulatory message.
    """
    font = pygame.font.Font('freesansbold.ttf', 40)
    run = True

    while run:
        SCREEN.fill((255, 255, 255))  # Clear the screen with white color

        # Render congratulations message
        congratulations_text = font.render("Congratulations!", True, (0, 0, 0))
        congratulations_rect = congratulations_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(congratulations_text, congratulations_rect)

        # Render the final score
        final_score_text = font.render(f"Your Final Score: {final_score}", True, (0, 0, 255))
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        SCREEN.blit(final_score_text, final_score_rect)

        pygame.display.update()

        # Wait for the user to quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    question_count = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Score: " + str(points), True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 40))  # Positioned at the upper middle
        SCREEN.blit(text, text_rect)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Start screen
    start_screen()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                correct, question_count = display_question(question_count)
                if not correct:
                    pygame.quit()
                    exit()
                else:
                    obstacles.clear()
                    if question_count >= 5:
                        final_score_screen(points)
                        return  # End the game after showing the final score

        background()
        cloud.draw(SCREEN)
        cloud.update()
        score()
        clock.tick(30)
        pygame.display.update()


main()
