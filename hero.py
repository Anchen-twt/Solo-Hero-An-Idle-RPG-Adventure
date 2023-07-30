#hero.py
import time
import random
import threading

class Hero:
    """一个表示英雄的类"""

    def __init__(self, name, level=1, exp=0, gold=0, attack_speed=1):
        """初始化英雄对象"""
        self.name = name  # 勇者名字
        self.level = level  # 勇者等级
        self.exp = exp  # 勇者经验
        self.threshold_exp = 2 ** (self.level - 1) * 10  # 升级所需经验
        self.gold = gold  # 勇者金币
        self.default_attack_speed = attack_speed  #勇者默认攻速
        self.attack_speed = attack_speed  # 勇者当前攻速
        self.base_atk = 10  # 勇者基础攻击
        self.final_atk_bonus = 0  # 勇者最终攻击加成
        self.final_atk = self.level * self.base_atk + self.final_atk_bonus  # 勇者最终攻击
        self.exp_rate = 1.0  # 经验获得倍率
        self.growth_start_time = time.time()  # 成长开始时间
        self.poison_start_time = time.time()  # 毒刃开始时间
        self.output_start_time = time.time()  # 输出开始时间
        self.inventory = []  # 物品栏
    
    def attack(self, monster):
        """攻击怪物"""
        damage = self.final_atk  # 计算伤害值
        monster.hp -= damage  # 减少怪物生命
        self.exp += damage * self.exp_rate  # 增加经验（根据经验获得倍率）
        self.gold += damage  # 增加金币
        self.poison_blade(monster)  # 尝试使用毒刃技能
        self.hunters_might(monster)  # 尝试使用猎杀之力技能
        self.slash(monster)   # 尝试使用连斩技能
    
    def level_up(self):
        """升级"""
        self.threshold_exp = 2 ** (self.level - 1) * 10  # 升级所需经验
        while self.exp >= self.threshold_exp:   # 如果经验达到升级条件 
            self.level +=1   # 升级 
            self.final_atk = self.level *self.base_atk +self.final_atk_bonus   # 更新最终攻击 
            self.exp -= self.threshold_exp   # 减少经验 
            # 处理技能获得 
            self.skill_get = ""
            if self.level >= 10:
                self.skill_get += "成长 "
            if self.level >= 15:
                self.skill_get += "猎杀之力 "
            if self.level >= 20:
                self.skill_get += "毒刃 "
            if self.level >= 25:
                self.skill_get += "连斩 "
            
    def growth(self):
        """使用成长技能"""
        if self.level >= 10:   # 如果等级大于等于10，使用成长技能 
            current_time = time.time()   # 获取当前时间 
            if current_time -self.growth_start_time >= 60:   # 如果距离上次成长超过60秒 
                self.last_skill = "成长"   # 记录使用的技能 
                self.base_atk *= 1.01   # 增加基础攻击1%
                self.final_atk = self.level *self.base_atk + self.final_atk_bonus   # 更新最终攻击 
                self.growth_start_time = current_time   # 更新成长时间

    def hunters_might(self, monster):
        """使用猎杀之力技能"""
        if monster.hp <=0 and self.level >= 15:   # 如果杀死了怪物且等级大于等于15 
            self.last_skill = "猎杀之力"   # 记录使用的技能 
            self.final_atk_bonus += 0.1   # 增加最终攻击加成 
            self.final_atk = self.level *self.base_atk + self.final_atk_bonus   # 更新最终攻击 
    
    def poison_blade(self, monster): 
        """使用毒刃技能"""
        if self.level >= 20:   # 如果等级大于等于20，使用毒刃技能 
            current_time = time.time()   # 获取当前时间 
            if current_time -self.poison_start_time >= 30:   # 如果距离上次使用毒刃超过30秒 
                self.last_skill = "毒刃"   # 记录使用的技能 
                monster.poisoned = True   # 让敌人进入中毒状态 
                monster.poison_damage = self.final_atk *0.3   # 设置每秒中毒伤害 
                monster.poison_duration = 10   # 设置中毒持续时间为10秒
                self.poison_start_time = current_time   # 更新毒刃时间
    
    def slash(self, monster):
        """使用连斩技能"""
        if self.level >= 25:   # 如果等级大于等于25，使用连斩技能 
            chance = random.random()   # 获取随机数 
            if chance <= 0.125:   # 如果随机数小于等于0.125，即12.5%概率 
                self.last_skill = "连斩"   # 记录使用的技能 
                self.attack(monster)   # 再攻击一次 
                self.slash(monster)   # 再尝试触发连斩
    
    def use_item(self, item):
        """管理物品效果"""
        if item == "史莱姆球":
            self.exp_rate += 0.1  # 增加10%经验获得倍率
        elif item == "哥布林之斧":
            self.base_atk += 10  # 增加基础攻击10
        elif item == "龙之心":
            if "龙之力" not in self.skill_get:
                self.skill_get += "龙之力 "  # 添加龙之力技能
            chance = random.random()  # 获取随机数
            count = self.inventory.count("龙之心")  # 获取物品个数
            if chance <= 0.015 * count:  # 如果随机数小于等于概率
                self.last_skill = "龙之心"  # 记录使用的技能
                self.attack_speed = 0.02  # 设置攻速为0.02s/次
                threading.Timer(5, self.reset_attack_speed).start()
                
    def reset_attack_speed(self):
        """恢复攻速"""
        self.attack_speed = self.default_attack_speed
    
    def pick_up_item(self, item):
        """添加物品到物品栏"""
        if item is not None:
            self.inventory.append(item)
            
    def get_inventory_str(self):
        """物品栏合并同类项"""
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