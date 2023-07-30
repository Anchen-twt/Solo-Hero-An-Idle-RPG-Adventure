import time
import threading

from hero import Hero   # 导入hero模块中的Hero类
from monster import monster_factory   # 导入monster模块中的monster_factory对象

class Game:
    """一个简单的游戏类，包含英雄和怪物对象，以及游戏逻辑"""

    def __init__(self, hero_name, hero_attack_speed, monster_name):
        """初始化游戏对象"""
        self.output_speed = 0.01
        self.hero = Hero(hero_name, attack_speed=hero_attack_speed)  # 创建英雄对象
        self.monster = monster_factory.create_monster(monster_name)  # 创建怪物对象
        self.monster_name = monster_name  # 记录当前怪物名称
        self.hero_timer = None  # 创建英雄定时器对象
        self.output_timer = None  # 创建输出定时器对象
    
    def print_progress_bar(self, progress):
        """打印进度条"""
        symbol = '▷'
        if progress > 0.5:
            symbol = '▶'
        percents = round(100.0 * progress, 1)
        print(f'[{self.hero.exp:.0f}/{self.hero.threshold_exp:.0f}] {symbol} {percents}%')
    
    def output(self):
        """输出英雄信息"""           
        print("\033[2J\033[H")  # 清屏并将光标移动到左上角
        print("# 勇者信息")
        print(f"名称：{self.hero.name}")
        print(f"等级：{self.hero.level}")
        progress = self.hero.exp / self.hero.threshold_exp
        print(f"经验：{self.hero.exp:.2f}")
        self.print_progress_bar(progress)
        print(f"金币：{self.hero.gold}")
        print(f"攻击：{self.hero.final_atk}")
        print(f"攻速：{self.hero.attack_speed:.2f}")
        print("## 技能信息")
        if hasattr(self.hero, "skill_get"):
            print(f"你获得的技能：{self.hero.skill_get}")
        if hasattr(self.hero, "last_skill"):
            print(f"你使用了技能：{self.hero.last_skill}")
        print("## 物品信息")
        print(self.hero.get_inventory_str())
        
        self.output_timer = threading.Timer(self.output_speed, self.output)  # 创建一个新的输出定时器对象，每隔一定时间执行一次output()方法
        self.output_timer.start()  # 启动输出定时器
        
    def switch_monster(self):
        """切换当前怪物"""
        while True:
            monster_name = input("请输入要切换的怪物名称（留空则不切换）：").strip()  # 去除输入中可能存在的空格或换行符
            try:
                if monster_name in monster_factory.monster_types:  # 如果输入了有效的怪物名称
                    self.monster = monster_factory.create_monster(monster_name)  # 切换当前怪物对象
                    self.monster_name = monster_name  # 更新当前怪物名称
                    self.monster.reset_hp()  # 重置当前怪物血量
                elif monster_name == "":  # 如果输入为空
                    pass  # 不做任何操作
                else:  # 如果输入了无效的怪物名称
                    raise ValueError("无效的怪物名称，请重新输入！")  # 抛出异常
            except ValueError as e:  # 捕获并处理异常
                print(e)  # 打印异常信息

    def hero_attack(self):
        """英雄攻击当前怪物"""
        self.hero.attack(self.monster)  # 调用英雄的攻击方法
        self.hero.level_up()  # 调用英雄的升级方法
        self.hero.growth()  # 调用英雄的成长方法

        if self.monster.hp <= 0:  # 如果当前怪物死亡
            item = self.monster.drop_item()  # 获取当前怪物掉落的物品
            # 处理掉落物品
            self.hero.pick_up_item(item)  # 调用英雄的拾取物品方法
            self.hero.use_item(item)  # 调用英雄的使用物品方法
            self.monster = monster_factory.create_monster(self.monster.name)  # 切换当前怪物对象
            self.monster.reset_hp()  # 重置当前怪物血量

        self.hero_timer = threading.Timer(self.hero.attack_speed, self.hero_attack)  # 创建一个新的英雄定时器对象，每隔一定时间执行一次英雄攻击方法
        self.hero_timer.start()  # 启动英雄定时器

    def start(self):
        """开始游戏"""
        print("游戏开始！")
        threading.Thread(target=self.switch_monster).start()  # 创建一个线程来处理玩家的输入
        self.hero_timer = threading.Timer(self.hero.attack_speed, self.hero_attack)  # 创建一个英雄定时器对象，每隔一定时间执行一次英雄攻击方法
        self.hero_timer.start()  # 启动英雄定时器
        self.output_timer = threading.Timer(self.output_speed, self.output)  # 创建一个输出定时器对象，每隔一定时间更新界面
        self.output_timer.start()  # 启动输出定时器
        
    def stop(self):
        """停止游戏"""
        print("游戏结束！")
        if self.hero_timer:  # 如果存在英雄定时器对象
            self.hero_timer.cancel()  # 取消英雄定时器
        if self.output_timer:  # 如果存在输出定时器对象
            self.output_timer.cancel()  # 取消输出定时器


if __name__ == "__main__":
    game = Game("勇者", hero_attack_speed = 2, monster_name="史莱姆")  # 创建一个游戏对象，指定英雄名称，攻击速度和初始怪物名称
    game.start()  # 开始游戏