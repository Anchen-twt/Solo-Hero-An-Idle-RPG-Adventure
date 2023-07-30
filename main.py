import time
import threading

from hero import Hero   # 导入hero模块中的Hero类
from monster import monster_types   # 导入monster模块

hero = Hero("勇者", attack_speed=0.05)
monster_name = "史莱姆"  # 默认为史莱姆
monster = monster_types["史莱姆"]

def switch_monster():
    global monster
    global monster_name
    while True:
        monster_name = input("请输入要切换的怪物名称（留空则不切换）：")
        if monster_name in monster_types:
            monster = monster_types[monster_name]
        elif monster_name == "":
            pass
        else:
            print("无效的怪物名称，请重新输入！")

# 创建一个线程来处理玩家的输入
threading.Thread(target=switch_monster).start()

last_attack_time = time.time()
while True:
    time.sleep(0.1)
    
    current_time = time.time()
    if current_time - last_attack_time >= hero.attack_speed:
        hero.attack(monster)
        last_attack_time = current_time
    hero.level_up()
    hero.growth()
    hero.output()

    if monster.hp <= 0:
        item = monster.drop_item()
        # 处理掉落物品
        hero.pick_up_item(item)
        hero.use_item(item)
        monster = monster_types[monster_name]
        monster.reset_hp()  # 生成一个新的怪物