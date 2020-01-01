import vk_api
import data
import json
import re
import random
import time
import os

# ������ ������ ������
vk_groups = ["-97758272", "-109933725", "-126239339", "-105737219", "-125914421"]

# ���-�� ������� ������� �����������, ������� ������
count = 10

# �����������
vk_session = vk_api.VkApi(os.environ.get("LOGIN"), os.environ.get("PASS"))
vk_session.auth()

# ���������� ������
while True:
    for i in range(len(vk_groups)):
    
        result = vk_session.method("wall.get",{"owner_id" : vk_groups[i], "count" : count, "filter" : "owner"})

        # ���������� ������
        for j in range(count):
            
            # �������� ����� ������ � id ������
            result_text = result["items"][j]["text"].lower()
            result_id = result["items"][j]["id"]
            
            # ������������ ��� ��
            right_format_post_id = "wall" + vk_groups[i] + "_" + str(result_id)
            
            # �������� �� ����������
            f1 = open("yetUsed.txt","r+", encoding="utf-8")
            flag = False
            for line in f1:
                if right_format_post_id == line.strip():
                    flag = True
                    print(right_format_post_id + " ��� �����������")
                    break
            if flag:
                continue
            
            # �������� �� ����������� ���� �� ������ ������
            f2 = open("whiteList.txt", "r+", encoding="utf-8")
            for line in f2:
                if result_text.find(line.strip()) == -1:
                    flag = True
                else:
                    flag = False
                    print("���� ����� " + line)
                    break
            if flag:
                continue
                    
            # ���� �� ������ ��������, ��������� � ��������� ������
            f2.close()
            
            # ���� ������ ������ �������� �� ����������, �� ��������� � ��� ������������
            f1.write(right_format_post_id + "\n")
            f1.close()
            
            # ���� ����������� ������ � ������������� �� ��� � ������ ������
            r = r"\d{9}"
            sponsor_group_id = re.findall(r, result_text)[0]
            
            #     ��������
            try:
                vk_session.method("groups.join", {"group_id" : sponsor_group_id})
            except:
                pass
            
            # ����� ��� ����
            print("=======================================")
            print(result_text + "\n\n")
            print("=======================================")            
            
            #     ������ ������
            vk_session.method("wall.repost", {"object" : right_format_post_id })
            
            print("��������� " + right_format_post_id + "� ������� � ������ " + sponsor_group_id + "\n" )
            
            # �� ��� �������
            time.sleep(120.0+random.random()*200.0)
    
    # ������ ��� � ���        
    time.sleep(3600)