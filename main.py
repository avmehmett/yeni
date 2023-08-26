import os
from datetime import timedelta, datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from tradingview_ta import TA_Handler, Interval


def dosyaOku(dosyaAdi):
    with open(dosyaAdi, "r") as d:
        icerik = d.read()
    return icerik

def dosyaYaz(dosyaAdi, icerik):
    with open(dosyaAdi, "w") as d:
        d.write(icerik)

class GirisEkrani(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.password_input = TextInput(hint_text="Şifre", password=True, multiline=False)
        self.login_button = Button(text="Giriş", on_press=self.gir)

        layout.add_widget(self.password_input)
        layout.add_widget(self.login_button)

        self.add_widget(layout)

    def gir(self, instance):
        if self.password_input.text == "7590":
            self.manager.current = "anaSayfa"
        else:
            content = BoxLayout(orientation='vertical')
            labelGiris = Label(text=f'Şifre yanlış. Lütfen tekrar deneyiniz.')
            closeGiris_button = Button(text='Kapat', on_press=self.closeGiris_popup)

            content.add_widget(labelGiris)
            content.add_widget(closeGiris_button)

            self.popupGiris = Popup(title='Bilgilendirme', content=content, size_hint=(None, None), size=(400, 200))
            self.popupGiris.open()

    def closeGiris_popup(self, instance):
        self.popupGiris.dismiss()

class AnaSayfa(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.girBinanCom = Button(text="Binance.com Giriş", on_press=self.girBinanceCom)
        self.girBinanTr = Button(text="Binance.tr Giriş", on_press=self.girBinanceTr)
        self.cikisCom_button = Button(text="Çıkış", on_press=self.cikisCom)

        layout.add_widget(self.girBinanCom)
        layout.add_widget(self.girBinanTr)
        layout.add_widget(self.cikisCom_button)

        self.add_widget(layout)

    def girBinanceCom(self, instance):

        dosya_var_mi = os.path.exists("apiComDosyasi.txt")
        if dosya_var_mi:
            self.manager.current = "binanceComAnaSayfa"
        else:
            self.manager.current = "binanceComApi"

    def girBinanceTr(self, instance):

        dosya_var_mi = os.path.exists("apiTrDosyasi.txt")
        if dosya_var_mi:
            self.manager.current = "binanceTrAnaSayfa"
        else:
            self.manager.current = "binanceTrApi"

    def cikisCom(self, instance):
        App.get_running_app().stop()

class BinanceComApiSayfasi(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.apikeyCom_input = TextInput(hint_text="Api Key", multiline=False)
        self.secretkeyCom_input = TextInput(hint_text="Secret Key", multiline=False)
        self.kaydetCom_button = Button(text="Kaydet", on_press=self.kaydetCom)

        layout.add_widget(self.apikeyCom_input)
        layout.add_widget(self.secretkeyCom_input)
        layout.add_widget(self.kaydetCom_button)

        self.add_widget(layout)

    def kaydetCom(self, instance):
        comApi = self.apikeyCom_input.text
        comSecret = self.secretkeyCom_input.text

        try:
            self.dosyaislemleri.dosyaOku("apiComDosyasi.txt")
        except:
            dosyaYaz("apiComDosyasi.txt", f"{comApi, comSecret}")

        self.manager.current = "binanceComAnaSayfa"

class BinanceComAnaSayfa(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.txt3 = 0
        self.yapilacakIslem = "yapilacakislemMiktari.txt"
        self.yapilanIslem = "yapilanislemMiktari.txt"
        self.zaman = "zaman.txt"
        self.alSatCom_button = Button(text="Al-Sat", on_press=self.alSatCom)
        self.bakiyeCom_button = Button(text="Bakiye", on_press=self.bakiyeCom)
        self.transferCom_button = Button(text="Transfer", on_press=self.transferCom)
        self.kapatCom_button = Button(text="Ana Sayfaya Dön", on_press=self.kapatCom)
        self.cikisCom_button = Button(text="Çıkış", on_press=self.cikisCom)

        layout.add_widget(self.alSatCom_button)
        layout.add_widget(self.bakiyeCom_button)
        layout.add_widget(self.transferCom_button)
        layout.add_widget(self.kapatCom_button)
        layout.add_widget(self.cikisCom_button)

        self.add_widget(layout)

        self.simdikiZaman = datetime.now()

    def alSatCom(self, instance):

        try:
            dosyaOku(self.yapilacakIslem)
            dosyaOku(self.yapilanIslem)
            self.kayitliZaman = datetime.strptime(dosyaOku(self.zaman), "%Y-%m-%d %H:%M:%S")

            if self.simdikiZaman - self.kayitliZaman >= timedelta(days = 1):
                dosyaYaz(self.yapilacakIslem, "0")
                dosyaYaz(self.yapilanIslem, "0")
                self.kayitliZaman = self.simdikiZaman
                dosyaYaz(self.zaman, self.kayitliZaman.strftime("%Y-%m-%d %H:%M:%S"))
        except:
            dosyaYaz(self.yapilacakIslem, f"{self.txt3}")
            dosyaYaz(self.yapilanIslem, "0")
            self.kayitliZaman = self.simdikiZaman
            dosyaYaz(self.zaman, self.kayitliZaman.strftime("%Y-%m-%d %H:%M:%S"))

        yapilacak_islem = int(dosyaOku(self.yapilacakIslem))
        yapilan_islem = int(dosyaOku(self.yapilanIslem))

        if yapilan_islem > yapilacak_islem:
            layout = BoxLayout(orientation='vertical')
            content = BoxLayout(orientation='vertical')
            labelCom = Label(text=f'En son alınan kripto henüz satılmadı.\nVeya günlük işlem sayısına ulaştınız.\nLütfen daha sonra tekrar deneyiniz.')
            close_buttonCom = Button(text='Kapat', on_press=self.close_popupCom)

            content.add_widget(labelCom)
            content.add_widget(close_buttonCom)

            self.popupCom = Popup(title='Al-Sat Bilgisi', content=content, size_hint=(None, None), size=(400, 200),auto_dismiss=False)
            self.popupCom.open()

        else:
            if yapilacak_islem == 0:
                layout = BoxLayout(orientation='vertical')
                content = BoxLayout(orientation='vertical')
                self.spinner = Spinner(text='İşlem Sayısı Seç',
                                  values=('1 İşlem Yap', '2 İşlem Yap', '3 İşlem Yap', '4 İşlem Yap', '5 İşlem Yap'))
                self.spinner.bind(text=self.on_spinner_select)
                close_buttonCom = Button(text='Kapat', on_release=self.close1_popupCom)

                content.add_widget(self.spinner)
                content.add_widget(close_buttonCom)

                self.popupCom = Popup(title='İşlem Sayısı Bilgisi', content=content, size_hint=(None, None), size=(400, 200),
                                      auto_dismiss=False)
                self.popupCom.open()
            else:
                self.manager.current = "alSatSayfasi"

    def on_spinner_select(self, spinner, text):

        if text == "1 İşlem Yap":
            self.txt3 = 1
        elif text == "2 İşlem Yap":
            self.txt3 = 2
        elif text == "3 İşlem Yap":
            self.txt3 = 3
        elif text == "4 İşlem Yap":
            self.txt3 = 4
        elif text == "5 İşlem Yap":
            self.txt3 = 5

        dosyaYaz(self.yapilacakIslem, f"{self.txt3 }")
        dosyaYaz(self.yapilanIslem, f"{1}")
    def close1_popupCom(self, instance):
        self.popupCom.dismiss()
    def close_popupCom(self, instance):
        self.manager.current = "binanceComAnaSayfa"
        self.popupCom.dismiss()
    def bakiyeCom(self, instance):
        self.manager.current = "bakiyeComSayfa"

    def transferCom(self, instance):
        self.manager.current = "transferComSayfa"

    def kapatCom(self, instance):
        self.manager.current = "anaSayfa"

    def cikisCom(self, instance):
        App.get_running_app().stop()

class AlSatComSayfasi(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        self.binanceCom_label = Label(text = "", size_hint_y = 10)

        self.spinner = Spinner(
            text='Grafik Seç',
            values=('15 Dakikalık Grafik', '1 Saatlik Grafik', '4 Saatlik Grafik'),
            size_hint_y=10
        )
        self.spinner.bind(text=self.on_spinner_select)

        self.spinner2 = Spinner(
            text='Kar Oranı Seç',
            values=('%1 Kar Al', '%2 Kar Al', '%3 Kar Al', '%4 Kar Al', '%5 Kar Al', '%10 Kar Al',
                    '%15 Kar Al', '%20 Kar Al', '%25 Kar Al'),
            size_hint_y=10
        )
        self.spinner2.bind(text=self.on_spinner_select2)

        self.spinner3 = Spinner(
            text='İşlem Miktarı Seç',
            values=('Bakiyenin %25 ile İşlem Yap', 'Bakiyenin %50 ile İşlem Yap',
                    'Bakiyenin %75 ile İşlem Yap', 'Bakiyenin %100 ile İşlem Yap'),
            size_hint_y=10
        )
        self.spinner3.bind(text=self.on_spinner_select3)

        self.kaydet_button = Button(text="İşlem Aç", on_press=self.kaydet, size_hint_y=10)
        self.donCom_button = Button(text="Binance.COM Ana Sayfasına Dön", on_press=self.don, size_hint_y=10)

        layout.add_widget(self.binanceCom_label)
        layout.add_widget(self.spinner)
        layout.add_widget(self.spinner2)
        layout.add_widget(self.spinner3)
        layout.add_widget(self.kaydet_button)
        layout.add_widget(self.donCom_button)
        self.add_widget(layout)

    def on_pre_enter(self):
        self.yapilacakIslemler = int(dosyaOku("yapilacakislemMiktari.txt"))
        self.yapilanIslemler = int(dosyaOku("yapilanislemMiktari.txt"))
        self.binanceCom_label.text = f"Bugün için max {self.yapilacakIslemler} işlem yapılması istendi. " \
                                     f"\nKalan işlem sayısı : {self.yapilacakIslemler - self.yapilanIslemler + 1}"
    def on_spinner_select(self, spinner, text):
        if text == "15 Dakikalık Grafik":
            self.intervalSecimi = Interval.INTERVAL_15_MINUTES
        elif text == "1 Saatlik Grafik":
            self.intervalSecimi = Interval.INTERVAL_1_HOUR
        elif text == "4 Saatlik Grafik":
            self.intervalSecimi = Interval.INTERVAL_4_HOURS

    def on_spinner_select2(self, spinner, text):
        if text == "%1 Kar Al":
            self.karOraniSecimi = 0.012
        elif text == "%2 Kar Al":
            self.karOraniSecimi = 0.022
        elif text == "%3 Kar Al":
            self.karOraniSecimi = 0.032
        elif text == "%4 Kar Al":
            self.karOraniSecimi = 0.042
        elif text == "%5 Kar Al":
            self.karOraniSecimi = 0.052
        elif text == "%10 Kar Al":
            self.karOraniSecimi = 0.102
        elif text == "%15 Kar Al":
            self.karOraniSecimi = 0.152
        elif text == "%20 Kar Al":
            self.karOraniSecimi = 0.202
        elif text == "%25 Kar Al":
            self.karOraniSecimi = 0.252

    def on_spinner_select3(self, spinner, text):
        if text == "Bakiyenin %25 ile İşlem Yap":
            self.kullanilacakBakiyeSecimi = 0.25
        elif text == "Bakiyenin %50 ile İşlem Yap":
            self.kullanilacakBakiyeSecimi = 0.5
        elif text == "Bakiyenin %75 ile İşlem Yap":
            self.kullanilacakBakiyeSecimi = 0.75
        elif text == "Bakiyenin %100 ile İşlem Yap":
            self.kullanilacakBakiyeSecimi = 1

    def kaydet(self, instance):

        try:
            if self.karOraniSecimi != 0 and self.intervalSecimi != "" and self.kullanilacakBakiyeSecimi != 0:
                self.manager.current = "alSatIslemSayfasi"
        except:
            layout = BoxLayout(orientation='vertical')
            content = BoxLayout(orientation='vertical')
            self.label = Label(text='Seçim yapmadınız.',)
            close_buttonCom = Button(text='Kapat', on_press=self.close1_popupCom)

            content.add_widget(self.label)
            content.add_widget(close_buttonCom)

            self.popupCom = Popup(title='Uyarı !', content = content, size_hint=(None, None), size=(400, 200))
            self.popupCom.open()
    def close1_popupCom(self, instance):
            self.popupCom.dismiss()

    def don(self, instance):
        self.manager.current = "binanceComAnaSayfa"

class AlSatIslemSayfasi(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label_layout = BoxLayout(orientation = "vertical", size_hint_y = 70)

        self.baslatCom_label = Label(text="Lütfen işlemi başlatın.")
        self.kapatCom_button = Button(text="Kapat", on_press=self.kapatCom, size_hint_y=10)
        self.islemCom_button = Button(text = "İşlemi Başlat", size_hint_y = 10 )
        self.islemCom_button.bind(on_press = self.islemCom)


        self.layout.add_widget(self.label_layout)
        self.label_layout.add_widget(self.baslatCom_label)
        self.layout.add_widget(self.islemCom_button)
        self.layout.add_widget(self.kapatCom_button)

        self.add_widget(self.layout)

    def kapatCom(self, instance):
        self.manager.current = "binanceComAnaSayfa"

    def sorgulaCom(self, dt):

            if self.counter == 1:
                self.baslatCom_label.text = "İşlem Devam Ediyor. (1.)"

            elif self.counter == 2:
                self.baslatCom_label.text ="İşlem Devam Ediyor. (2.)"


            elif self.counter == 3:
                self.baslatCom_label.text = "İşlem Bitti."
                self.schedule_interval.cancel()

            for i in range(8):

                if i == 3:
                    self.counter += 1
                    break
                elif i == 5:
                    self.counter += 1
                    break
                elif i == 7:
                    self.counter += 1
                    break


    def islemCom(self, instance):

        islem = int(dosyaOku("yapilanislemMiktari.txt"))
        islem += 1
        dosyaYaz("yapilanislemMiktari.txt", f"{islem}")
        self.baslatCom_label.text = "İşlem Başladı."
        self.schedule_interval = Clock.schedule_interval(self.sorgulaCom, 0.2)
        self.counter = 0

class BakiyeComSayfasi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        self.bakiyeCom_label = Label(text="Bakiye Bilgisi ", size_hint_y = 80)
        self.transferCom_button = Button(text="Transfer", on_press=self.transferCom, size_hint_y = 10)
        self.gosterCom_button = Button(text="Bakiye Göster", on_press=self.gosterCom, size_hint_y=10)
        self.donCom_button = Button(text="Binance.COM Ana Sayfasına Dön", on_press=self.don, size_hint_y=10)

        layout.add_widget(self.bakiyeCom_label)
        layout.add_widget(self.gosterCom_button)
        layout.add_widget(self.transferCom_button)
        layout.add_widget(self.donCom_button)

        self.add_widget(layout)

    def gosterCom(self, instance):
        self.bakiyeCom_label.text = f"USDT Miktarı : {1000} $ \nTL Karşılığı : {float(1000) * float(25)} TL"
    def transferCom(self, instance):
        self.manager.current = "transferComSayfa"

    def don(self, instance):
        self.manager.current = "binanceComAnaSayfa"

class TransferComSayfasi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.bakiyeCom_label = Label(text="Bakiye Bilgisi", size_hint_y = 70)
        self.miktarCom_input = TextInput(hint_text="Transferedilecek USDT miktarı gir.", size_hint_y = 10)
        self.transferEtCom_button = Button(text="Transfer Et", on_press=self.transferEtCom, size_hint_y = 10)
        self.gosterCom_button = Button(text="Bakiye Göster", on_press=self.gosterCom, size_hint_y=10)
        self.donCom_button = Button(text="Binance.COM Ana Sayfasına Dön", on_press=self.don, size_hint_y=10)

        layout.add_widget(self.bakiyeCom_label)
        layout.add_widget(self.miktarCom_input)
        layout.add_widget(self.gosterCom_button)
        layout.add_widget(self.transferEtCom_button)
        layout.add_widget(self.donCom_button)

        self.add_widget(layout)

    def gosterCom(self, instance):
        self.bakiyeCom_label.text = f"USDT Miktarı : {1000} $ \nTL Karşılığı : {float(1000) * float(25)} TL"
    def transferEtCom(self, instance):
        content = BoxLayout(orientation='vertical')
        labelCom = Label(text=f'Transfer edildi')
        closeCom_button = Button(text='Kapat', on_press=self.closeCom_popup)

        content.add_widget(labelCom)
        content.add_widget(closeCom_button)

        self.popupCom = Popup(title='Transfer Bilgisi', content=content, size_hint=(None, None), size=(400, 200), auto_dismiss=False)
        self.popupCom.open()

    def closeCom_popup(self, instance):
        self.manager.current = "binanceComAnaSayfa"
        self.popupCom.dismiss()

    def don(self, instance):
        self.manager.current = "binanceComAnaSayfa"

class BinanceTrApiSayfasi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.apikeyTr_input = TextInput(hint_text="Api Key", multiline=False)
        self.secretkeyTr_input = TextInput(hint_text="Secret Key", multiline=False)
        self.kaydetTr_button = Button(text="Kaydet", on_press=self.kaydetTr)

        layout.add_widget(self.apikeyTr_input)
        layout.add_widget(self.secretkeyTr_input)
        layout.add_widget(self.kaydetTr_button)

        self.add_widget(layout)

    def kaydetTr(self, instance):

        trApi = self.apikeyTr_input.text
        trSecret = self.secretkeyTr_input.text

        try:
            dosyaOku("apiTrDosyasi.txt")
        except:
            dosyaYaz("apiTrDosyasi.txt", f"{trApi, trSecret}")

        self.manager.current = "binanceTrAnaSayfa"

class BinanceTrAnaSayfa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.bakiyeTr_button = Button(text="Bakiye", on_press=self.bakiyeTr)
        self.transferTr_button = Button(text="Transfer", on_press=self.transferTr)
        self.kapatTr_button = Button(text="Ana Sayfaya Dön", on_press=self.kapatTr)
        self.cikisTr_button = Button(text = "Çıkış", on_press = self.cikisTr)

        layout.add_widget(self.bakiyeTr_button)
        layout.add_widget(self.transferTr_button)
        layout.add_widget(self.kapatTr_button)
        layout.add_widget(self.cikisTr_button)

        self.add_widget(layout)

    def bakiyeTr(self, instance):
        self.manager.current = "bakiyeTrSayfa"

    def transferTr(self, instance):
        self.manager.current = "transferTrSayfa"

    def kapatTr(self, instance):
        self.manager.current = "anaSayfa"

    def cikisTr(self, instance):
        App.get_running_app().stop()

class BakiyeTrSayfasi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.bakiyeTr_label = Label(text="Tr Bakiye Bilgisi", size_hint_y = 90)
        self.transferTr_button = Button(text="Transfer", on_press=self.transferTr, size_hint_y = 10)
        self.gosterTr_button = Button(text="Bakiye Göster", on_press=self.gosterTr, size_hint_y=10)
        self.donTr_button = Button(text="Binance.TR Ana Sayfasına Dön", on_press=self.don, size_hint_y=10)

        layout.add_widget(self.bakiyeTr_label)
        layout.add_widget(self.gosterTr_button)
        layout.add_widget(self.transferTr_button)
        layout.add_widget(self.donTr_button)


        self.add_widget(layout)

    def gosterTr(self, instance):
        self.bakiyeTr_label.text = f"USDT Miktarı : {1000} $ \nTL Karşılığı : {float(1000) * float(25)} TL"

    def transferTr(self, instance):
        self.manager.current = "transferTrSayfa"

    def don(self, instance):
        self.manager.current = "binanceTrAnaSayfa"

class TransferTrSayfasi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.bakiyeTr_label = Label(text="Tr Bakiye Bilgisi", size_hint_y = 90)
        self.miktarTr_input = TextInput(hint_text="Transferedilecek USDT miktarı gir.", size_hint_y = 10)
        self.transferEtTr_button = Button(text="Transfer Et", on_press=self.transferEtTr, size_hint_y = 10)
        self.gosterTr_button = Button(text="Bakiye Göster", on_press=self.gosterTr, size_hint_y=10)
        self.donTr_button = Button(text="Binance.TR Ana Sayfasına Dön", on_press=self.don, size_hint_y=10)

        layout.add_widget(self.bakiyeTr_label)
        layout.add_widget(self.miktarTr_input)
        layout.add_widget(self.gosterTr_button)
        layout.add_widget(self.transferEtTr_button)
        layout.add_widget(self.donTr_button)

        self.add_widget(layout)

    def gosterTr(self, instance):
        self.bakiyeTr_label.text = f"USDT Miktarı : {1000} $ \nTL Karşılığı : {float(1000) * float(25)} TL"


    def transferEtTr(self, instance):
        content = BoxLayout(orientation='vertical')
        labelTr = Label(text=f'Tr Transfer edildi')
        closeTr_button = Button(text='Kapat', on_press=self.close_popupTr)

        content.add_widget(labelTr)
        content.add_widget(closeTr_button)

        self.popupTr = Popup(title='Tr Transfer Bilgisi', content=content, size_hint=(None, None), size=(400, 200), auto_dismiss=False)
        self.popupTr.open()

    def close_popupTr(self, instance):
        self.manager.current = "binanceTrAnaSayfa"
        self.popupTr.dismiss()

    def don(self, instance):
        self.manager.current = "binanceTrAnaSayfa"

class Uygulama(App):

    def build(self):
        self.title = "Binance Botum"

        self.screenManager = ScreenManager()

        self.girisEkrani = GirisEkrani()
        self.anaSayfa = AnaSayfa(name = "anaSayfa")

        # BİNANCE COM
        self.binanceComApi = BinanceComApiSayfasi(name = "binanceComApi")
        self.binanceComAnaSayfa = BinanceComAnaSayfa(name = "binanceComAnaSayfa")
        self.alsatComSayfasi = AlSatComSayfasi(name = "alSatSayfasi")
        self.alSatIslemleriSayfasi = AlSatIslemSayfasi(name = "alSatIslemSayfasi")
        self.bakiyeComSayfasi = BakiyeComSayfasi(name = "bakiyeComSayfa")
        self.transferComSayfasi = TransferComSayfasi(name = "transferComSayfa")

        # BİNANCE TR
        self.binanceTrApi = BinanceTrApiSayfasi(name="binanceTrApi")
        self.binanceTrAnaSayfa = BinanceTrAnaSayfa(name="binanceTrAnaSayfa")
        self.bakiyeTrSayfasi = BakiyeTrSayfasi(name="bakiyeTrSayfa")
        self.transferTrSayfasi = TransferTrSayfasi(name="transferTrSayfa")

        self.screenManager.add_widget(self.girisEkrani)
        self.screenManager.add_widget(self.anaSayfa)

        # BİNANCE COM
        self.screenManager.add_widget(self.binanceComApi)
        self.screenManager.add_widget(self.binanceComAnaSayfa)
        self.screenManager.add_widget(self.alsatComSayfasi)
        self.screenManager.add_widget(self.alSatIslemleriSayfasi)
        self.screenManager.add_widget(self.bakiyeComSayfasi)
        self.screenManager.add_widget(self.transferComSayfasi)

        # BİNANCE TR
        self.screenManager.add_widget(self.binanceTrApi)
        self.screenManager.add_widget(self.binanceTrAnaSayfa)
        self.screenManager.add_widget(self.bakiyeTrSayfasi)
        self.screenManager.add_widget(self.transferTrSayfasi)

        return self.screenManager

if __name__ == "__main__":
    uygulama = Uygulama()
    uygulama.run()

