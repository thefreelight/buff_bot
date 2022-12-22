import time
import re
import os
import getpass
import random

import sqlite3

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.win.win import *


from poco.drivers.android.uiautomation import AndroidUiautomationPoco




#带参数的精确查询
def query(sql,*keys):
    db = conn
    cursor = db.cursor()
    cursor.execute(sql,keys)
    result = cursor.fetchall()
    cursor.close()
    return result

#不带参数的模糊查询
def query2(sql):
    db = conn
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

#获取当前时间
def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

#更新数据库
def update(sql):
    db = conn
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except:
        #发生错误时回滚
        db.rollback()




#判断文件是否存在
def is_txt_exists(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            f = open(filename, 'r', encoding='utf-8')
            return f
    else:
        with open(filename, 'w+', encoding='utf-8') as f:
            print('文件创建成功')
            f = open(filename, 'r', encoding='utf-8')
            return f


#生成安卓模拟器地址
def creat_android_list(number):
    base_port = 21503
    base_url = 'Android:///127.0.0.1:'
    android_list = []
    for i in range(int(number)):
        new_port = base_port + 10*i
        android_url = base_url + str(new_port)
        android_list.append(android_url)
        i = i + 1
    return android_list


# 往上滑
def up(poco):
    xy = poco.get_screen_size()
    x = xy[0]
    y = xy[1]
    swipe([x * 0.5, y * 0.9], [x * 0.5, y * 0.82])

#往左滑
def left(poco):
    xy = poco.get_screen_size()
    x = xy[0]
    y = xy[1]
    swipe([x * 0.8, y * 0.5], [x * 0.2, y * 0.5])


#生成vcf
def txt_turn_vcf(filename,number):
    with open(filename, encoding='utf-8') as f:
        res = f.readlines()
    faker = Faker()
    username = getpass.getuser()
    for i in range(int(number)):
            path = 'C:/Users/' + username + '/Pictures/逍遥安卓照片/'
            if os.path.exists(path):
                with open(path + f"{i}.vcf","w",encoding='utf-8')as v:
                    for r in res[500*i : 500*(i+1)]:
                        name = faker.name()
                        nn = r.split(",")
                        v.write("BEGIN:VCARD"+"\n")
                        v.write("VERSION:2.1"+"\n")
                        v.write("FN:"+name+"\n")
                        v.write("TEL;CELL:+"+nn[0])
                        v.write("END:VCARD"+"\n")
                    print('转换完成')
            else:
                print('请检查路径是否正确')

#导入通讯录
def upload_contacts(number,poco):
    poco(text='通讯录').click()
    poco("更多选项").click()
    poco(text="导入/导出").click()
    poco(text="从 .vcf 文件导入").click()
    left(poco)
    poco("更多选项").click()
    if poco(text="显示内部存储设备"):
        poco(text="显示内部存储设备").click()
        poco("显示根目录").click()
        poco(text="DUK-AL20").click()
        poco(text="Pictures").click()
        poco(text=f'{number}.vcf').click()
    elif poco(text='隐藏内部存储设备'):
        keyevent('BACK')
        poco("显示根目录").click()
        poco(text="DUK-AL20").click()
        poco(text="Pictures").click()
        poco(text=f'{number}.vcf').click()

#好友群发
def friends_sender(poco,second,number,text):
    poco(text='WhatsApp').click()
    time.sleep(1)
    poco("com.whatsapp:id/fab").click()
    time.sleep(1)
    for i in range(0,number):
        poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring(
            "com.whatsapp:id/root_layout").offspring("android:id/list").child("android.widget.RelativeLayout")[i].child(
            "com.whatsapp:id/contactpicker_text_container").click()
        time.sleep(1)
        shell(f"input text '{text}'")
        time.sleep(1)
        poco("com.whatsapp:id/send").click()
        time.sleep(1)
        i = i + 1
        keyevent('BACK')
        time.sleep(random.randint(0,second))
        poco("com.whatsapp:id/fab").click()
        time.sleep(1)
        up()















