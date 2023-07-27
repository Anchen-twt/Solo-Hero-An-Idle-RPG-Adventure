import time

from hero import Hero   # 导入hero模块中的Hero类
from monster import Monster   # 导入monster模块中的Monster类

hero = Hero("勇者", attack_speed=0.01)  
monster = Monster("史莱姆", 10000000)  

last_attack_time = time.time()  
while monster.hp > 0:  
    current_time = time.time()  
    if current_time - last_attack_time >= hero.attack_speed:  
        hero.attack(monster)  
        last_attack_time = current_time  
        hero.slash(monster)  
    hero.level_up()  
    hero.growth()  
    hero.output()