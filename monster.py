import random

class Monster:
    def __init__(self, name, hp):
        self.name = name  # 怪物名字
        self.hp = hp  # 怪物生命
    
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
            
monster_types = {
    "史莱姆": Monster("史莱姆", 10000),
    "哥布林": Monster("哥布林", 20000),
    "巨龙": Monster("巨龙", 50000)
}