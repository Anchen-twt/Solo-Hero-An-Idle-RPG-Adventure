import random

class Monster:
    def __init__(self, name, hp):
        self.name = name  # 怪物名字
        self.hp = hp  # 怪物生命
    
    # 处理掉落物    
    def drop_item(self):
        if random.random() < 0.25:  # 有25%的概率掉落物品
            return "史莱姆球"
        else:
            return None