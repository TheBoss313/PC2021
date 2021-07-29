from tkinter import *
from winsound import PlaySound, SND_ASYNC
import random
from math import floor
from time import time
t = Tk()
t.title('Snake')
SCORES_LEADERBOARD = []
WIDTH = 600
HEIGHT = 800
GAME_HEIGHT = 600
FOOD_VALUE = 50
SEG_SIZE = 10
BONUS_START_TIME = 0
IN_GAME = True
LENGTH_SNAKE = 1
BASE_SCORE = 0
modes = {'normal': ['#ffffff', 'red', 'black', 'black'], 'dark': ['#000000', 'white', 'red', 'white']}
BLOCK = object
BONUS_BLOCK = object
TO_BONUS = 5
username = ''
mode = 'dark'


def calculate_bonus(time_from_start):
    return 100 - (floor(time_from_start * 10))


class Segment(object):
    def __init__(self, x, y, color=modes[mode][2]):
        self.instance = c.create_rectangle(x, y,
                                           x + SEG_SIZE, y + SEG_SIZE,
                                           fill=color)


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        # Dictionaries of (x,y) movement directions
        self.mapping = {"Down": (0, 1), "Up": (0, -1),
                        "Left": (-1, 0), "Right": (1, 0)}
        # Snake starts out moving right
        self.vector = self.mapping["Right"]
        self.vector_label = "Right"

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
        pressed_key = event.keysym
        if pressed_key in self.mapping:
            if self.vector_label == "Right" and pressed_key == "Left":
                pass
            elif self.vector_label == "Left" and pressed_key == "Right":
                pass
            elif self.vector_label == "Up" and pressed_key == "Down":
                pass
            elif self.vector_label == "Down" and pressed_key == "Up":
                pass
            else:
                self.vector = self.mapping[pressed_key]
                self.vector_label = pressed_key

    def add_segment(self, color=modes[mode][2]):
        global LENGTH_SNAKE
        # Finding last existing segment
        last_seg = c.coords(self.segments[0].instance)
        # Figure out where to put next segment
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        LENGTH_SNAKE += 1
        # Adding an extra segment at given coordiantes
        self.segments.insert(0, Segment(x, y, color))

    def add_segment_b(self, color="yellow"):
        # Finding last existing segment
        last_seg = c.coords(self.segments[0].instance)
        # Figure out where to put next segment
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        # Adding an extra segment at given coordiantes
        self.segments.insert(0, Segment(x, y, color))


def create_block():
    global BLOCK
    # Creates Food
    while True:
        posix = SEG_SIZE * (random.randint(1, int((WIDTH - SEG_SIZE) / SEG_SIZE)))
        posy = SEG_SIZE * (random.randint(1, int((GAME_HEIGHT - SEG_SIZE) / SEG_SIZE)))
        on_top = 0
        for i in snake.segments:
            seg_coords = c.coords(i.instance)
            if (posix, posy, posix + SEG_SIZE, posy + SEG_SIZE) == seg_coords:
                on_top = 1
                break
        if on_top == 1:
            pass
        else:
            break
    # Block is food, a coloured circle
    BLOCK = c.create_oval(posix, posy,
                          posix + SEG_SIZE,
                          posy + SEG_SIZE,
                          fill=modes[mode][1])


def create_bonus():
    global BONUS_BLOCK, BONUS_START_TIME
    # Creates Bonus Food
    while True:
        posix = SEG_SIZE * (random.randint(1, int((WIDTH - SEG_SIZE) / SEG_SIZE)))
        posy = SEG_SIZE * (random.randint(1, int((GAME_HEIGHT - SEG_SIZE) / SEG_SIZE)))
        on_top = 0
        for i in snake.segments:
            seg_coords = c.coords(i.instance)
            if [float(posix), float(posy), float(posix + SEG_SIZE), float(posy + SEG_SIZE)] == seg_coords:
                on_top = 1
                break
        if on_top == 1:
            pass
        else:
            break
    BONUS_BLOCK = c.create_oval(posix, posy,
                                posix + SEG_SIZE,
                                posy + SEG_SIZE,
                                fill="yellow")  # change to theme color later
    BONUS_START_TIME = time()


