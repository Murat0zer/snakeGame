import kivy
__version__ = '1.9.1'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.graphics import *


class OyunAlani(Widget):
    meyve = ObjectProperty(None)
    yilan = ObjectProperty(None)
    #ekran ayarlari
    sutun_sayi = 16
    satir_sayi = 9
    # oyun degiskenleri.
    skor = NumericProperty(0)
    donus_sayici = NumericProperty(0)
    meyve_ritmi = NumericProperty(0)

    # oyuncunun inputlari
    dokunma_pozisyonu = ListProperty()
    eylem_tetiklendi = BooleanProperty()


class Meyve(Widget):
    duration = NumericProperty(10)
    interval = NumericProperty(3)

    object_on_board = ObjectProperty(None)
    durum = BooleanProperty(False)


class Yilan(Widget):
    kafa = ObjectProperty(None)
    kuyruk = ObjectProperty(None)

    def hareket(self):
        yeni_kuyruk_poz = list(self.kafa.pozisyon)
        self.kafa.hareket()
        self.kuyruk.blok_ekle(yeni_kuyruk_poz)

    def sil(self):
        self.kafa.sil()
        self.kuyruk.sil()

    def pozisyon_ayarla(self, pozisyon):
        self.kafa.pozisyon = pozisyon

    def pozisyon_al(self):
        return self.kafa.pozisyon
    def tam_pozisyon_al(self):
        return self.kafa.pozisyon + self.kuyruk.pozisyon

    def yon_ayarla(self, yon):
        self.kafa.yon = yon

    def yon_al(self):
        return self.kafa.yon

class YilanKafa(Widget):
    yon = OptionProperty(
        "Right", options=["Up", "Down", "Left", "Right"])
    x_pozisyonu = NumericProperty(0)
    y_pozisyonu = NumericProperty(0)
    pozisyon = ReferenceListProperty(x_pozisyonu, y_pozisyonu)

    points = ListProperty([0]*6)
    object_onboard = ObjectProperty(None)
    durum = BooleanProperty(False)

    def is_on_board(self):
        return self.durum

    def sil(self):
        if self.is_on_board():
            self.canvas.remove(self.object_onboard)
            self.object_onboard = ObjectProperty(None)
            self.durum = False

    def ciz(self):
        with self.canvas:
            if not self.is_on_board():
                self.object_onboard = Triangle(points=self.puanlar)
                self.durum = True #
            else:
                self.canvas.remove(self.object_onboard)
                self.object_onboard = Triangle(points=self.puanlar)

    def hareket(self):
        if self.yon == "Right":
            self.pozisyon[0] += 1
            x0 = self.pozisyon[0] * self.width
            y0 = (self.pozisyon[1] - 0.5) * self.height
            x1 = x0 + self.width
            y1 = y0 + self.height / 2
            x2 = x0 - self.width
            y2 = y0 - self.height / 2
        elif self.yon == "Left":
            self.pozisyon[0] -= 1
            x0 = (self.pozisyon[0] - 1) * self.width
            y0 = (self.pozisyon[0] - 0.5) * self.height
            x1 = x0 + self.width
            y1 = y0 + self.height / 2
            x2 = x0 + self.width
            y2 = y0 + self.height / 2
        elif self.pozisyon == "Up":
            self.pozisyon[1] += 1
            x0 = (self.pozisyon[0] - 0.5) * self.width
            y0 = self.pozisyon[1] * self.height
            x1 = x0 - self.width / 2
            y1 = y0 - self.height
            x2 = x0 + self.width / 2
            y2 = y0 - self.height
        elif self.yon == "Down":
            self.pozisyon[1] -= 1
            x0 = (self.position[0] - 0.5) * self.width
            y0 = (self.position[1] - 1) * self.height
            x1 = x0 + self.width / 2
            y1 = y0 + self.height
            x2 = x0 - self.width / 2
            y2 = y0 + self.height

        self.points = [x0, y0, x1, y1, x2, y2]
        self.ciz()




class YilanKuyruk(Widget):
    # kuyruk uzunlugu
    boyut = NumericProperty(3)

    blok_pozisyonu = ListProperty()
    kuyruk_blok_objeleri = ListProperty()

    def sil(self):
        self.boyut = 3

        for block in self.kuyruk_blok_objeleri:
            self.canvas.remove(block)

        self.blok_pozisyonu = []
        self.kuyruk_blok_objeleri = []

    def blok_ekle(self, pozisyon):
        self.blok_pozisyonu.append(pozisyon)

        if len(self.blok_pozisyonu) > self.size:
            self.blok_pozisyonu.pop(0)

        with self.canvas:
            for poz in self.blok_pozisyonu:
                x = (poz[0] - 1) * self.width
                y = (poz[1] - 1) * self.height
                koord = (x,y)
                blok = Rectangle(poz=koord, size=(self.width,
                                                         self.height))
                self.kuyruk_blok_objeleri.append(blok)

                if len(self.kuyruk_blok_objeleri) > self.size:
                    son_blok = self.kuyruk_blok_objeleri.pop(0)
                    self.canvas.remove(son_blok)


class YilanApp(App):
    oyun_motoru = ObjectProperty(None)
    def build(self):
        game = OyunAlani()
        return game

if __name__ == '__main__':
    YilanApp().run()


