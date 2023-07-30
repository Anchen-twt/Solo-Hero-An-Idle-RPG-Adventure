import random

class Monster:
    def __init__(self, name, default_hp):
        self.name = name  # 怪物名字
        self.default_hp = default_hp
        self.hp = default_hp  # 怪物当前生命
        self.poisoned = False
        
    # 处理掉落物    
    def drop_item(self):
        if self.name == "史莱姆":
            if random.random() < 0.25:  # 有25%的概率掉落物品
                return "史莱姆球"
            else:
                return None
        elif self.name == "哥布林":
            if random.random() < 0.25:  # 有25%的概率掉落物品
                return "哥布林之斧"
        elif self.name == "巨龙":
            if random.random() < 0.25:  # 有25%的概率掉落物品
                return "龙之心"
                
    def reset_hp(self):
        self.hp = self.default_hp
            
monster_types = {
    "史莱姆": Monster("史莱姆", 10000),
    "哥布林": Monster("哥布林", 20000),
    "巨龙": Monster("巨龙", 50000)
}