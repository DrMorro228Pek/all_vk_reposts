# coding: utf8
import vk_api
import json
import re
import random
import time
import os

# Ãðóïïû êîòîðû ÷åêàåì
vk_groups = ["-97758272", "-109933725", "-126239339", "-105737219", "-125914421"]

# Êîë-âî çàïèñåé êîòîðûå ïðîâåðÿþòñÿ, íà÷èíàÿ ñâåðõó
count = 10

# Àâòîðèçàöèÿ
vk_session = vk_api.VkApi(os.environ.get("LOGIN"), os.environ.get("PASS"))
vk_session.auth()

# Ïåðåáèðàåì ãðóïïû
while True:
    for i in range(len(vk_groups)):
    
        result = vk_session.method("wall.get",{"owner_id" : vk_groups[i], "count" : count, "filter" : "owner"})

        # Ïåðåáèðàåì çàïèñè
        for j in range(count):
            
            # Ïîëó÷àåì òåêñò çàïèñè è id çàïèñè
            result_text = result["items"][j]["text"].lower()
            result_id = result["items"][j]["id"]
            
            # Âèäîèçìåíÿåì äëÿ âê
            right_format_post_id = "wall" + vk_groups[i] + "_" + str(result_id)
            
            # Ïðîâåðêà íà ïîâòîðåíèå
            f1 = open("yetUsed.txt","r+", encoding="utf-8")
            flag = False
            for line in f1:
                if right_format_post_id == line.strip():
                    flag = True
                    print(right_format_post_id + " óæå ðåïîñòèëîñü")
                    break
            if flag:
                continue
            
            # Ïðîâåðêà íà ïðèñóòñòâèå ñëîâ èç áåëîãî ñïèñêà
            f2 = open("whiteList.txt", "r+", encoding="utf-8")
            for line in f2:
                if result_text.find(line.strip()) == -1:
                    flag = True
                else:
                    flag = False
                    print("Åñòü ñëîâî " + line)
                    break
            if flag:
                continue
                    
            # Åñëè íå ïðîøëà ïðîâåðêè, ïåðåõîäèì ê ñëåäóþùåé çàïèñå
            f2.close()
            
            # Åñëè çàïèñü ïðîøëà ïðîâåðêè íà ïîâòîðåíèå, òî äîáàâëÿåì â óæå çàðåïîùåííûå
            f1.write(right_format_post_id + "\n")
            f1.close()
            
            # Èùåì ñïîíñîðñêóþ ãðóïïó è ïîäïèñûâàåìñÿ íà íåå è äåëàåì ðåïîñò
            r = r"\d{9}"
            sponsor_group_id = re.findall(r, result_text)[0]
            
            #     Âñòóïàåì
            try:
                vk_session.method("groups.join", {"group_id" : sponsor_group_id})
            except:
                pass
            
            # Âûâîä äîï èíôû
            print("=======================================")
            print(result_text + "\n\n")
            print("=======================================")            
            
            #     Äåëàåì ðåïîñò
            vk_session.method("wall.repost", {"object" : right_format_post_id })
            
            print("Ðåïîñòíóë " + right_format_post_id + "è âñòóïèë â ãðóïïó " + sponsor_group_id + "\n" )
            
            # Êä äëÿ çàïèñåé
            time.sleep(120.0+random.random()*200.0)
    
    # ×åêàòü ðàç â ÷àñ        
    time.sleep(3600)
