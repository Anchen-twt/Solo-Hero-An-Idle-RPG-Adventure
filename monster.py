import random

class Monster:
    """一个表示怪物的类"""

    def __init__(self, name, default_hp):
        """初始化怪物对象"""
        self.name = name  # 怪物名字
        self.default_hp = default_hp  # 怪物默认生命
        self.hp = default_hp  # 怪物当前生命
        self.poisoned = False  # 怪物是否中毒
        
    def drop_item(self):
        """处理掉落物"""
        if self.name == "史莱姆":
            if random.random() < 0.25:  # 有25%的概率掉落物品
                return "史莱姆球"
            else:
                return None
        elif self.name == "哥布林":
            if random.random() < 0.25:  # 有25%的概率掉落物品
                return "哥布林之斧"
            else:
                return None
        elif self.name == "巨龙":
            if random.random() < 0.25:  # 有25%的概率掉落物品
                return "龙之心"
            else:
                return None
                
    def reset_hp(self):
        """重置当前生命"""
        self.hp = self.default_hp



class MonsterFactory:
    """一个创建怪物对象的工厂类"""

    def __init__(self):
        """初始化工厂对象"""
        self.monster_types = {}  # 创建一个空字典，用来存储不同类型的怪物对象

    def register_monster(self, name, default_hp):
        """注册一个新的怪物类型"""
        self.monster_types[name] = Monster(name, default_hp)  # 创建并存储一个怪物对象

    def create_monster(self, name):
        """根据给定的怪物名称，创建并返回一个怪物对象"""
        if name in self.monster_types:  # 如果存在该类型的怪物
            return self.monster_types[name]  # 返回对应的怪物对象
        else:  # 如果不存在该类型的怪物
            raise ValueError(f"无效的怪物名称：{name}")  # 抛出异常


# 创建一个怪物工厂对象
monster_factory = MonsterFactory()

# 注册三种类型的怪物
monster_factory.register_monster("史莱姆", 10000)
monster_factory.register_monster("哥布林", 20000)
monster_factory.register_monster("巨龙", 50000)

