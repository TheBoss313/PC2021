from turtle import *

WN_HEIGHT = 600
WN_WIDTH = 800
wn = Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=WN_WIDTH, height = WN_HEIGHT)
wn.tracer(0)

right_score = 0
left_score = 0
#Pen
pen = Turtle()
pen.speed(0)
pen.color("white")
pen.hideturtle()
pen.penup()
pen.goto(0, 260)
pen.write(f"Player A: {left_score}  Player B: {right_score}", align = "center", font=("Courier", 24, "normal"))

def update_score():
    pen.clear()
    pen.write(f"Player A: {left_score}  Player B: {right_score}", align = "center", font=("Courier", 24, "normal"))

# Paddle L
paddle_l = Turtle()
paddle_l.speed(0)
paddle_l.shape("square")
paddle_l.shapesize(stretch_wid=5,stretch_len=1)
paddle_l.color("white")
paddle_l.penup()
paddle_l.goto(-350,0)
# Paddle R
paddle_r = Turtle()
paddle_r.speed(0)
paddle_r.shape("square")
paddle_r.shapesize(stretch_wid=5,stretch_len=1)
paddle_r.color("white")
paddle_r.penup()
paddle_r.goto(350,0)
# Ball
ball = Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0,0)

ball.dx = .3
ball.dy = .3


#Left Paddle UP
def pad_l_u():
    y = paddle_l.ycor()
    if y+70 > 300:
        y = 250
    else:
        y += 20
    paddle_l.sety(y)

#Left Paddle DOWN
def pad_l_d():
    y = paddle_l.ycor()
    if y-70 < -300:
        y = -250
    else:
        y -= 20
    paddle_l.sety(y)
#Right Paddle UP
def pad_r_u():
    y = paddle_r.ycor()
    if y+70 > 300:
        y = 250
    else:
        y += 20
    paddle_r.sety(y)

#Right Paddle DOWN
def pad_r_d():
    y = paddle_r.ycor()
    if y-70 < -300:
        y = -250
    else:
        y -= 20
    paddle_r.sety(y)
# Bind Keys
wn.listen()
wn.onkeypress(pad_l_u,"w")
wn.onkeypress(pad_l_d,"s")
wn.onkeypress(pad_r_u,"Up")
wn.onkeypress(pad_r_d,"Down")
while True:
    wn.update()
    ball.setx(ball.xcor()+ball.dx)
    ball.sety(ball.ycor()+ball.dy)
    
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
    elif ball.ycor() < -283:
        ball.sety(-283)
        ball.dy *= -1
    if ball.xcor() > 390:
        ball.goto(0, 0)
        left_score += 1
        update_score()
        ball.dx *= -1
    elif ball.xcor() < -390:
        ball.goto(0, 0)
        right_score += 1
        update_score()
        ball.dx *= -1
    if ball.xcor() > 330 and ball.xcor() < 360 and ball.ycor()< paddle_r.ycor()+50 and ball.ycor() > paddle_r.ycor()-50:
        ball.setx(330)
        ball.dx *= -1
    elif ball.xcor() <= -330 and ball.xcor() > -360 and ball.ycor()< paddle_l.ycor()+50 and ball.ycor() > paddle_l.ycor()-50:
        ball.setx(-330)
        ball.dx *= -1
