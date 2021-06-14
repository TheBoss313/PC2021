from tkinter import *
import random
t = Tk()
t.title('Snek')
WIDTH = 600
HEIGHT = 600
SEG_SIZE = 10
IN_GAME = True
LENGTH_SNAKE = 1
modes = {'normal': ['#ffffff', 'red', 'black', 'black'], 'dark': ['#000000', 'white', 'red', 'white']}
BLOCK = object
username = ''
mode = 'normal'


def ultra_main2():
    global LENGTH_SNAKE

    class Segment(object):
        def __init__(self, x, y):
            self.instance = c.create_rectangle(x, y,
                                               x + SEG_SIZE, y + SEG_SIZE,
                                               fill=modes[mode][2])

    class Snake(object):
        def __init__(self, segments):
            self.segments = segments
            # список доступных направлений движения змейки
            self.mapping = {"Down": (0, 1), "Up": (0, -1),
                            "Left": (-1, 0), "Right": (1, 0)}
            # изначально змейка двигается вправо
            self.vector = self.mapping["Right"]

        def move(self):
            for index in range(len(self.segments) - 1):
                segment = self.segments[index].instance
                x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
                c.coords(segment, x1, y1, x2, y2)
            x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
            c.coords(self.segments[-1].instance,
                     x1 + self.vector[0] * SEG_SIZE,
                     y1 + self.vector[1] * SEG_SIZE,
                     x2 + self.vector[0] * SEG_SIZE,
                     y2 + self.vector[1] * SEG_SIZE)

        def change_direction(self, event):
            if event.keysym in self.mapping:
                self.vector = self.mapping[event.keysym]

        def add_segment(self):
            global LENGTH_SNAKE
            # Определяем последний сегмент
            last_seg = c.coords(self.segments[0].instance)
            # Определяем координаты куда поставить следующий сегмент
            x = last_seg[2] - SEG_SIZE
            y = last_seg[3] - SEG_SIZE
            LENGTH_SNAKE += 1
            # Добавляем змейке еще один сегмент в заданных координатах
            self.segments.insert(0, Segment(x, y))

    def create_block():
        global BLOCK
        posx = SEG_SIZE * (random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
        posy = SEG_SIZE * (random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))
        # Блок это кружочек красного цвета
        BLOCK = c.create_oval(posx, posy,
                              posx + SEG_SIZE,
                              posy + SEG_SIZE,
                              fill=modes[mode][1])

    def main():
        global IN_GAME, BLOCK
        if IN_GAME:
            snake.move()
            head_coords = c.coords(snake.segments[-1].instance)
            x1, y1, x2, y2 = head_coords
            if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
                IN_GAME = False
            elif head_coords == c.coords(BLOCK):
                snake.add_segment()
                c.itemconfig(score, text=LENGTH_SNAKE - 1)
                c.delete(BLOCK)
                create_block()
            else:
                for index in range(len(snake.segments) - 1):
                    if c.coords(snake.segments[index].instance) == head_coords:
                        IN_GAME = False
            t.after(100, main)
        else:
            c.create_text(WIDTH / 2, HEIGHT / 2,
                          text=f"GAME OVER!\nFINAL SCORE:\n{LENGTH_SNAKE - 1}",
                          font="Arial 20",
                          fill="#ff0000")
            send_score()

    c = Canvas(t, width=WIDTH, height=HEIGHT, bg=modes[mode][0])
    c.grid()
    c.focus_set()

    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE * 2, SEG_SIZE),
                Segment(SEG_SIZE * 3, SEG_SIZE)]
    snake = Snake(segments)
    score = c.create_text(300, 30, text=LENGTH_SNAKE - 1, font='Times 40 italic bold', fill=modes[mode][3])

    c.bind("<KeyPress>", snake.change_direction)
    create_block()
    main()


def ultra_main1():
    global username, mode

    def go():
        global username
        username = e.get()
        lab.destroy()
        e.destroy()
        b.destroy()
        b_m1.destroy()
        b_m2.destroy()
        ultra_main2()

    def set_mode(mode1):
        global mode
        mode = mode1

    lab = Label(t, text='ENTER USERNAME')
    lab.pack()
    e = Entry()
    e.pack()
    b = Button(text='GO!', command=lambda: go())
    b.pack()
    b_m1 = Button(text='Eye Death', command=lambda mode2='normal': set_mode(mode2))
    b_m2 = Button(text='Dark', command=lambda mode2='dark': set_mode(mode2))
    b_m1.pack(side='left')
    b_m2.pack(side='right')


ultra_main1()
t.mainloop()
