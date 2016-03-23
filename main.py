import kivy
__version__ = '1.9.1'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.graphics import *
from random import randint
from kivy import vector

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

    def basla(self):
        self.yeni_yilan()
        self.update()

    def reset(self):
        self.donus_sayici = 0
        self.skor = 0
        self.yilan.sil()
        self.meyve.sil()

    def yeni_yilan(self):
        baslangic_koord = (randint(2, self.satir_sayi - 2),
                           randint(2, self.sutun_sayi - 2))

        self.yilan.pozisyon_ayarla(baslangic_koord)
        rand_indis = randint(0, 3)
        baslangic_yon =["Up", "Down", "Left", "Right"][rand_indis]
        self.yilan.yon_ayarla(baslangic_koord)

    def meyve_cikar(self, *args):
        random_koord = [
            randint(1, self.satir_sayi), randint(1, self.sutun_sayi)]

    # yilanin oldugu hucrelerin pozisyonlarini alioruz.
        yilan_nerde = self.Yilan.tam_pozisyon_al()

    # meyvenin oldugu yerde yilan varsa yeni meyve cikar
        while random_koord in yilan_nerde:
            random_koord = [
            randint(1, self.satir_sayi), randint(1, self.sutun_sayi)]

        self.meyve_cikar(random_koord)

    def yenilgi_kontrol(self):
        yilan_pozisyon = self.Yilan.pozisyon_al()
        if yilan_pozisyon in self.YilanKuyruk.blok_pozisyonu:
            return True
        if yilan_pozisyon[0] > self.satir_sayi \
            or yilan_pozisyon[0] < 1 \
            or yilan_pozisyon[1] > self.sutun_sayi \
            or yilan_pozisyon[1] < 1:
            return True
        return False

    def update(self, *args):
        self.Yilan.hareket()
        if self.yenilgi_kontrol():
            self.reset()
            self.basla()
            return

        if self.Meyve.is_on_board():
            if self.Yilan.pozisyon_al() == self.Meyve.poz:
                self.Meyve.sil()
                self.skor += 1
                self.YilanKuyruk.size += 1
        self.donus_sayici += 1

    def on_touch_down(self, touch):
        self.dokunma_baslgnc_poz = touch.spos

    def on_touch_move(self, touch):
        delta = vector(*touch.spos) - vector(*self.dokunma_baslgnc_poz)

        if not self.eylem_tetiklendi \
                and (abs(delta[0]) > 0.1 or abs(delta[1]) > 0.1):
            if abs(delta[0]) > abs(delta[1]):
                if delta[0] > 0:
                    self.Yilan.yon_ayarla("Right")
                else:
                    self.Yilan.yon_ayarla("Left")
            else:
                if delta[1] > 0:
                    self.Yilan.yon_ayarla("Up")
                else:
                    self.Yilan.yon_ayarla("Down")
        self.eylem_tetiklendi = True

    def on_touch_up(self, touch):
        self.eylem_tetiklendi = False

class Meyve(Widget):
    duration = NumericProperty(10)
    interval = NumericProperty(3)

    object_on_board = ObjectProperty(None)
    durum = BooleanProperty(False)

    def is_on_board(self):
        return self.durum

    def sil(self, *args):
        if self.is_on_board():
            self.canvas.remove(self.object_on_board)
            self.object_on_board = ObjectProperty(None)
            self.durum = False
    def cikar(self, poz):
        self.poz = poz

        with self.canvas:
            x = (poz[0] -1) * self.size[0]
            y = (poz[1] -1) * self.size[1]
            koord = (x, y)

            self.object_on_board = Ellipse(pos=koord, size=self.size)
            self.durum = True


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


