import random

import pygame
import sys
import json
from scenes import current_scene, scenes, player_choice

# Настройки игры

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music/Main_Menu.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
choice_sound = pygame.mixer.Sound('music/choice_sound.mp3')
choice_sound.set_volume(0)
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Midnight Stories")

# Оформление

default_background = pygame.image.load('pic/background.jpg')
default_background = pygame.transform.scale(default_background, (screen_width, screen_height))
background = default_background
current_music_path = None
try:
    font = pygame.font.Font('font/basis33.ttf', 36)
except FileNotFoundError:
    print("Ошибка: файл шрифта 'basis33.ttf' не найден!")
    pygame.quit()
    sys.exit()
white = (255, 255, 255)
black = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 30

# Функция отрисовки текста

def draw_text(text, x, y, screen, font, color=white, line_spacing=1.5, center=False):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, color)
        text_rect = rendered_text.get_rect()
        if center:
            x = (screen.get_width() - text_rect.width) // 2
            y = (screen.get_height() - text_rect.height) // 2 + i * (font.get_height() * line_spacing)
        screen.blit(rendered_text, (x, y))

# Смена фона и музыки

def change_scene_background_and_music(scene_name):
    global background, current_music_path
    scene_data = {
        "Im_legend": ("pic/legend.jpg", "music/Im_legend2.mp3"),
        "Im_legend_start": ("pic/bedroom.jpg", "music/Im_legend.mp3"),
        "Im_legend_woke_up": ("pic/bedroom.jpg", "music/Im_legend.mp3"),
        "Im_legend_woke_up_2": ("pic/bedroom.jpg", "music/Im_legend.mp3"),
        "Im_legend_breakfast": ("pic/kitchen.jpg", "music/Im_legend.mp3"),
        "Im_legend_way_to_work": ("pic/street.jpg", "music/Im_legend2.mp3"),
        "Im_legend_way_to_work_2": ("pic/street.jpg", "music/Im_legend2.mp3"),
        "Im_legend_at_work": ("pic/in_office.jpg", "music/Im_legend3.mp3"),
        "Im_legend_at_work_2": ("pic/in_office.jpg", "music/Im_legend3.mp3"),
        "Im_legend_at_work_3": ("pic/office_view.jpg", "music/Im_legend_emot.mp3"),
        "Im_legend_at_work_troll": ("pic/office_troll.jpg", "music/Im_legend_emot.mp3"),
        "Im_legend_at_work_view_window": ("pic/office_view.jpg", "music/Im_legend_emot.mp3"),
        "Im_legend_at_work_start": ("pic/in_office.jpg", "music/Im_legend_emot.mp3"),
        "Im_legend_at_work_exit_1": ("pic/office_find.jpg", "music/Im_legend_emot.mp3"),
        "Im_legend_at_work_exit": ("pic/way_home.jpg", "music/Im_legend_emot.mp3"),
        "Im_legend_looking_for_people": ("pic/way_home.jpg", "music/Im_legend_emot.mp3"),
        "Im_legend_at_home_1": ("pic/legend_at_home.jpg", "music/Im_legend.mp3"),
        "Im_legend_at_home_dinner": ("pic/kitchen.jpg", "music/Im_legend.mp3"),
        "Im_legend_at_home_2": ("pic/legend_at_home.jpg", "music/Im_legend.mp3"),
        "Im_legend_game_start": ("pic/game.jpg", "music/game.mp3"),
        "Im_legend_game_no": ("pic/game.jpg", "music/game.mp3"),
        "Im_legend_game_no2": ("pic/game.jpg", "music/game.mp3"),
        "Im_legend_final_choice": ("pic/ending_1.jpg", "music/Im_legend.mp3"),
        "Im_legend_final_choice2": ("pic/game.jpg", "music/ending_l.mp3"),
        "Im_legend_final_ending": ("pic/ending.jpg", "music/ending_l.mp3"),
        "Im_legend_ending_1": ("pic/ending_home.jpg", "music/ending_l.mp3"),
        "Im_legend_ending_2": ("pic/ending_science.jpg", "music/ending_l.mp3"),
        "Im_legend_ending_3": ("pic/ending_home_destroy.jpg", "music/im_l_end.mp3"),
    }
    image_path, music_path = scene_data.get(scene_name, ("pic/background.jpg", "music/Main_Menu.mp3"))
    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (screen_width, screen_height))
    if current_music_path != music_path:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        current_music_path = music_path
    screen.blit(background, (0, 0))
    pygame.display.update()

