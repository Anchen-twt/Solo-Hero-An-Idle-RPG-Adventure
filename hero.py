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
        self.exp_rate = 1.0  # 经验获得倍率
        self.growth_start_time = time.time()  # 成长开始时间
        self.output_start_time = time.time()  # 输出开始时间
        self.total_damage = 0  # 总输出
        self.kill_count = 0  # 杀怪数
        self.level_up_count = 0  # 升级数
        self.inventory = []  # 物品栏

    def attack(self, monster):
        damage = self.level * self.base_damage  # 计算伤害
        monster.hp -= damage  # 减少怪物生命
        if monster.hp <= 0:
            self.kill_count += 1  # 增加杀怪数
        self.exp += damage * self.exp_rate  # 增加经验（根据经验获得倍率）
        self.gold += damage  # 增加金币
        self.total_damage += damage  # 增加总输出
        self.hunters_might(monster)
        self.slash(monster)
    
    def level_up(self):
        threshold_exp = 2 ** (self.level - 1) * 10
        while self.exp >= threshold_exp:  # 如果经验达到升级条件
            self.level += 1  # 升级
            self.exp -= threshold_exp  # 减少经验
            self.level_up_count += 1  # 增加升级数
            # 处理技能获得
            if self.level == 10:
                print(f"{self.name} 获得了技能成长！")
            elif self.level == 15:
                print(f"{self.name} 获得了技能猎杀之力！")
            elif self.level == 25:
                print(f"{self.name} 获得了技能连斩！")
                	
    def growth(self):
        if self.level >= 10:  # 如果等级大于等于10，使用成长技能
            current_time = time.time()  # 获取当前时间
            if current_time - self.growth_start_time >= 60:  # 如果距离上次成长超过60秒
                self.base_damage *= 1.01  # 增加基础伤害1%
                print(f"{self.name} 的成长发动了！现在的基础伤害是 {self.base_damage:.2f}。")
                self.growth_start_time = current_time  # 更新成长时间

    def hunters_might(self, monster):
        if monster.hp <= 0 and self.level >= 15:  # 如果杀死了怪物且等级大于等于15
            self.base_damage += 1  # 增加基础伤害
            print(f"{self.name} 的猎杀之力发动了！现在的基础伤害是 {self.base_damage}。")
    
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
            print("「")
            print(f"{self.name} 在过去的10秒内总共造成了 {self.total_damage:.2f} 点伤害！")
            print(f"{self.name} 在过去的10秒内总共杀死了 {self.kill_count} 只怪物！")
            print(f"{self.name} 在过去的10秒内总共升级了 {self.level_up_count} 次！")
            print(f"{self.name} 现在是 {self.level} 级！")
            print(f"{self.name} 在过去的10秒内总共获得了 {len(self.inventory)} 个战利品！")
            print(f"{self.name} 的物品栏是 {self.get_inventory_str()}。")
            print("」")
            self.output_start_time = current_time  # 更新输出时间
            self.total_damage = 0  # 清零总输出
            self.kill_count = 0   # 清零杀怪数
            self.level_up_count = 0   # 清零升级数
    
    def use_item(self, item):
        if item == "史莱姆球":
            self.exp_rate *= 1.01  # 增加1%经验获得倍率            
            print(f"{self.name} 捡起了 {item}，现在的经验获得倍率是 {self.exp_rate:.2f}。")
    
    def pick_up_item(self, item):
        if item is not None:
            self.inventory.append(item)  # 添加物品到物品栏
            

    def get_inventory_str(self):
        inventory_str = ""
        item_count = {}
        for item in self.inventory:
            if item in item_count:
                item_count[item] += 1
            else:
                item_count[item] = 1
        for item, count in item_count.items():
            inventory_str += f"{item}*{count}, "
        return inventory_str[:-2]