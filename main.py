import pygame
import random
import threading
from hero import Hero
from monster import monster_factory

pygame.init()

# 设置游戏界面
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
FPS = 30

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
Cyan = (0, 255, 255)
BLUE = (0, 0, 255)

# 创建游戏界面
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("一人勇者")

# 加载字体（替换成你下载的中文字体文件名）
font_file = "锐字潮牌燕尾宋.ttf"
font = pygame.font.Font(font_file, 25)

class Game:
    def __init__(self, hero_name, hero_attack_speed, monster_name):
        self.hero = Hero(hero_name, attack_speed=hero_attack_speed)
        self.monster_types = list(monster_factory.monster_types.keys())
        self.current_monster_index = self.monster_types.index(monster_name)
        self.monster = monster_factory.create_monster(monster_name)
        self.monster_name = monster_name
        # 加载怪物图像并将它们与怪物名称关联
        self.monster_images = {
            "史莱姆": pygame.image.load("images/史莱姆.png"),
            "哥布林": pygame.image.load("images/哥布林.png"),
            "巨龙": pygame.image.load("images/巨龙.png")
        }

        # 根据提供的怪物名称设置初始怪物图像
        self.monster_image = self.monster_images[monster_name]
        self.create_button()

        # 启动游戏逻辑
        self.hero_timer = threading.Timer(self.hero.attack_speed, self.hero_attack)
        self.hero_timer.start()

    def create_button(self):
        # 创建切换怪物的按钮
        self.button_rect = pygame.Rect(270, 220, 100, 50)
        self.button_text = font.render("切换怪物", True, BLACK)
    
        
    def draw(self):
        # 绘制游戏界面
        screen.fill(WHITE)

        # 绘制英雄信息
        name_text = font.render(f"名称：{self.hero.name}", True, BLACK)
        level_text = font.render(f"等级：{self.hero.level}", True, BLACK)
        exp_text = font.render(f"经验：{self.hero.exp:.2f}/{self.hero.threshold_exp:.0f}", True, BLACK)
        gold_text = font.render(f"金币：{self.hero.gold}", True, BLACK)
        base_attack_text = font.render(f"基础攻击：{self.hero.base_atk}", True, BLACK)
        final_attack_text = font.render(f"最终攻击：{self.hero.final_atk}", True, BLACK)
        attack_speed_text = font.render(f"攻速：{self.hero.attack_speed:.2f}", True, BLACK)
        exp_rate_text = font.render(f"经验提升倍率：{self.hero.exp_rate:.2f}", True, BLACK)
        items_text = font.render(f"物品栏：{self.hero.get_inventory_str()}", True, BLACK)
        skills_text = font.render(f"获得技能：{self.hero.skill_get}", True, BLACK)
        
        # 绘制升级进度条
        progress = self.hero.exp / self.hero.threshold_exp
        pygame.draw.rect(screen, BLACK, (50, 340, 300, 20))
        pygame.draw.rect(screen, (0, 255, 0), (50, 340, 300 * progress, 20))
        
        # 绘制英雄信息文本
        screen.blit(name_text, (50, 30))
        screen.blit(level_text, (50, 60))
        screen.blit(exp_text, (50, 90))
        screen.blit(gold_text, (50, 120))
        screen.blit(base_attack_text, (50, 150))
        screen.blit(final_attack_text, (50, 180))
        screen.blit(attack_speed_text, (50, 210))
        screen.blit(exp_rate_text, (50, 240))
        screen.blit(items_text, (50, 270))
        screen.blit(skills_text, (50, 300))
              
        # 绘制当前怪物信息
        monster_text = font.render(f"当前怪物：{self.monster_name}", True, BLACK)
        screen.blit(monster_text, (50, 360))

        # 绘制怪物图像
        screen.blit(self.monster_image, (50, 350))  # 调整怪物图像显示位置
        
        # 绘制切换怪物按钮
        pygame.draw.rect(screen, Cyan, self.button_rect)
        screen.blit(self.button_text, (280, 235))

    def hero_attack(self):
        self.hero.attack(self.monster)
        self.hero.level_up()

        if self.monster.hp <= 0:
            item = self.monster.drop_item()
            self.hero.pick_up_item(item)
            self.hero.use_item(item)
            self.monster = monster_factory.create_monster(self.monster_name)
            self.monster.reset_hp()

        self.hero_timer = threading.Timer(self.hero.attack_speed, self.hero_attack)
        self.hero_timer.start()
    
    def switch_monster(self):
        self.current_monster_index = (self.current_monster_index + 1) % len(self.monster_types)
        self.monster_name = self.monster_types[self.current_monster_index]
        self.monster = monster_factory.create_monster(self.monster_name)
        self.monster.reset_hp()
        
        # 根据新的怪物名称设置当前怪物图像
        self.monster_image = self.monster_images[self.monster_name]
    
# 创建一个游戏对象
game = Game("勇者", hero_attack_speed=0.02, monster_name="史莱姆")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.button_rect.collidepoint(event.pos):
                game.switch_monster()
    
    # 调用英雄的成长技能
    game.hero.growth()
    
    # 更新界面
    game.draw()
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

pygame.quit()