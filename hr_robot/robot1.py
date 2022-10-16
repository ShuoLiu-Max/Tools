import time
import pyperclip

from math import sqrt
from pymouse import PyMouse
from pykeyboard import PyKeyboard





########################################
class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

def distance(a, b):
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)



def drag(p1, p2, t = 0.05, r = 1):
    m.press(p1.x, p1.y, 1)

    x = p1.x
    y = p1.y
    step = 80


    while distance(Point(x, y), p2) >= 1 :
        x += (p2.x - x)/step
        y += (p2.y - y)/step
        step -= 1
        m.move(int(x), int(y))
        time.sleep(0.01)
    time.sleep(t)
    if r == 1:
        m.release(p2.x, p2.y, 1)




def get_key_pos():
    pos1 = Point(0,0)
    pos2 = Point(0,0)
    pos3 = Point(0,0)
    pos4 = Point(0,0)
    pos5 = Point(0,0)
    last_time = time.time()
    step = -1
    
    print("标定开始...")
    while 1<2:
        t = time.time() - last_time
        if  t > 5:
            last_time = time.time()
            if step == -1:
                print("请点击一次简历左上角的空白处,并保持不动")
                step = 0
            elif step == 0:
                time.sleep(5)
                pos1.x,pos1.y = m.position()
                print("请点击一次打招呼,并保持不动")
                step = 1.1
            elif step == 1.1:
                time.sleep(5)
                pos2.x,pos2.y = m.position()
                print("请点击一次继续沟通,并保持不动")
                step = 1
            elif step == 1:
                time.sleep(5)
                pos2.x,pos2.y = m.position()
                print("请点击一次文字输入框,并保持不动")
                step = 2
            elif step == 2:
                time.sleep(5)
                pos3.x,pos3.y = m.position()
                print("请点击一次关闭对话框,并保持不动")
                step = 3
            elif step == 3:
                time.sleep(5)
                pos4.x,pos4.y = m.position()
                print("请点击一次下一个,并保持不动")
                step = 4
            elif step == 4:
                time.sleep(5)
                pos5.x,pos5.y = m.position()
                print(pos1,pos2,pos3,pos4,pos5)
                return pos1,pos2,pos3,pos4,pos5

########################################


def people_filter():
    drag(Point(pos1.x,pos1.y),Point(pos1.x,pos1.y+350),2,0)
    m.scroll(vertical=-100, horizontal=0)
    time.sleep(1)
    k.press_key(k.control_key)
    k.tap_key('c')
    time.sleep(1)
    
    k.release_key(k.control_key)


    text = pyperclip.paste()

    print(">>> 候选人，人物画像: ")
    target_schools_flag=0
    for school in target_schools:
        if text.find(school) != -1:
            print('目标院校:',school)
            target_schools_flag=1
            break
    if target_schools_flag==0:
        print("非目标院校")
        return 0
    
    for continution in no_continution:
        if text.find(continution) != -1:
            print('不满足条件:',continution)
            return 0
    
    target_language_flag=0
    for language in target_language:
        if text.find(language) != -1:
            print('目标语言/岗位:',language)
            target_language_flag=1
            break
    if target_language_flag==0:
        print("非目标语言/岗位")
        return 0

    return 1
    
########################################


def hr_start():

    last_time = time.time()
    step = -1
    while 1<2:
        t = time.time() - last_time
        if  t > 4:
            if step == -1:
                if people_filter() == 1:
                    step = 0
                else:
                    step = 4
            elif step == 0:
                m.click(pos2.x, pos2.y, 1)     
                step = 1
                print("沟通")
            elif step == 1:
                m.click(pos2.x, pos2.y, 1)      
                step = 2
                pyperclip.copy("欢迎随时沟通哦~")
                print("打开沟通对话框")
            elif step == 2:
                m.click(pos3.x, pos3.y , 1)     
                k.press_key(k.control_key)
                k.tap_key('v')
                time.sleep(1)
                k.release_key(k.control_key)
                k.tap_key(k.enter_key)
                step = 3
                print("输入一句话")
            elif step == 3:
                m.click(pos4.x, pos4.y, 1)      #取整除 - 向下取接近除数的整数
                step = 4
                print("关闭沟通")
            elif step == 4:
                m.click(pos5.x, pos5.y, 1)
                time.sleep(1)
                k.release_key(k.control_key)
                time.sleep(1)

                step = -1
                print("下一个")

            #print("time=",t)
            last_time = time.time()


if __name__ == '__main__':
    target_schools = []
    with open('目标院校.txt','r',encoding='utf-8') as f:
        F = f.readlines()
        for i in F:
            target_schools.append(i.strip())
    # print(target_schools)
    Y = input('请将自动搜索界面放在最左边, 并完全展示出来, 终端放置在最右侧,准备完毕输入 Y:')
    while Y not in ['Y','y']:
        Y = input('请将自动搜索界面放在最左边, 并完全展示出来, 终端放置在最右侧,准备完毕输入 Y:')

    target_language = ['Python','python','Java','java','C语言','C++','C#','测试开发','软件开发','测试工程师','软件开发工程师']

    no_continution = ['23年应届生','大专','非全日制','在职-暂不考虑']
    
    m = PyMouse()
    k = PyKeyboard()
    
    
    pos1,pos2,pos3,pos4,pos5 = Point(170,141),Point(899,210),Point(701,771),Point(1015,418),Point(1027,480)
    pos1,pos2,pos3,pos4,pos5 = get_key_pos()

    hr_start()


