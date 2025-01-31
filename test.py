import pygame
import random
import time

# Инициализация pygame
pygame.init()
run_game = True

# Разрешения
resolutions = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1920, 1080)
]

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Шрифты
font = pygame.font.SysFont('chalkduster.ttf', 40)
small_font = pygame.font.SysFont('chalkduster.ttf', 30)

# Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        if self.hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surface = small_font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Функция для выбора разрешения
def select_resolution():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Выберете разрешение')

    buttons = []
    for i, res in enumerate(resolutions):
        button = Button(200, 150 + i * 100, 400, 80, f'{res[0]}x{res[1]}', GRAY, GREEN)
        buttons.append(button)

    selected_resolution = None

    while selected_resolution is None:
        screen.fill(WHITE)
        title = font.render('Выберете разрешение', True, BLACK)
        screen.blit(title, (200, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.check_hover(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.is_clicked(event.pos):
                        selected_resolution = resolutions[i]

        for button in buttons:
            button.draw(screen)

        pygame.display.update()

    return selected_resolution

# Разрешения
WIDTH, HEIGHT = select_resolution()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Breakout Game')


# Главное меню
def main_menu():
    global run_game
    screen.fill(BLACK)
    title = font.render('Breakout Game', True, WHITE)
    start_button = Button(WIDTH // 2 - 100, 300, 200, 80, 'Начать игру', GRAY, GREEN)
    quit_button = Button(WIDTH // 2 - 100, 400, 200, 80, 'Выход', GRAY, RED)

    while run_game:
        pygame.display.update()
        screen.fill(BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        start_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION:
                start_button.check_hover(event.pos)
                quit_button.check_hover(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    countdown()
                    game_loop()
                if quit_button.is_clicked(event.pos):
                    run_game = False
                    pygame.quit()
                    return


# Отсчет для старта игры
def countdown():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        countdown_text = font.render(f'Начало через {i}...', True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        time.sleep(1)

# Бонусы
def apply_bonus(balls, platform_multiplier):
    bonus_type = random.choice(['extra_balls', 'speed_up', 'platform_increase'])
    if bonus_type == 'extra_balls':
        balls.append((WIDTH // 2, HEIGHT // 2, 5 * WIDTH / 800, -5 * HEIGHT / 600))
        balls.append((WIDTH // 2, HEIGHT // 2, -5 * WIDTH / 800, -5 * HEIGHT / 600))
        bonus_text = small_font.render('Бонус: Удвоение шаров', True, WHITE)
    elif bonus_type == 'speed_up':
        for i in range(len(balls)):
            balls[i] = (balls[i][0], balls[i][1], balls[i][2] * 1.2, balls[i][3] * 1.2)
        bonus_text = small_font.render('Бонус: Увеличение скорости шаров', True, WHITE)
    elif bonus_type == 'platform_increase':
        platform_multiplier = min(platform_multiplier + 0.5, 2.0)  # Limit platform size
        bonus_text = small_font.render('Бонус: Увеличение платформы', True, WHITE)
        # Reset platform size after 10 seconds
        pygame.time.set_timer(pygame.USEREVENT, 10000)  # 10 seconds

    screen.blit(bonus_text, (WIDTH // 2 - bonus_text.get_width() // 2, HEIGHT // 2 - bonus_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1000)
    return platform_multiplier

# Создание кирпичиков
def generate_bricks(level):
    bricks = []
    # Базовый размер кирпичей
    base_brick_width = 75 * WIDTH / 800
    base_brick_height = 30 * HEIGHT / 600
    # Уменьшайте размер кирпича по мере повышения уровня
    brick_width = max(50 * WIDTH / 800, base_brick_width * (0.9 ** (level - 1)))
    brick_height = max(20 * HEIGHT / 600, base_brick_height * (0.9 ** (level - 1)))
    # Увеличивайте количество кирпичей по мере повышения уровня
    rows = 5 + level
    cols = 8 + level
    # Рассчитайте расстояние между кирпичами, чтобы они располагались по центру
    total_width = cols * (brick_width + 10 * WIDTH / 800) - 10 * WIDTH / 800
    start_x = (WIDTH - total_width) // 2
    for i in range(rows):
        for j in range(cols):
            bricks.append(pygame.Rect(
                start_x + j * (brick_width + 10 * WIDTH / 800),
                50 * HEIGHT / 600 + i * (brick_height + 10 * HEIGHT / 600),
                brick_width,
                brick_height
            ))
    return bricks

# Игровой цикл
def game_loop():
    global run_game
    paddle_width, paddle_height = 100 * WIDTH / 800, 20 * HEIGHT / 600
    paddle_x = (WIDTH - paddle_width) // 2
    paddle_y = HEIGHT - paddle_height - 10
    paddle_speed = 10 * WIDTH / 800

    ball_radius = 10 * WIDTH / 800
    ball_x = paddle_x + paddle_width // 2  # шарик начинает на платформе
    ball_y = paddle_y - ball_radius
    ball_dx = 5 * WIDTH / 800
    ball_dy = -5 * HEIGHT / 600

    lives = 3
    level = 1
    score = 0

    bricks = generate_bricks(level)  # Генерация кирпичуй для текущего уровня

    paused = False
    balls = [(ball_x, ball_y, ball_dx, ball_dy)]  # Список для управления несколькими шарами
    platform_multiplier = 1  # Множитель размера платформы
    platform_timer = 0  # Таймер для увеличения бонуса на платформе

    while run_game:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    run_game = False
                    pygame.quit()
                    return
            if event.type == pygame.USEREVENT:  # Сброс размера платформы по истечении таймера
                platform_multiplier = 1
                platform_timer = 0

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle_x > 0:
                paddle_x -= paddle_speed
            if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width * platform_multiplier:
                paddle_x += paddle_speed

            new_balls = []
            for ball in balls:
                bx, by, bdx, bdy = ball
                bx += bdx
                by += bdy

                if bx <= 0 or bx >= WIDTH:
                    bdx *= -1
                if by <= 0:
                    bdy *= -1
                if by >= HEIGHT:
                    continue  # Мяч упал не добавлять его обратно

                paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width * platform_multiplier, paddle_height)
                if paddle_rect.collidepoint(bx, by):
                    # Проверить попадает ли мяч в верхнюю часть платформы
                    if by + ball_radius >= paddle_y and bdy > 0:
                        # Рассчитать относительное положение мяча на лопатке
                        relative_intersect_x = (bx - paddle_x) / (paddle_width * platform_multiplier)
                        # Регкляция горизонтальной скорости мяча в зависимости от того где он попадает в ракетку
                        bdx = (relative_intersect_x - 0.5) * 10  # Регуляция множителя для достижения желаемого эффекта
                        bdy *= -1

                for brick in bricks[:]:
                    if brick.collidepoint(bx, by):
                        bricks.remove(brick)
                        bdy *= -1
                        score += 10
                        if random.randint(0, 100) < 10:  # 10% шанс на бонус
                            platform_multiplier = apply_bonus(balls, platform_multiplier)

                new_balls.append((bx, by, bdx, bdy))

            balls = new_balls

            if not balls:  # Не осталось шариков
                lives -= 1
                if lives == 0:
                    game_over(score)
                    return
                balls = [(paddle_x + paddle_width // 2, paddle_y - ball_radius, 5 * WIDTH / 800, -5 * HEIGHT / 600)]  # Сброс мяча на платформу
                countdown()

            if not bricks:
                level += 1
                if level > 5:
                    festive_congratulations()
                    return
                bricks = generate_bricks(level)  # Создание кирпичей для нового уровня

        pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width * platform_multiplier, paddle_height))
        for ball in balls:
            pygame.draw.circle(screen, RED, (int(ball[0]), int(ball[1])), int(ball_radius))
        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick)

        lives_text = small_font.render(f'Жизни: {lives}', True, WHITE)
        level_text = small_font.render(f'Уровень: {level}', True, WHITE)
        score_text = small_font.render(f'Счет: {score}', True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(score_text, (10, 90))

        if paused:
            pause_text = font.render('Игра приостановлена', True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

        pygame.display.update()
        pygame.time.Clock().tick(60)

# Конец игры
def game_over(score):
    global run_game
    screen.fill(BLACK)
    game_over_text = font.render('Игра окончена', True, WHITE)
    score_text = font.render(f'Ваш счет: {score}', True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + score_text.get_height()))
    pygame.display.update()

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run_game = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main_menu()
                return

# Праздничное поздравление
def congratulations():
    global run_game
    screen.fill(BLACK)
    congrats_text = font.render('Поздравляем! Вы прошли игру!', True, WHITE)
    screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - congrats_text.get_height() // 2))
    pygame.display.update()

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run_game = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main_menu()
                return

# Главная функция
def main():
    main_menu()

if __name__ == '__main__':
    main()
