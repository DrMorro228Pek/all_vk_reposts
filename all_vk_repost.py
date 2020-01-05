# coding: utf8
import vk_api
import re
import random
import time
import os

# Группы которы чекаем
vk_groups = ["-97758272", "-109933725", "-126239339", "-105737219", "-125914421"]

# Кол-во записей которые проверяются, начиная сверху
count = 10

# Авторизация
vk_session = vk_api.VkApi(os.environ.get("LOGIN"), os.environ.get("PASS"))
vk_session.auth()

# Перебираем группы
while True:
    for i in range(len(vk_groups)):
    
        result = vk_session.method("wall.get",{"owner_id" : vk_groups[i], "count" : count, "filter" : "owner"})

        # Перебираем записи
        for j in range(count):
            
            # Получаем текст записи и id записи
            result_text = result["items"][j]["text"].lower()
            result_id = result["items"][j]["id"]
            
            # Видоизменяем для вк
            right_format_post_id = "wall" + vk_groups[i] + "_" + str(result_id)
            
            # Проверка на повторение
            f1 = open("yetUsed.txt","r+", encoding="utf-8")
            flag = False
            for line in f1:
                if right_format_post_id == line.strip():
                    flag = True
                    print(right_format_post_id + " уже репостилось")
                    break
            if flag:
                continue
            
            # Проверка на присутствие слов из белого списка
            f2 = open("whiteList.txt", "r+", encoding="utf-8")
            for line in f2:
                if result_text.find(line.strip()) == -1:
                    flag = True
                else:
                    flag = False
                    print("Есть слово " + line)
                    break
            if flag:
                continue
                    
            # Если не прошла проверки, переходим к следующей записе
            f2.close()
            
            # Если запись прошла проверки на повторение, то добавляем в уже зарепощенные
            f1.write(right_format_post_id + "\n")
            f1.close()
            
            # Ищем спонсорскую группу и подписываемся на нее и делаем репост
            r = r"\d{9}"
            sponsor_group_id = re.findall(r, result_text)[0]
            
            #     Вступаем
            try:
                vk_session.method("groups.join", {"group_id" : sponsor_group_id})
            except:
                pass
            
            # Вывод доп инфы
            print("=======================================")
            print(result_text + "\n\n")
            print("=======================================")            
            
            #     Делаем репост
            try:
                vk_session.method("wall.repost", {"object" : right_format_post_id })
            except:
                print("Достигнут лимит записей (>50)")
                time.sleep(7200)
                continue
            
            print("Репостнул " + right_format_post_id + "и вступил в группу " + sponsor_group_id + "\n" )
            
            # Кд для записей
            time.sleep(120.0+random.random()*200.0)
    
    # Чекать раз в час        
    time.sleep(3600)