import subprocess
import time
import random

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.win.win import *
from airtest.core.android.android import *

from config.base import query, current_time, update, is_txt_exists, creat_android_list, up, txt_turn_vcf, \
    upload_contacts

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

auto_setup(__file__)

dev = connect_device("Android:///127.0.0.1:21563")
poco = AndroidUiautomationPoco(device=dev, use_airtest_input=True, screenshot_each_action=False)


# poco(text='WhatsApp').click()
# time.sleep(1)
# poco("com.whatsapp:id/fab").click()
# time.sleep(1)
# poco("com.whatsapp:id/menuitem_search").click()
# time.sleep(1)
# shell("input text 'Angela' ")
# time.sleep(1)
# poco(text="Angela Singleton").click()
# poco("com.whatsapp:id/entry").click()
# time.sleep(1)
# shell("input text 'Hello' ")
# time.sleep(1)
# poco("com.whatsapp:id/send").click()
# time.sleep(1)
# keyevent('Back')

# 往上滑
def up():
    xy = poco.get_screen_size()
    x = xy[0]
    y = xy[1]
    swipe([x * 0.5, y * 0.9], [x * 0.5, y * 0.82])


# 往下滑
def down():
    xy = poco.get_screen_size()
    x = xy[0]
    y = xy[1]
    swipe([x * 0.5, y * 0.1], [x * 0.5, y * 0.8])


# 好友群发
def friends_sender(second, number, text):
    poco(text='WhatsApp').click()
    time.sleep(1)
    poco("com.whatsapp:id/fab").click()
    time.sleep(1)
    for i in range(0, number):
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
        time.sleep(random.randint(0, second))
        poco("com.whatsapp:id/fab").click()
        time.sleep(1)
        up()


# friends_sender(30,500,'very sorry')


# 导入通讯录
def upload_contacts(number):
    poco(text='通讯录').click()
    poco("更多选项").click()
    poco(text="导入/导出").click()
    poco(text="从 .vcf 文件导入").click()
    poco("更多选项").click()
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


# i = 0
# while True:
#     poco("com.whatsapp:id/fab").click()
#     time.sleep(1)
#     poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("com.whatsapp:id/root_layout").offspring("android:id/list").child("android.widget.RelativeLayout")[i].child("com.whatsapp:id/contactpicker_text_container").click()
#     time.sleep(1)
#     i = i + 1
#
#
#     keyevent('BACK')


while True:
    try:
        poco("com.netease.buff:id/batchPurchaseButton").wait_for_appearance(timeout=60)
        if poco("com.netease.buff:id/batchPurchaseButton"):  # 如果批量购买存在
            time.sleep(5)
            poco("com.netease.buff:id/batchPurchaseButton").click()
            print('点击批量购买成功')
            poco("com.netease.buff:id/buyPriceEdit").click()  # 点击价格输入框
            print(poco("com.netease.buff:id/buyPriceEdit").get_text())
            if poco("com.netease.buff:id/buyPriceEdit").get_text() != '最高单价':
                poco("com.netease.buff:id/buyPriceEdit").set_text('')
            else:
                shell(f"input text '0.72'")
                if poco("com.netease.buff:id/marketItemCounter"):  # 如果符合要求的存在
                    if poco("com.netease.buff:id/marketItemCounter").get_text() == '查询中…':
                        time.sleep(5)
                        availabe_text = poco("com.netease.buff:id/marketItemCounter").get_text()  # 获取符合要求的文本
                        availabe_number = int(availabe_text.split('件')[0])
                        print(availabe_number)
                        if availabe_number > 0:
                            poco("com.netease.buff:id/buyCountEdit").click()
                            poco("com.netease.buff:id/buyCountEdit").set_text(availabe_number)
                            time.sleep(1)
                            poco("com.netease.buff:id/submit").click()
                            print('点击购买成功')
                            poco("com.netease.buff:id/actionButton").wait_for_appearance(timeout=60)
                            if poco("com.netease.buff:id/actionButton") and availabe_number > 1:
                                poco("com.netease.buff:id/actionButton").click()
                                poco("android:id/button1").wait_for_appearance(timeout=10)
                                poco("android:id/button1").click()
                                poco("android:id/button1").wait_for_appearance(timeout=10)
                                poco("android:id/button1").click()
                                poco("android:id/button1").wait_for_appearance(timeout=60)
                                poco("android:id/button1").click()
                            elif poco("com.netease.buff:id/actionButton") and availabe_number == 1:
                                poco("com.netease.buff:id/actionButton").click()
                                poco("android:id/button1").wait_for_appearance(timeout=10)
                                poco("android:id/button1").click()
                                poco("android:id/button1").wait_for_appearance(timeout=60)
                                poco("android:id/button1").click()
                            else:
                                keyevent('BACK')
                        else:
                            keyevent('BACK')
                    else:
                        availabe_text = poco("com.netease.buff:id/marketItemCounter").get_text()  # 获取符合要求的文本
                        availabe_number = int(availabe_text.split('件')[0])
                        print(availabe_number)
                        if availabe_number > 0:
                            poco("com.netease.buff:id/buyCountEdit").click()
                            poco("com.netease.buff:id/buyCountEdit").set_text(availabe_number)
                            time.sleep(1)
                            poco("com.netease.buff:id/submit").click()
                            print('点击购买成功')
                            poco("com.netease.buff:id/actionButton").wait_for_appearance(timeout=60)
                            if poco("com.netease.buff:id/actionButton") and availabe_number > 1:
                                poco("com.netease.buff:id/actionButton").click()
                                poco("android:id/button1").wait_for_appearance(timeout=10)
                                poco("android:id/button1").click()
                                poco("android:id/button1").wait_for_appearance(timeout=10)
                                poco("android:id/button1").click()
                                poco("android:id/button1").wait_for_appearance(timeout=60)
                                poco("android:id/button1").click()
                                print(f'购买成功{availabe_number}件')
                            elif poco("com.netease.buff:id/actionButton") and availabe_number == 1:
                                poco("com.netease.buff:id/actionButton").click()
                                poco("android:id/button1").wait_for_appearance(timeout=10)
                                poco("android:id/button1").click()
                                poco("android:id/button1").wait_for_appearance(timeout=60)
                                poco("android:id/button1").click()
                                print(f'购买成功{availabe_number}件')
                            else:
                                keyevent('BACK')
                        else:
                            keyevent('BACK')
        else:
            keyevent('BACK')
    except Exception as e:
        print(e)
        stop_app('com.netease.buff')
        time.sleep(1)
        start_app('com.netease.buff')
        poco(text='搜索').click()  # 点击搜索框
        poco("android.widget.LinearLayout").offspring("com.netease.buff:id/editText").set_text("命悬一线武器箱")
        time.sleep(1)
        poco.click([0.5, 0.1])  # 点击命悬一线武器箱