def main():
    global IN_GAME, BLOCK, BASE_SCORE, BONUS_SCORE, BONUS_BLOCK, TO_BONUS
    if IN_GAME:
        if time() - BONUS_START_TIME >= 5:
            c.delete(BONUS_BLOCK)
        snake.move()
        head_coords = c.coords(snake.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Checks for collision with walls
        if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > GAME_HEIGHT:
            IN_GAME = False
        elif head_coords == c.coords(BLOCK):
            # Snake ate Small Snack
            PlaySound("chomp.wav", SND_ASYNC)
            snake.add_segment()
            TO_BONUS -= 1
            if TO_BONUS == 0:
                TO_BONUS = 5
            BASE_SCORE += FOOD_VALUE
            c.itemconfig(score, text=f"Score: {BASE_SCORE}")
            c.itemconfig(to_bonus, text=f"Until Bonus: {TO_BONUS}")
            c.delete(BLOCK)
            create_block()
            if (LENGTH_SNAKE - 1) % 5 == 0:
                create_bonus()
        elif head_coords == c.coords(BONUS_BLOCK):
            # Snake ate Big Snack
            PlaySound("chomp.wav", SND_ASYNC)
            snake.add_segment_b()
            time_passed = time() - BONUS_START_TIME
            BASE_SCORE += calculate_bonus(time_passed)
            c.itemconfig(score, text=f"Score: {BASE_SCORE}")
            c.itemconfig(to_bonus, text=f"Until Bonus: {TO_BONUS}")
            c.delete(BONUS_BLOCK)
        else:
            for i in snake.segments[:-1]:
                # checks for collision with self
                if c.coords(i.instance) == head_coords:
                    IN_GAME = False
        # after small delay, run function again
        t.after(100, main)
    else:
        # If game is over, show score and game over message
        c.destroy()
        SCORES_LEADERBOARD.append((username, BASE_SCORE))
        ultra_main1()


def ultra_main2():
    global LENGTH_SNAKE, TO_BONUS, c, score, to_bonus, snake, BASE_SCORE, IN_GAME
    BASE_SCORE = 0
    LENGTH_SNAKE = 1
    TO_BONUS = 5
    IN_GAME = True
    c = Canvas(t, width=WIDTH, height=HEIGHT, bg=modes[mode][0])
    c.create_line(0, GAME_HEIGHT + 1, WIDTH, GAME_HEIGHT + 1, fill="red")
    c.grid()
    c.focus_set()

    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE * 2, SEG_SIZE),
                Segment(SEG_SIZE * 3, SEG_SIZE, "green")]
    snake = Snake(segments)
    score = c.create_text(100, GAME_HEIGHT + 70, text=f"Score: {BASE_SCORE}", font='Times 30 italic bold',
                          fill=modes[mode][3])
    to_bonus = c.create_text(130, GAME_HEIGHT + 110, text=f"Until Bonus: {TO_BONUS}", font='Times 30 italic bold',
                             fill=modes[mode][3])

    c.bind("<KeyPress>", snake.change_direction)
    create_block()
    main()


# Username and theme selection
def ultra_main1():
    global username, mode

    def go():
        # Destroys input used at the start, and runs the actual game
        global username
        username = e.get()
        lab.destroy()
        e.destroy()
        b.destroy()
        b_m1.destroy()
        b_m2.destroy()
        try:
            score_l.destroy()
            b_leader.destroy()
        except NameError:
            pass
        ultra_main2()

    def set_mode(mode1):
        global mode
        mode = mode1

    def leaderboard():
        tk = Tk()
        tk.title("Snake Leaderboard")
        for i in SCORES_LEADERBOARD:
            line = f"{i[0]}: {i[1]}"
            lab_score = Label(tk, text=line)
            lab_score.pack()

    lab = Label(t, text='ENTER USERNAME')
    lab.grid(row=0, column=0, columnspan=2)
    e = Entry()
    e.grid(row=1, column=0, columnspan=2)
    if len(SCORES_LEADERBOARD) > 0:
        score_l = Label(t, text=f"SCORE: {SCORES_LEADERBOARD[-1][1]}")
        b_leader = Button(t, text="Leaderboard", command=leaderboard)
        b = Button(text='Play Again!', command=lambda: go())
        score_l.grid(row=2, column=0)
        b_leader.grid(row=2, column=1)
    else:
        b = Button(text='Play!', command=lambda: go())
    b.grid(row=3, column=0, columnspan=2)
    b_m1 = Button(text='Eye Death', command=lambda mode2='normal': set_mode(mode2))
    b_m2 = Button(text='Dark', command=lambda mode2='dark': set_mode(mode2))
    b_m1.grid(row=4, column=0)
    b_m2.grid(row=4, column=1)


ultra_main1()
t.mainloop()
