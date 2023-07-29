import time
import random

class Hero:
    def __init__(self, name, level=1, exp=0, gold=0, attack_speed=1):
        self.name = name  # 勇者名字
        self.level = level  # 勇者等级
        self.exp = exp  # 勇者经验
        self.gold = gold  # 勇者金币
        self.attack_speed = attack_speed  # 勇者攻速
        self.base_atk = 10  # 勇者基础攻击
        self.final_atk = self.level * self.base_atk
        self.final_atk_bonus = 0
        self.exp_rate = 1.0  # 经验获得倍率
        self.growth_start_time = time.time()  # 成长开始时间
        self.output_start_time = time.time()  # 输出开始时间
        self.inventory = []  # 物品栏

    def attack(self, monster):
        damage = self.final_atk
        monster.hp -= damage  # 减少怪物生命
        self.exp += damage * self.exp_rate  # 增加经验（根据经验获得倍率）
        self.gold += damage  # 增加金币
        self.hunters_might(monster)
        self.slash(monster)
    
    def level_up(self):
        self.threshold_exp = 2 ** (self.level - 1) * 10
        while self.exp >= self.threshold_exp:  # 如果经验达到升级条件
            self.level += 1  # 升级
            self.final_atk = self.level * self.base_atk  # 更新最终攻击
            self.exp -= self.threshold_exp  # 减少经验
            # 处理技能获得
            self.skill_get = ""
            if self.level >= 10:
                self.skill_get += "成长 "
            if self.level >= 15:
                self.skill_get += "猎杀之力 "
            if self.level >= 25:
                self.skill_get += "连斩 "
                	
    def growth(self):
        if self.level >= 10:  # 如果等级大于等于10，使用成长技能
            current_time = time.time()  # 获取当前时间
            if current_time - self.growth_start_time >= 60:  # 如果距离上次成长超过60秒
                self.last_skill = "成长"  # 记录使用的技能
                self.base_atk *= 1.01  # 增加基础攻击1%
                self.growth_start_time = current_time  # 更新成长时间

    def hunters_might(self, monster):
        if monster.hp <= 0 and self.level >= 15:  # 如果杀死了怪物且等级大于等于15
            self.last_skill = "猎杀之力"  # 记录使用的技能
            self.final_atk_bonus += 1  # 增加最终攻击
    
    def slash(self, monster):
        if self.level >= 25:  # 如果等级大于等于25，使用连斩技能
            chance = random.random()  # 获取随机数
            if chance <= 0.125:  # 如果随机数小于等于0.125，即12.5%概率
                self.last_skill = "连斩"  # 记录使用的技能
                self.attack(monster)  # 再攻击一次
                self.slash(monster)   # 再尝试触发连斩
    
    def output(self):
        current_time = time.time()
        if current_time - self.output_start_time >= 0.3:
            print("\033[2J\033[H")  # 清屏并将光标移动到左上角
            print(f"勇者：{self.name}")
            print(f"等级：{self.level}")
            progress = int(self.exp / self.threshold_exp * 20)
            print(f"经验：{self.exp:.2f} [{'#' * progress}{'.' * (20 - progress)}]")
            print(f"金币：{self.gold}")
            print(f"攻速：{self.attack_speed:.2f}")
            print(f"基础攻击：{self.base_atk:.2f}")
            print(f"最终攻击：{self.final_atk:.2f}")
            print(f"经验获得倍率：{self.exp_rate:.2f}")
            print(f"物品栏：{self.get_inventory_str()}")
            if hasattr(self, 'skill_get'):
                print(f"获得技能：{self.skill_get}")
            if hasattr(self, 'last_skill'):
                print(f"使用技能：{self.last_skill}")
            self.output_start_time = current_time
            
    def use_item(self, item):
        if item == "史莱姆球":
            self.exp_rate += 0.01  # 增加1%经验获得倍率
        elif item == "哥布林之斧":
            self.base_atk += 0.1
    
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