import kivy

kivy.require("1.9.0")


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty
from kivy.clock import Clock
from random import randint
from plyer import vibrator

count_door = 0
count_cat = 0


# PopIp when door clicked
class CustomPopup(Popup):
    pass

class SensorBox(Screen):
    pass


class MiezIcon(Widget):
    pass


# red Ball as toy
class MiezBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


# Whole widget
class MiezBox(Screen):
    # manage ball
    ball = ObjectProperty(None)
    icon = ObjectProperty(None)

    # Opens Popup when called
    def open_popup(self):
        print('open PopUp')
        the_popup = CustomPopup()
        the_popup.open()

    def serve_ball(self):
        # self.ball.center = self.center
        self.ball.velocity = Vector(10, 0).rotate(randint(0, 360))
        # self.ball.velocity = Vector(8, 0).rotate(20)

    def update(self, dt):
        speed_reduce = [0.05, 0.05]

        # reduce speed
        if Vector(*self.ball.velocity)[0] < 0:
            speed_reduce[0] = -1 * speed_reduce[0]
        if Vector(*self.ball.velocity)[1] < 0:
            speed_reduce[1] = -1 * speed_reduce[1]

        self.ball.velocity = Vector(*self.ball.velocity) - speed_reduce
        self.ball.move()

        # bounce off top and bottom, the multilpication is a bad workaround
        print(self.ball.x)
        print(self.ball.y)
        if (self.ball.y < 0) or (self.ball.top - 200 > self.height):  # *1.2
            #print('self.ball.top: %d\n', self.ball.top)
            #print('self.height: %d\n', self.height)
            #print('self.ball.y: \n', self.ball.y)
            self.ball.velocity_y *= -1
            print('bounced top or bottom')

        # bounce off left and right
        if (self.ball.x + 200 < 0) or (self.ball.right - 200 > self.width):  # *1.4
            self.ball.velocity_x *= -1
            print('bounced left or right')

    def on_touch_up(self, touch):
        #print touch
        global count_door
        global count_cat

        # size ball is 70
        print(abs(touch.pos[0] - self.ball.x))
        print(abs(touch.pos[1] - self.ball.y))
        print(' ')
        if abs(touch.pos[0] - self.ball.x) < 55 and abs(touch.pos[1] - self.ball.y) < 220:
            print('worked')
            self.serve_ball()

        # koordinates of the door are x: 0.6543, 0.7925 and y: 0.9292, 0.5550
        # print(touch): <MouseMotionEvent spos=(0.654375, 0.9292035398230089) pos=(1047.0, 735.0)>
        # -> pos absolute position (like pixel), spos is the position on a scale 0-1
        elif (touch.spos[0] > 0.505 and touch.spos[0] < 0.643) and (
                        touch.spos[1] > 0.503 and touch.spos[1] < 0.847):
            if count_door is 4:
                self.open_popup()
                count_door = 0
            else:
                count_door += 1

        elif (touch.spos[0] > 0.1630 and touch.spos[0] < 0.2550) and (
                        touch.spos[1] < 0.5200 and touch.spos[1] > 0.2830):
            if count_cat is 2:
                vibrator.pattern([0.1, 0.1, 0.2])
                count_cat = 0
            else:
                count_cat += 1

    # For Spinner
    def spinner_clicked(self, value):
        pass


class MiezApp(App):
    def build(self):
        game = MiezBox()
        # game.serve_ball()
        # Clock.schedule_interval(game.update, 1.0 / 60.0)
        # Window.clearcolor = (1,1,1,1)
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        screen_manager = ScreenManager()
        screen_manager.add_widget(MiezBox(name='miez_screen'))
        screen_manager.add_widget(SensorBox(name='sensor_screen'))
        return screen_manager

    def on_pause(self):
        return True


if __name__ == '__main__':
    MiezApp().run()

# miez_app = MiezApp()
# miez_app.run()
