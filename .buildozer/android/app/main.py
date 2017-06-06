import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.clock import Clock
from random import randint

bsensors = None # Boolean ob plyer erkannt wird (iOS)
try:
    from plyer import battery
    from plyer import vibrator
    bsensors = True
except:
    bsensors = False

# Zaehle mit wie oft Objekt angetippt wurde
count_door = 0
count_cat = 0

# Erzeuge die Objekte
class DoorPopup(Popup):
    pass

class BatteryPopup(Popup):
    pass

class MiezIcon(Widget):
    pass


# Erzeuge den roten Ball mit den Eigenschaften seine Position zu ändern
class MiezBall(Widget):

    # Folgender Code basiert auf dem offiziellem Pong-Beispiel:
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

# Erzeuge das ganze Widget
class MiezBox(BoxLayout):

    # Verwalte den Ball
    ball = ObjectProperty(None)
    icon = ObjectProperty(None)
    lbl1 = ObjectProperty()
    lbl2 = ObjectProperty()


    # Öffne das PopUp wenn an der Tür angeklopft wird
    def open_door_popup(self):
        print('open PopUp')
        the_popup = DoorPopup()
        the_popup.open()

    # Öffne ein Fenster mit dem Status der Batterie
    def get_battery_status(self, *args):
        if bsensors:
            try:
                msg = "isCharching: " + str(battery.status['isCharging']) + "   Percentage: " + str(battery.status['percentage']) + "%"
            except ValueError:
                msg = "Sorry, couldn't get battery status."
        else:
            msg = "Sorry, can't access sensors by code (iOS)."
        pop = Popup(title='Battery status',
            content=Label(text=msg),
            size_hint=[.5, .2])
        pop.open()

    # Setze den Ball
    def serve_ball(self):
        self.ball.velocity = Vector(10, 0).rotate(randint(0, 360))

    # Update für den Ball (z.B. Reduktion der Geschwindigkeit)
    def update(self, dt):
        speed_reduce = [0.05, 0.05]

        # reduce speed
        if Vector(*self.ball.velocity)[0] < 0:
            speed_reduce[0] = -1 * speed_reduce[0]
        if Vector(*self.ball.velocity)[1] < 0:
            speed_reduce[1] = -1 * speed_reduce[1]

        self.ball.velocity = Vector(*self.ball.velocity) - speed_reduce
        self.ball.move()

        # Ball soll von oben und unten abprallen, schlechter Workaround mit der Multiplikation
        if (self.ball.y < 0) or (self.ball.top > self.height*1.3): #*1.2
            self.ball.velocity_y *= -1

        # Ball soll von rechts und links abprallen, schlechter Workaround mit der Multiplikation
        if (self.ball.x < 0) or (self.ball.right > self.width*1.4): #*1.4
            self.ball.velocity_x *= -1


    # Bei Berührung des Bildschirms:
    def on_touch_up(self, touch):
        print touch
        global count_door
        global count_cat

        # Falls der Ball berührt wurde
        if abs(touch.pos[0] - self.ball.x) < 80 and abs(touch.pos[1] - self.ball.y) < 80:
            self.serve_ball()

        # Falls die Tür berührt wurde zähle bis 5 Berührungen ("Anklopfen")
        # print(touch): <MouseMotionEvent spos=(0.654375, 0.9292035398230089) pos=(1047.0, 735.0)>
        # -> pos ist die absolute Position (wie Pixel), spos ist die Position auf einer Skala  0-1
        elif (touch.spos[0] > 0.6543 and touch.spos[0] < 0.7925) and (touch.spos[1] > 0.5550 and touch.spos[1] < 0.9292):
            if count_door is 4:
                self.open_door_popup()
                count_door = 0
            else:
                count_door+=1

        # Falls die Mieze berührt wurde warte 3 Berührungen ab um zu vibrieren
        elif (touch.spos[0] > 0.1630 and touch.spos[0] < 0.2550) and (touch.spos[1] < 0.5200 and touch.spos[1] > 0.2830):
            if count_cat is 2:
                if bsensors:
		            vibrator.vibrate(0.5)
                count_cat = 0
            else:
                count_cat+=1

    # Beim Spinner wird der Text selbst gesetzt, siehe kv-Datei
    def spinner_clicked(self, value):
        pass

##################################################
# Erstelle die App basierend auf dem Widget MiezBox
class MiezApp(App):
    def build(self):
        game = MiezBox()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    MiezApp().run()

