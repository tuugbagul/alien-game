import time
import random

from grafik.canvas import Canvas

# # windows için aşağıdaki satırı yorumdan kaldırın
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
# # Mac için aşağıdaki satırı yorumdan kaldırın
# from playsound import playsound


""" sabit değişkenler """
# Kanvas değişkenleri
KANVAS_EN = 500
KANVAS_BOY = 750
YENILEME_SURESI = 0.01


# Harita değişkenleri
YAZILAR_Y_KOORDINATI = 25
YAZILAR_X_AYRIMI = 50

UZAYLI_SATIR_SAYISI = 3
UZAYLI_SUTUN_SAYISI = 3
UZAYLI_BOYUT = 25
UZAYLI_MIN_HIZ = 5
UZAYLI_MAX_HIZ = 10

ANA_KARAKTER_BOYUT = 50

LAZER_BOYUT = 10

FONT = "Cambria"
FONT_BUYUKLUGU = 14

# Oyun değişkenleri
TOPLAM_CANLAR = 5
KAZANMA_SKORU = 300

# Resimler
UZAYLI_RESMI = "resimler/uzayli.png"
ANA_KARAKTER_RESMI = "resimler/ana_karakter.png"
LAZER_RESMI = "resimler/lazer.png"

# Sesler (BONUS)
CARPISMA_SESI_WINDOWS = "sesler/oldu.wav"
CARPISMA_SESI_MAC = "sesler/oldu.au"
""" kod """


def uzaylilari_olustur(kanvas,satir_sayisi,sutun_sayisi,uzayli_resmi):
    """ belirtilen sütun x satır sayısı kadar uzaylı yaratır
        uzaylıları uzayli_resmi isimli paramteredeki resim olarak kanvasa ekler
        yaratılan uzaylıları içeren bir liste döndürür """
    uzayli_listesi= list()
    for satir in range(satir_sayisi):
        for sutun in range(sutun_sayisi):
            uzayli = kanvas.create_image_with_size(satir * YAZILAR_Y_KOORDINATI + 20,
                                                         sutun* YAZILAR_Y_KOORDINATI + 50, UZAYLI_BOYUT,
                                                         UZAYLI_BOYUT, UZAYLI_RESMI)
            uzayli_listesi.append(uzayli)
    return uzayli_listesi


def uzaylilari_rastgele_dagit(kanvas, ana_karakter, uzayli_listesi):
    """
    uzaylilari kanvas uzerinde ana_karakter ile kesismeyen koordinatlara rastgele yerlestirir.
    """
    for i in range(len(uzayli_listesi)):
        uzayli = uzayli_listesi[i]
        ana_karakter_x = kanvas.get_left_x(ana_karakter)
        ana_karakter_y = kanvas.get_top_y(ana_karakter)
        uzayli_x = random.randint(ana_karakter_x-25,KANVAS_EN)
        uzayli_y = random.randint(ana_karakter_x-25,KANVAS_BOY)
        kanvas.move(uzayli, uzayli_x, uzayli_y)


def uzaylilar_hiz_listesi_olustur(n):
    """
    Uzaylilarin hepsinin random bir sekilde etrafa savrulmasini saglamak icin
     random sekilde uretilmis vektor listesi döndürür
    """
    hiz_listesi = list()
    for uzayli in range(n):
        hiz_x = random.randint(UZAYLI_MIN_HIZ, UZAYLI_MAX_HIZ)
        hiz_y = random.randint(UZAYLI_MIN_HIZ, UZAYLI_MAX_HIZ)
        hiz_listesi.append([hiz_x, hiz_y])
    return hiz_listesi


def uzaylilari_hareket_ettir(kanvas, uzayli_listesi, hiz_listesi):
    """
    uzayli_listesi'ndeki her bir uzayliyi hiz_listesi'nde verilen hizlara gore hareket ettirir.
    Bu hareket sonrasında uzaylilarin duvara carpip carpmadigini kontrol edip,
    eger carptiysa bu uzaylilarin hiz listesindeki hizini carptigi duvara gore gunceller.
    """
    for b in range(len(uzayli_listesi)):
        uzayli = uzayli_listesi[b]
        dx = hiz_listesi[b][0]
        dy = hiz_listesi[b][1]
        kanvas.move(uzayli, dx, dy)

        if kanvas.get_top_y(uzayli) <= 0 or kanvas.get_top_y(uzayli) + UZAYLI_BOYUT >= KANVAS_BOY:
                hiz_listesi[b][1] *= -1
        if kanvas.get_left_x(uzayli) <= 0 or kanvas.get_left_x(uzayli) + UZAYLI_BOYUT >= KANVAS_EN:
                hiz_listesi[b][0] *= -1
        kanvas.update()



def ana_karakteri_guncelle(kanvas, ana_karakter):
    """
    Ana karakterimizin bulundugu yeri mouse'in bulundugu koordinatalara gore guncelleyen bir fonksiyon.
    Ana karakterimizin merkez noktası mouseun koordinatlarına denk gelmeli.
    Bonus: En basit haliyle mouse'n olduğu yere karakterinizi gönderirseniz karngelleyin
    Bonus 2: Oyunu zorlaştırmak için karakterin ilerleyebileceği bir maksimum hız ekleyin.
        Örneğin her animasyon karesinde mouse'un koordinatlarına doğru maksimum x birim ilerle
    """
    yeni_x = kanvas.get_mouse_x() - ANA_KARAKTER_BOYUT / 2
    yeni_y = kanvas.get_mouse_y() - ANA_KARAKTER_BOYUT / 2
    kanvas.move_to(ana_karakter, yeni_x, yeni_y)


