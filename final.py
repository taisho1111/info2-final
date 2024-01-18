import pyxel
import random

class Timer:
    def __init__(self):
        self.count = 0
        self.x = 5
        self.y = 5
        self.color = 0 #black
        self.started = False

    def update(self):
        # Enterが押されたか確認し、押されていなければ何もしない
        if not self.started and pyxel.btnp(pyxel.KEY_RETURN):
            self.started = True

        # 開始していない場合は何もしない
        if not self.started:
            return
        if (pyxel.frame_count % 30 == 0):
            self.count += 1

    def draw(self):
        pyxel.text(self.x, self.y, "Timer:" + str(self.count), self.color)

class Rect:
    def __init__(self):
        self.recty = 0
        self.rectsize = 7
        self.generate()

    def generate(self):
        self.rectx = random.randint(0,100)
        self.randomnum = random.randint(2,5)

    def move(self):
        self.recty += self.randomnum
        if self.recty >= 200:
            self.recty = -10

class Pointer:
    def __init__(self):
        self.x = 50
        self.y = 200
        self.speed = 1

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed

class Melon:
    def __init__(self):
        self.Melon_x = random.randint(10,90)
        self.Melon_y = 0
        self.Melon_size = 16

    def update(self):
        self.Melon_y += 0.3
        if self.Melon_y >= 200:
            self.Melon_y = -10
            self.Melon_x = random.randint(10,90)
    def draw(self):
        pyxel.blt(self.Melon_x, self.Melon_y, 0, 64, 0, 16, 16, 12)


class App:
    pyxel.init(100,200)
    flag = False
    def __init__(self):
        pyxel.load("jump_game.pyxres")
        self.rectn = 10
        self.start = True
        self.goal = False
        self.flag = False
        self.rects = []
        self.Timer = Timer()
        self.Melon = Melon()
        self.Pointer = Pointer()


        #四角の数はrectn
        for i in range(self.rectn):
            self.rects.append(Rect())
        pyxel.run(self.update,self.draw)
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.Pointer.y <= 0 and self.start == False:
            self.goal = True


        #スタートメニューの当たり判定
        for i in range(self.rectn):
            self.rects[i].move()
            if (
                self.start == False and
                self.Pointer.x>= self.rects[i].rectx and
                self.Pointer.x <= self.rects[i].rectx+self.rects[i].rectsize and
                self.Pointer.y >= self.rects[i].recty and
                self.Pointer.y <= self.rects[i].recty+self.rects[i].rectsize
            ):
                self.flag = True
            self.Melon.update()
            if (
                self.start == False and
                self.Pointer.x >= self.Melon.Melon_x and
                self.Pointer.x <= self.Melon.Melon_x + self.Melon.Melon_size and
                self.Pointer.y >= self.Melon.Melon_y and
                self.Pointer.y <= self.Melon.Melon_y + self.Melon.Melon_size
            ):
                self.Pointer.speed = 0.5
        self.Pointer.update()
        self.Timer.update()

        #シーン分け（スタート画面）
        if self.start == True:
            if pyxel.btn(pyxel.KEY_RETURN):
                self.start = False
        #シーン分け（プレイ中）
        if self.start == False and self.flag == False and self.Pointer.x >= 195:
            self.goal = True
        #シーン分け（ゴール画面）
        if self.start == False and self.goal == True:
            if pyxel.btn(pyxel.KEY_R):
                for i in range(self.rectn):
                    self.rects[i].generate()
                self.flag = False
                self.start = True
                self.goal = False
                self.Pointer.speed = 1
                self.Pointer.x = 50
                self.Pointer.y = 200
                self.Timer.count =0
                self.Timer.started = False

        #シーン分け（死んだとき）
        if self.start == False and self.flag == True:
            if pyxel.btn(pyxel.KEY_R):
                for i in range(self.rectn):
                    self.rects[i].generate()
                self.flag = False
                self.start = True
                self.Pointer.speed = 1
                self.Pointer.x = 50
                self.Pointer.y = 200
                self.Timer.count =0
                self.Timer.started = False

    def draw(self):
        pyxel.cls(3)
        pyxel.circ(self.Pointer.x,self.Pointer.y,2,4)
        self.Timer.draw()

        if self.start == True:
            pyxel.text(30,50,"DODGER!",8)
            pyxel.text(30,70,"Push Enter",0)
        else:
            if self.goal == False:
                self.Melon.draw()
                for i in range(self.rectn):
                    pyxel.rect(self.rects[i].rectx,self.rects[i].recty,7,5,13)
                if self.flag == True:
                    pyxel.cls(10)
                    pyxel.text(10,100,"Game Over!!!",0)
                    pyxel.text(10,120,"Press [R] to Restart",0)
                    pyxel.text(10,140,"Press [Q] to Quit",0)
            if self.goal == True:
                pyxel.cls(10)
                pyxel.text(10,100,"Goal!!!",0)
                pyxel.text(10,120,"Press [R] to Restart",0)
                pyxel.text(10,140,"Press [Q] to Quit",0)

App()