# Отображение инвентаря + предметы

def show_inventory(screen, font):
    if not inventory:
        screen.blit(background, (0, 0))
        draw_text("Инвентарь пуст", 50, 150, screen, font)
        pygame.display.flip()
        pygame.time.wait(2000)
        return
    running = True
    while running:
        screen.blit(background, (0, 0))
        draw_text("Инвентарь:", 50, 150, screen, font)
        for i, item in enumerate(inventory):
            draw_text(f"{i+1}. {item}", 50, 100 + i * 40, screen, font)
        draw_text("Нажмите номер предмета для использования или Esc для выхода", 50, 100 + len(inventory) * 40 + 40, screen, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    index = event.key - pygame.K_1
                    if index < len(inventory):
                        item = inventory[index]
                        #Предметы для легенды
                        if item == "Пачка сигарет (+ 5 здоровья)":
                            max_hp, _ = update_player_stats()
                            player_hp = min(player_hp + 5, max_hp)  # +5 HP, не превышая максимум
                            draw_text("Курение - это не самая плохая зависимость. +5 HP", 300, 300, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(5000)
                            inventory.pop(index)
                        elif item == "Бутылка 'XXX' (+ 5 здоровья)":
                            max_hp, _ = update_player_stats()
                            player_hp = min(player_hp + 5, max_hp)  # +5 HP, не превышая максимум
                            draw_text("Мы не будем говорить что это - но вы знаете сами. +5 HP", 300, 300, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(5000)
                            inventory.pop(index)
                        elif item == "Яичница (+ 2 здоровья)":
                            max_hp, _ = update_player_stats()
                            player_hp = min(player_hp + 2, max_hp)  # +5 HP, не превышая максимум
                            draw_text("Самый лучший завтрак. +2 HP", 300, 300, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(5000)
                            inventory.pop(index)
                        elif item == "Зажигалка":
                            draw_text("Зачем она нужна?", 300, 300, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(5000)
                            inventory.pop(index)
                        #Предметы для ххх
                        elif item == "Ржавый меч":
                            draw_text("Ржавый меч экипирован! Ваш урон увеличен.", 300, 300, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(5000)
                            # Можно добавить временное увеличение урона, если хочешь
                        elif item == "Чертёж":
                            player_stats["intelligence"] += 1
                            draw_text("Вы изучили чертёж! +1 Интеллект", 300, 300, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(5000)
                            inventory.pop(index)
                            max_hp, damage = update_player_stats()  # Пересчитываем характеристики

# Характеристики игрока

player_stats = {
    "strength": 1,     # Сила
    "agility": 1,      # Ловкость
    "intelligence": 1  # Интеллект
}
base_hp = 10          # Базовое здоровье
base_damage = 3       # Базовый урон
player_hp = base_hp   # Текущее здоровье
inventory = []

def update_player_stats():
    global player_hp, base_hp, base_damage
    max_hp = base_hp + player_stats["strength"] * 2  # 1 Сила = +2 HP
    base_damage = 3 + player_stats["agility"] * 2    # 1 Ловкость = +2 урона
    # Убеждаемся, что текущее здоровье не превышает максимальное
    if player_hp > max_hp:
        player_hp = max_hp
    return max_hp, base_damage

# Сохранение и загрузка

def save_game():
    data = {
        "current_scene": current_scene,
        "inventory": inventory,
        "player_hp": player_hp,
        "player_stats": player_stats
    }
    with open("savegame.json", "w") as f:
        json.dump(data, f)
    screen.blit(background, (0, 0))
    draw_text("Игра сохранена!", 50, 50, screen, font)
    pygame.display.flip()
    pygame.time.wait(1000)

def load_game():
    global current_scene, inventory, player_hp, player_stats
    try:
        with open("savegame.json", "r") as f:
            data = json.load(f)
            current_scene = data["current_scene"]
            inventory = data["inventory"]
            player_hp = data["player_hp"]
            player_stats = data["player_stats"]
        screen.blit(background, (0, 0))
        draw_text("Игра загружена!", 50, 50, screen, font)
        pygame.display.flip()
        pygame.time.wait(1000)
    except FileNotFoundError:
        screen.blit(background, (0, 0))
        draw_text("Сохранение не найдено!", 50, 50, screen, font)
        pygame.display.flip()
        pygame.time.wait(1000)

# Затемнение для переходов

def fade_out():
    fade = pygame.Surface((screen_width, screen_height))
    fade.fill(black)
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.blit(background, (0, 0))
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)

# Переход слайдами

def slide_transition():
    temp_surface = screen.copy()
    for i in range(0, screen_width, 10):
        screen.blit(temp_surface, (-i, 0))
        pygame.display.flip()
        pygame.time.wait(5)

# Текстовая коробка с анимацией

def draw_text_box(text, screen, font, text_color=white, box_color=(0, 0, 0, 150), border_color=(255, 255, 255), padding=20, typing_speed=30, animate=True):
    text_box_width = screen_width - 100
    text_box_height = 440
    text_box_surface = pygame.Surface((text_box_width, text_box_height), pygame.SRCALPHA)
    box_x = (screen_width - text_box_width) // 2
    box_y = screen_height - text_box_height - 5
    pygame.draw.rect(text_box_surface, border_color, (0, 0, text_box_width, text_box_height), 2)
    pygame.draw.rect(text_box_surface, box_color, (2, 2, text_box_width - 4, text_box_height - 4))
    lines = text.splitlines()
    max_lines = (text_box_height - 2 * padding) // (font.get_height() + 5)
    lines = lines[:max_lines]
    if animate:
        rendered_lines = []
        for i, line in enumerate(lines):
            current_text = ""
            for char in line:
                current_text += char
                text_box_surface.fill((0, 0, 0, 0))  # Очищаем поверхность
                pygame.draw.rect(text_box_surface, border_color, (0, 0, text_box_width, text_box_height), 2)
                pygame.draw.rect(text_box_surface, box_color, (2, 2, text_box_width - 4, text_box_height - 4))
                for j, rendered_line in enumerate(rendered_lines):
                    rendered_text = font.render(rendered_line, True, text_color)
                    text_box_surface.blit(rendered_text, (padding, padding + j * (font.get_height() + 5)))
                rendered_text = font.render(current_text, True, text_color)
                text_box_surface.blit(rendered_text, (padding, padding + i * (font.get_height() + 5)))
                screen.blit(background, (0, 0))
                screen.blit(text_box_surface, (box_x, box_y))
                pygame.display.flip()
                pygame.time.wait(typing_speed)
            rendered_lines.append(current_text)
    else:
        rendered_lines = lines

    text_box_surface.fill((0, 0, 0, 0))
    pygame.draw.rect(text_box_surface, border_color, (0, 0, text_box_width, text_box_height), 2)
    pygame.draw.rect(text_box_surface, box_color, (2, 2, text_box_width - 4, text_box_height - 4))
    for i, line in enumerate(rendered_lines):
        rendered_text = font.render(line, True, text_color)
        text_box_surface.blit(rendered_text, (padding, padding + i * (font.get_height() + 5)))
    screen.blit(background, (0, 0))
    screen.blit(text_box_surface, (box_x, box_y))

# Система боя

def battle(enemy_type, player_hp=10, player_damage=base_damage):
    enemy = enemies[enemy_type]
    enemy_hp = enemy["hp"]
    enemy_damage = enemy["damage"]
    running = True
    while running and enemy_hp > 0 and player_hp > 0:
        screen.fill(black)
        draw_text(f"Ваши HP: {player_hp} | HP {enemy['name']}: {enemy_hp}", 50, 100, screen, font)
        draw_text(f"Ваш урон: {player_damage}", 50, 150, screen, font)
        draw_text("1. Атаковать 2. Убежать", 50, 200, screen, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    enemy_hp -= player_damage  # Используем динамический урон
                    player_hp -= enemy_damage
                    if "special" in enemy and random.random() < enemy["special"]["chance"]:
                        player_hp -= enemy["special"]["damage"]
                        draw_text(f"{enemy['name']} использует заклинание! -{enemy['special']['damage']} HP", 50, 150, screen, font)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                elif event.key == pygame.K_2:
                    running = False
                    return "run", player_hp  # Возвращаем текущее здоровье
    return ("win" if enemy_hp <= 0 else "lose"), player_hp

# Враги

enemies = {
    "gnomes": {"hp": 15, "damage": 100, "name": "Гномы"},
    "wolves": {"hp": 10, "damage": 2, "name": "Волки"},
    "cultists": {"hp": 20, "damage": 1, "name": "Культисты", "special": {"chance": 0.2, "damage": 3}}
}

# Не работает

def draw_character(character_name, screen):
    character_images = {
        "Jimmy": "pic/Man_sprite.png",
        "Hazel": "pic/Woman_sprite.png"
    }
    if character_name in character_images:
        character_img = pygame.image.load(character_images[character_name])
        character_img = pygame.transform.scale(character_img, (200, 400))
        screen.blit(character_img, (50, screen_height - 450))

# Меню

def show_menu():
    menu_running = True
    pygame.mixer.music.load('music/Main_Menu.mp3')
    pygame.mixer.music.play(-1)
    button_normal = pygame.image.load("pic/button_normal.png")
    button_hover = pygame.image.load("pic/button_hover.png")
    button_width, button_height = 300, 50
    buttons = [
        {"text": "1. Начать игру", "y": 400},
        {"text": "2. Гайд", "y": 460},
        {"text": "3. Настройки", "y": 520},
        {"text": "4. Сохранить игру", "y": 580},
        {"text": "5. Загрузить игру", "y": 640},
        {"text": "6. Выход", "y": 700}
    ]
    while menu_running:
        screen.blit(background, (0, 0))
        for button in buttons:
            button_img = button_normal
            button_rect = pygame.Rect((screen_width - button_width) // 2, button["y"], button_width, button_height)
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                button_img = button_hover
            button_img = pygame.transform.scale(button_img, (button_width, button_height))
            screen.blit(button_img, ((screen_width - button_width) // 2, button["y"]))
            draw_text(button["text"], (screen_width - button_width) // 2 + 20, button["y"] + 10, screen, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
                elif event.key == pygame.K_1:
                    choice_sound.play()
                    menu_running = False
                    game_loop()
                elif event.key == pygame.K_2:
                    choice_sound.play()
                    show_guide()
                elif event.key == pygame.K_3:
                    choice_sound.play()
                    show_sound_settings()
                elif event.key == pygame.K_6:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_4:
                    choice_sound.play()
                    save_game()
                elif event.key == pygame.K_5:
                    choice_sound.play()
                    load_game()

# Концовки (не работает)

def show_endings():
    endings = [
        "Концовка 1 - Вы победили бандитов.",
        "Концовка 2 - Вы спасли деревню.",
        "Концовка 3 - Вы стали вождём культа.",
    ]
    endings_running = True
    while endings_running:
        screen.fill((30, 30, 30))
        for i, ending in enumerate(endings):
            box_width = screen_width * 0.6
            box_height = screen_height * 0.1
            box_x = (screen_width - box_width) // 2
            box_y = screen_height * 0.2 + i * (box_height + 20)
            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            box_surface.fill((255, 255, 255, 180))
            screen.blit(box_surface, (box_x, box_y))
            draw_text(ending, box_x + 20, box_y + 20, screen, font, color=white)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                endings_running = False

# Отрисовка UI

def draw_hud(player_hp, max_hp, stats, damage):
    draw_text(f"HP: {player_hp}/{max_hp}", 50, 50, screen, font)
    draw_text(f"Урон: {damage}", 50, 100, screen, font)
    draw_text(f"Сила: {stats['strength']} | Ловкость: {stats['agility']} | Интеллект: {stats['intelligence']}", 50, 150, screen, font)

# Не используется

def show_preview():
    screen.fill((0, 0, 0))
    background = pygame.image.load("pic/as.jpg")
    screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
    title_font = pygame.font.Font("font/basis33.ttf", 72)
    pygame.display.flip()
    pygame.time.wait(2590)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Не используется

def show_preview2():
    preview_running = True
    pygame.mixer.music.stop()
    pygame.mixer.Sound("music/preview_sound.mp3").play()
    start_time = pygame.time.get_ticks()
    preview_font = pygame.font.Font("font/basis33.ttf", 82)
    preview_background = pygame.image.load('pic/as.jpg')
    preview_background = pygame.transform.scale(preview_background, (screen_width, screen_height))
    while preview_running:
        screen.blit(preview_background, (0, 0))
        draw_text("",
                  screen_width // 1, screen_height // 1, screen, preview_font, color=white, line_spacing=1.5, center=True)
        pygame.display.flip()
        if pygame.time.get_ticks() - start_time > 1777:
            preview_running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Страница гайда

def show_guide():
    guide_running = True
    guide_background = pygame.image.load("pic/guide.jpg")
    guide_background = pygame.transform.scale(guide_background, (screen_width, screen_height))
    while guide_running:
        screen.blit(guide_background, (0, 0))
        draw_text("Существующая ошибка: Если звук в меню не сохраняется при игре, во время игры выйдите в главное меню 'ESC' и измените параметр звука снова",0, 100, screen, font)
        draw_text("Добро пожаловать в гайд!",50, 100, screen, font)
        draw_text("Управление: Для выборки вариантов ответа необходимо нажимать клавиши 1 - 2 - 3 - 4, в зависимости от желаемого варианта ответа.", 50, 200, screen, font)
        draw_text("Для открытия инвентаря нажмите клавишу 'I'. Для перезапуска игры нужно нажать 'R' Для возвращения в главное меню - 'ESC'", 50, 300, screen, font)
        draw_text("Главное меню:", 50, 400, screen, font)
        draw_text("Для запуска игры необходимо выбрать пункт 1 'Начать игру'", 50, 500, screen, font)
        draw_text("Для сохранения прогресса нужно выйти в главное меню (Клавиша 'ESC') и выбрать пункт 'Сохранить игру''", 50, 600, screen, font)
        draw_text("Для загрузки прогресса необходимо выбрать пункт 'Загрузить игру'", 50, 700, screen, font)
        draw_text("Процесс игры: Для продвижения по сюжету необходимо выбирать интересующие вас варианты ответов указанные в нижней части экрана", 50, 800, screen, font)
        draw_text("Помимо вариантов выбора в нижней части экрана отображается текущая катсцена описывающая происходящее в игре.", 50, 900, screen, font)
        draw_text("В правой верхней части экрана указаны характеристики персонажа (Которые в свою очередь зависят от выборов игрока", 50, 1000, screen, font)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                guide_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                guide_running = False
                show_menu()

def restart_game():
    global current_scene, player_choice
    current_scene = "campaign_choice"
    player_choice = None
    show_menu()

# Страница настроек

def show_sound_settings():
    volume_running = True
    music_volume = pygame.mixer.music.get_volume()
    effects_volume = choice_sound.get_volume()
    # Загружаем фон для меню настроек
    settings_background = pygame.image.load("pic/settings.jpg")
    settings_background = pygame.transform.scale(settings_background, (screen_width, screen_height))

    while volume_running:
        # Отображаем фон вместо сплошного цвета
        screen.blit(settings_background, (0, 0))
        draw_text(f"Громкость музыки: {int(music_volume * 40)}%", 300, 300, screen, font, color=white)
        draw_text(f"Громкость эффектов: {int(effects_volume * 40)}%", 300, 400, screen, font, color=white)
        draw_text("Стрелка вверх/вниз - музыка", 300, 600, screen, font, color=white)
        draw_text("Стрелка влево/вправо - эффекты", 300, 650, screen, font, color=white)
        draw_text("Esc - Вернуться в меню", 300, 700, screen, font, color=white)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                volume_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    volume_running = False
                elif event.key == pygame.K_UP:
                    music_volume = min(1.0, music_volume + 0.1)
                    pygame.mixer.music.set_volume(music_volume)
                elif event.key == pygame.K_DOWN:
                    music_volume = max(0.0, music_volume - 0.1)
                    pygame.mixer.music.set_volume(music_volume)
                elif event.key == pygame.K_RIGHT:
                    effects_volume = min(1.0, effects_volume + 0.1)
                    choice_sound.set_volume(effects_volume)
                elif event.key == pygame.K_LEFT:
                    effects_volume = max(0.0, effects_volume - 0.1)
                    choice_sound.set_volume(effects_volume)

# Игровой цикл

def game_loop():
    global current_scene, player_choice, player_hp
    change_scene_background_and_music(current_scene)
    running = True
    text_animation_done = False

    while running:
        screen.blit(background, (0, 0))
        max_hp, damage = update_player_stats()  # Пересчитываем перед каждым кадром

        if not text_animation_done:
            scene_text = scenes[current_scene]["text"]
            draw_text_box(scene_text, screen, font)
            if current_scene in ["Jimmy", "nachalo_act_4"]:
                draw_character("Jimmy", screen)
            elif current_scene in ["Hazel", "Miranda", "Forest_way"]:
                draw_character("Hazel", screen)
            text_animation_done = True
        else:
            scene_text = scenes[current_scene]["text"]
            draw_text_box(scene_text, screen, font, animate=False)
            choices = scenes[current_scene]["choices"]
            for i, (choice_key, choice_data) in enumerate(choices.items(), 1):
                choice_text = f"{choice_key}. {choice_data['text']}"
                draw_text(choice_text, 50, screen_height - 150 + i * 30, screen, font)

        draw_hud(player_hp, max_hp, player_stats, damage)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    show_menu()
                elif event.key == pygame.K_i:
                    show_inventory(screen, font)
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                   pygame.K_8, pygame.K_9]:
                    player_choice = str(event.key - pygame.K_0)

        if player_choice:
            choices = scenes[current_scene]["choices"]
            if player_choice in choices:
                choice_sound.play()
                choice_data = choices[player_choice]

                if "requirement" in choice_data:
                    for stat, required_value in choice_data["requirement"].items():
                        if player_stats[stat] < required_value:
                            draw_text(
                                f"Не хватает {stat.capitalize()}! Требуется {required_value}, у вас {player_stats[stat]}",
                                50, 400, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(2500)
                            current_scene = choice_data.get("fail_scene", "game_over")
                            change_scene_background_and_music(current_scene)
                            text_animation_done = False
                            player_choice = None
                            continue

                if "effect" in choice_data:
                    for stat, value in choice_data["effect"].items():
                        if stat == "inventory":
                            inventory.append(value)
                            draw_text(f"Вы получили: {value}", 50, 250, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(2500)
                        else:
                            player_stats[stat] += value
                            draw_text(f"+{value} к {stat.capitalize()}!", 50, 300, screen, font)
                            pygame.display.flip()
                            pygame.time.wait(2500)
                            max_hp, damage = update_player_stats()
                            if stat == "strength" and player_hp < max_hp:
                                player_hp = max_hp

# Драки с противниками

                if current_scene == "forest" and player_choice == "2":
                    max_hp, damage = update_player_stats()
                    result, player_hp = battle(enemy_type="gnomes", player_hp=player_hp, player_damage=damage)
                    if result == "win":
                        current_scene = "cave"
                        inventory.append("Гномий кошелёк")
                    elif result == "run":
                        current_scene = "Caves_way"
                    else:
                        current_scene = "game_over"
                    change_scene_background_and_music(current_scene)
                    text_animation_done = False

                elif choice_data["next_scene"] == "restart_game":
                    restart_game()
                    return
                elif choice_data["next_scene"] == "show_menu":
                    show_menu()
                    return
                else:
                    fade_out()
                    current_scene = choice_data["next_scene"]
                    change_scene_background_and_music(current_scene)
                    text_animation_done = False
            player_choice = None