def carpismalari_kontrol_et(kanvas, ana_karakter, uzayli_listesi):
    """ ana karakterin uzaylılarla çarpışmasını kontrol edelim
        eğer uzaylı ile çarpışıldıysa True, çarpışılmadıysa False döndürün """
    x1= kanvas.get_left_x(ana_karakter)
    y1= kanvas.get_top_y(ana_karakter)
    x2= x1 + ANA_KARAKTER_BOYUT
    y2= y1 + ANA_KARAKTER_BOYUT

    liste_1 = kanvas.find_overlapping(x1,y1,x2,y2)

    for i in liste_1:
        if i in uzayli_listesi:
           return True
    return False


def bitis_yazisi_olustur(kanvas, yazi):
    """ oyunun bitiminde kanvastaki objeleri silin ve verilen mesajı kanvasın ortasında oluşturun """
     # while True'nın içinde oluşturdum çünkü burada diğer değişkenler tanımlanmamıştı.


""" bonus başlangıç """


def yeni_lazerleri_ekle(kanvas, ana_karakter, lazerler):
    """ kullanıc ASDW tuşlarından birine bastıysa yeni lazer ekleyelim
        oluşturulan lazerleri lazerler isimli bir dictionary'ye ekleyelim """
    # lazer yollamak için kullanıcının klavye hareketlerini kontrol etmeliyiz
    pass


def lazerleri_hareket_ettir(kanvas, lazerler, uzayli_listesi):
    """ lazerler dictionary'si içindeki lazerleri hareket ettirelim, lazerin çarpıştığı uzaylıları silinecek
    uzaylilar isimli bir sete ekleyelim
        her lazer için ekranın dışına çıkıp çıkmama durumunu kontrol edelim
    """
    pass


def lazer_olustur(kanvas, x, y):
    """ verilen x ve y koordinatında lazer oluşturun
        lazeri resimler/lazer.png'de bulabilirsiniz
        lazerin boyutu LAZER_BOYUT değişkeniyle size verilmiştir """
    pass


def olen_uzaylilari_kaldir(kanvas, silinecek_uzaylilar, uzayli_listesi, hiz_listesi):
    """ silinecek uzaylilar'da bulunan uzaylıları kanvastan, uzayli_listesinden ve hiz_listesinden
        kaldırın """
    pass


""" bonus bitiş """


def main():
    kanvas = Canvas(KANVAS_EN, KANVAS_BOY)
    kanvas.set_canvas_title("Final Projesi")
    # oyun ekranını ayarlayalım, oyuncu canlarını ve skoru başlatın, kanvasa yazı olarak ekleyin
    canlar= TOPLAM_CANLAR
    skor= 0
    can_yazisi= kanvas.create_text(KANVAS_EN-2*YAZILAR_X_AYRIMI,YAZILAR_Y_KOORDINATI,'\u2764\ufe0f'*canlar)
    kanvas.set_font(can_yazisi,FONT,FONT_BUYUKLUGU)
    skor_yazisi= kanvas.create_text(YAZILAR_X_AYRIMI,YAZILAR_Y_KOORDINATI,'Skor:'+ str(skor))
    kanvas.set_font(skor_yazisi,FONT,FONT_BUYUKLUGU)
    # uzaylıları oluşturun
    uzayli_listesi= uzaylilari_olustur(kanvas,UZAYLI_SATIR_SAYISI,UZAYLI_SUTUN_SAYISI,'resimler/uzayli.png')
    # hiz listesini oluşturun
    hiz_listesi = uzaylilar_hiz_listesi_olustur(UZAYLI_SATIR_SAYISI*UZAYLI_SUTUN_SAYISI)
    # ana karakteri oluşturun
    ana_karakter = kanvas.create_image_with_size(KANVAS_EN/2-ANA_KARAKTER_BOYUT,KANVAS_BOY/2-ANA_KARAKTER_BOYUT,ANA_KARAKTER_BOYUT,ANA_KARAKTER_BOYUT,ANA_KARAKTER_RESMI)
    # oyunun animasyon döngüsünü ayarlayın
    while True:
        # skoru güncelleyin
        skor += 1
        kanvas.set_text(skor_yazisi,'Skor:'+ str(skor))
        # ana karakterin konumunu güncelleyin
        ana_karakteri_guncelle(kanvas,ana_karakter)
        # uzaylıları hareket ettirin
        uzaylilari_hareket_ettir(kanvas,uzayli_listesi,hiz_listesi)
         # uzaylı ve ana karakter arasındaki çarpışmaları kontrol edip çarpışma olduysa oyuncunun canlarını bir azaltın,
        # ekranda gözüken can yazısını güncelleyin
        if carpismalari_kontrol_et(kanvas,ana_karakter,uzayli_listesi):
            canlar = canlar -1
            kanvas.set_text(can_yazisi,'\u2764\ufe0f'*canlar)
            uzaylilari_rastgele_dagit(kanvas,ana_karakter,uzayli_listesi)
        # kazanıp kazanmadığımızı kontrol edin

        # her aşamada kanvası yenileyin
        kanvas.update()
        time.sleep(YENILEME_SURESI)

        # bitiş yazılarını ekrana ekleyin
        if canlar == 0:
            kanvas.delete_all()
            kaybetti_yazisi= kanvas.create_text(KANVAS_EN/2,KANVAS_BOY/2," Kaybettiniz \uD83D\uDE80")
            break

        elif skor == KAZANMA_SKORU:
            kanvas.delete_all()
            kazandi_yazisi = kanvas.create_text(KANVAS_EN/2,KANVAS_BOY/2, "Kazandınız \uD83D\uDE80")
            break
        time.sleep(YENILEME_SURESI)

    kanvas.wait_for_click()


if __name__ == "__main__":
    main()