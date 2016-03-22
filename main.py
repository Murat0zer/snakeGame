import kivy
__version__ = '1.9.1'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import *
import Canvas


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

    puanlar = ListProperty([0]*6)
    object_onboard = ObjectProperty(None)
    durum = BooleanProperty(False)




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
                blok = Canvas.Rectangle(poz=koord, size=(self.width,
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


