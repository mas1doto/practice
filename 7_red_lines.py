import turtle as t

def draw_half_cat(x=0):
   t.lt(140 - 100 * x)
   t.fd(100)

   for i in range(1, 50):
       t.fd(5)
       if i < 15:
           t.rt(4 * (-1 if x else 1))
       if 15 < i > 35:
           t.fd(2)

   t.rt(150 * (-1 if x else 1))
   t.fd(130)
   t.lt(-70)

   if not x:
       t.circle(144, -88)


def set_pos(x, y):
   t.up()
   t.setpos(x, y)
   t.setheading(0)
   t.down()


def draw_cat():
   set_pos(-90, 0)
   draw_half_cat()

   set_pos(50, 0)
   draw_half_cat(1)

def draw_lines():
   # "прозрачный"
   ar = (200, 161, 130)
   colors = {0: "red", 10: ar, 20: "green", 30: ar, 40: "green", 50: ar, 60: "red"}

   for i in range(0, 70, 10):
       t.color(colors[i])
       set_pos(-90 + i, 0)
       t.setheading(-40)
       t.fd(300)

       set_pos(50 - i, 0)
       t.setheading(-140)
       t.fd(300)

       if i:
           set_pos(-90 + i, 0)
           t.setheading(-90)
           t.circle(70 - i, -180)


if __name__ == '__main__':
   t.colormode(255)
   t.width(3)
   t.color("red")
   t.ht()
   t.speed(10)

   draw_cat()
   draw_lines()

   t.done()
