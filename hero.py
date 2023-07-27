import time
import random

class Hero:
    def __init__(self, name, level=1, exp=0, gold=0, attack_speed=1):
        self.name = name  # 勇者名字
        self.level = level  # 勇者等级
        self.exp = exp  # 勇者经验
        self.gold = gold  # 勇者金币
        self.attack_speed = attack_speed  # 勇者攻速
        self.base_damage = 10  # 勇者基础伤害
        self.growth_start_time = time.time()  # 成长开始时间
        self.output_start_time = time.time()  # 输出开始时间
        self.total_damage = 0  # 总输出

    def attack(self, monster):
        damage = self.level * self.base_damage  # 计算伤害
        monster.hp -= damage  # 减少怪物生命
        self.exp += damage  # 增加经验
        self.gold += damage  # 增加金币
        self.total_damage += damage  # 增加总输出

    def level_up(self):
        threshold_exp = 2 ** (self.level - 1) * 10
        while self.exp >= threshold_exp:  # 如果经验达到升级条件
            self.level += 1  # 升级
            self.exp -= threshold_exp  # 减少经验
            print(f"{self.name} 升级了！现在是 {self.level} 级。")
            # 处理技能获得
            if self.level == 10:
                print(f"{self.name} 获得了技能成长！")
            elif self.level == 25:
                print(f"{self.name} 获得了技能连斩！")
                	
    def growth(self):
        if self.level >= 10:  # 如果等级大于等于10，使用成长技能
            current_time = time.time()  # 获取当前时间
            if current_time - self.growth_start_time >= 60:  # 如果距离上次成长超过60秒
                self.base_damage *= 1.01  # 增加基础伤害1%
                print(f"{self.name} 的成长发动了！现在的基础伤害是 {self.base_damage}。")
                self.growth_start_time = current_time  # 更新成长时间

    def slash(self, monster):
        if self.level >= 25:  # 如果等级大于等于25，使用连斩技能
            chance = random.random()  # 获取随机数
            if chance <= 0.125:  # 如果随机数小于等于0.125，即12.5%概率
                print(f"{self.name} 触发了连斩！")
                self.attack(monster)  # 再攻击一次
                self.slash(monster)   # 再尝试触发连斩

    def output(self):
        current_time = time.time()  # 获取当前时间
        if current_time - self.output_start_time >= 10:  # 如果距离上次输出超过10秒
            print(f"{self.name} 在过去的10秒内总共造成了 {self.total_damage} 点伤害！")
            self.output_start_time = current_time  # 更新输出时间
            self.total_damage = 0  # 清零总输出