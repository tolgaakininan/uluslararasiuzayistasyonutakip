from datetime import *
import requests
from smtplib import *
from time import sleep


KULLANICI_ENLEM = 41.008240
KULLANICI_BOYLAM = 28.978359

parameters = {
    "lat": KULLANICI_ENLEM,
    "lng": KULLANICI_BOYLAM,
    "formatted": 0
}

KULLANICI_EMAIL= # GMAIL HESABINIZI GİRİN
KULLANICI_SIFRE= # GMAIL HESABINIZDAN AYARLARA GIRIP UYGULAMA ŞİFRELERİ KISMINDAN ALDIĞINIZ 16 HANELİ ŞİFREYİ GİRİN
HEDEF_ADRES= # E-POSTANIN GONDERILECEGI MAIL HESABINI GİRİN


def iss_kontrol():
    # HAVA KARANLIK MI DİYE KONTROL EDİYORUZ
    if kullanici_zaman >= gunesbatisi_veri or kullanici_zaman <= günesdogmasi_veri:
        # ISS YAKINDA MI DİYE KONTROL EDİYORUZ
        if 5 > boylam_veri - KULLANICI_ENLEM > -5 and 5 > enlem_veri - KULLANICI_ENLEM > -5:
            baglanti = SMTP("smtp.gmail.com")
            baglanti.login(email=KULLANICI_EMAIL, password=KULLANICI_SIFRE)
            baglanti.starttls()
            baglanti.sendmail(from_addr=KULLANICI_EMAIL, to_addrs=HEDEF_ADRES,
                              msg="Subject:ISS REPORT\n\n ISS tam olarak üstünde")


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
enlem_veri = float(response.json()["iss_position"]["latitude"])
boylam_veri = float(response.json()["iss_position"]["longitude"])


# GÜNEŞ BATIŞI VE DOĞUŞU İLE ALAKALI VERİYİ API SAYESİNDE ALIYORUZ
response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
gunesbatisi_veri = float(str(response.json()["results"]["sunset"]).split("T")[1].split(":")[0])
günesdogmasi_veri = float(str(response.json()["results"]["sunrise"]).split("T")[1].split(":")[0])
kullanici_zaman = datetime.now().hour

while True:
    iss_kontrol()
    sleep(60)
