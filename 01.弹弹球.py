import tkinter
import time
import random


"""
    弹弹球游戏逻辑分析
    1.创建游戏窗口   ---初始化
    2.创建一个弹弹球 ---创建弹球的类 初始化属性 创建实例对象 
    3.弹弹球反弹移动 ---添加一个移动方法 --> y方向移动 遇到边框反弹
    4.弹弹球随机移动 ---增加球的x轴的随机运动方向
    5.创建一个小木板 ---
    6.小木板添加移动功能
    7.增加球和小木板的碰撞侦测 
    8.判断当球移动到底部游戏结束
"""


# 创建一个弹球的类
class Ball(object):
    """弹球"""

    def __init__(self, canvas, color, plank):
        """初始化弹球"""
        self.canvas = canvas
        self.oval = canvas.create_oval(10, 10, 25, 25, fill=color)     # 创建一个实心球,并记录它的id
        self.canvas.move(self.oval, 245, 100)                          # 初始化弹球的位置
        self.x = 0
        self.y = -5
        # self.canvas_height = self.canvas.winfo_height()
        self.x_direct = [-3, -2, -1, 1, 2, 3]
        self.plank = plank                                             # 接收木板对象
        self.hit_bottom = False

        # starts = [-3, -2, -1, 1, 1, 2, 3]   ---公众号思路代码
        # random.shuffle(starts)
        # self.x = starts[0]  # 从list里面随机取一个
        # self.y = -3  # -3表示y轴运动的速度

    def draw(self):
        """移动"""
        index = random.randint(0, 5)

        pos = self.canvas.coords(self.oval)
        if pos[1] <= 0:                             # 如果y坐标超出窗口顶部 则+5向下移动
            self.y = 5
            self.x = self.x_direct[index]

        if pos[3] >= 400:                           # 如果y坐标超出窗口底部 则-5向上移动
            self.y = -5
            self.x = self.x_direct[index]

        if pos[0] <= 0:                             # 如果x坐标超出窗口左部 则向右移动
            self.x = self.x_direct[index]

        if pos[2] >= 500:                           # 如果x坐标超出窗口右部 则向左移动
            self.x = self.x_direct[index]

        if self.hit_plank(pos):                     # 如果检测到木板撞击,则向上移动
            self.y = -5

        if pos[3] >= 380:                           # 如果检测到弹弹球撞击窗口底部, 则更改hit_bottom状态
            self.hit_bottom = True

        # self.canvas.move(self.oval, 0, -1)
        self.canvas.move(self.oval, self.x, self.y)  # 移动弹球

    def hit_plank(self, pos):
        """检测弹弹球和木板的撞击"""
        plank_pos = self.canvas.coords(self.plank.rect)
        if (pos[2] >= plank_pos[0]) and (pos[0] <= plank_pos[2]):
            if (pos[3] >= plank_pos[1]) and (pos[3] <= plank_pos[3]):
                return True

        return False


class Plank(object):
    """创建木板的类"""
    def __init__(self, canvas, color):
        """初始化小木板对象"""
        self.canvas = canvas
        self.rect = canvas.create_rectangle(0, 0, 80, 10, fill=color)
        self.canvas.move(self.rect, 200, 350)

        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        """通过draw函数画出木板左移右移"""
        self.canvas.move(self.rect, self.x, 0)
        pos = self.canvas.coords(self.rect)

        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= 500:
            self.x = 0

    def turn_left(self, event):
        """木板向左移动"""
        self.x = -5

    def turn_right(self, event):
        self.x = 5


def main():
    """弹弹球游戏主程序"""

    # 初始化 游戏窗口
    tk = tkinter.Tk()                                  # 1.创建一个tk的实例
    tk.title('弹弹球-refrain')                         # 2.游戏窗口命名
    # tk.geometry('500x400')
    tk.resizable(0, 0)                                 # 3.窗口布局不能被拉升
    canvas = tkinter.Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)          # 4.创建窗口大小
    canvas.pack()                                      # 5.通知窗口管理器注册组件
    # tk.mainloop()  # 开始事件循环     tk.update() 刷新界面

    # 创建一个弹球 和 木板 对象
    plank = Plank(canvas, 'grey')
    ball = Ball(canvas, 'blue', plank)

    while True:
        if not ball.hit_bottom:
            ball.draw()
            plank.draw()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.1)
        else:
            break


if __name__ == '__main__':
    main()