import pygame,random,time,cv2,pyautogui
import numpy as np

# Pygame ve OpenCV ayarları
pygame.init()
ekran = pygame.display.set_mode((400, 600))

pygame.display.set_caption("Yeşil Yuvarlak Oyunu")

siyah = (0, 0, 0)
beyaz = (255, 255, 255)
yesil = (0, 255, 0)
kirmizi = (255, 0, 0)

class Daire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.yarıçap = 20
        self.yarıçap = random.uniform(5, 25)
        self.renk = yesil
        #self.hız = random.uniform(0, 3)
        self.hız = 10

    def çiz(self):
        pygame.draw.circle(ekran, self.renk, (self.x, self.y), self.yarıçap)

    def güncelle(self):
        self.y += self.hız

class Bomba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
#        self.yarıçap = 20
        self.yarıçap = random.uniform(5, 25)

        self.renk = kirmizi
        #self.hız = random.uniform(0, 3)
        self.hız = 3

    def çiz(self):
        pygame.draw.circle(ekran, self.renk, (self.x, self.y), self.yarıçap)

    def güncelle(self):
        self.y += self.hız

oyun_bitti = False
skor = 0
oyun_suresi = 15
baslangic_zamani = time.time()
daireler = []
bombalar = []

font = pygame.font.Font(None, 36)
skor_metni = font.render("Skor: " + str(skor), True, beyaz)
sure_metni = font.render("Kalan Süre: " + str(oyun_suresi), True, beyaz)
rest_of_time=3
total_score=0
# Ekranın sol üst köşesinin koordinatları
x, y = 200, 100
# Ekran boyutları
width, height = 400, 600

def cek_ve_isle():
    # Ekran görüntüsünü al
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    # Ekran görüntüsünü NumPy dizisine dönüştür
    frame = np.array(screenshot)
    # OpenCV'nin BGR formatına dönüştür
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Yeşil nesneleri tespit etmek için renk aralığı belirle
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Nesne konumlarını belirle
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Nesneleri tıkla
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:  # Belirli bir alan eşiğinden büyük nesneleri tıkla
            moments = cv2.moments(contour)
            if moments['m00'] != 0:
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
                
                # Tıklama işlemi
                pyautogui.click(x + cx, y + cy)


ekran.fill(siyah)
time.sleep(3)

while True:
    if not oyun_bitti:
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyun_bitti = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for daire in daireler:
                    if daire.x - daire.yarıçap < x < daire.x + daire.yarıçap and daire.y - daire.yarıçap < y < daire.y + daire.yarıçap:
                        skor += 1
                        daireler.remove(daire)
                        break

                for bomba in bombalar:
                    if bomba.x - bomba.yarıçap < x < bomba.x + bomba.yarıçap and bomba.y - bomba.yarıçap < y < bomba.y + bomba.yarıçap:
                        skor = 0
                        bombalar.remove(bomba)
                        break

        ekran.fill(siyah)

        if random.random() < 0.9:#             yogunlugunu buradan ayarlıyorsun 
            x = random.randint(0, ekran.get_width() - 40)
            y = -40
            daireler.append(Daire(x, y))

        if random.random() < 0.05:
            x = random.randint(0, ekran.get_width() - 60)
            y = -60
            bombalar.append(Bomba(x, y))

        for daire in daireler:
            daire.güncelle()
            daire.çiz()

        for bomba in bombalar:
            bomba.güncelle()
            bomba.çiz()
            
        
        cek_ve_isle()
        skor_metni = font.render("Skor: " + str(skor), True, beyaz)
        sure_metni = font.render("Kalan Süre: " + str(int(oyun_suresi - (time.time() - baslangic_zamani))), True, beyaz)

        ekran.blit(skor_metni, (10, 10))
        ekran.blit(sure_metni, (10, 50))

        pygame.display.update()

        if time.time() - baslangic_zamani >= oyun_suresi:
            oyun_bitti = True
    else :
        while oyun_bitti:
            if rest_of_time!=0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:                    
                        pygame.quit()
                        print("Oyun Bitti!")
                        print("Skorunuz:", skor)
                        exit()
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 150 < x < 250 and 450 < y < 500:
                            baslangic_zamani=time.time()
                            rest_of_time-=1
                            total_score+=skor
                            oyun_bitti= False  # Oyunu yeniden başlat

                ekran.fill(siyah)
                skor_metni = font.render("Skor: " + str(skor), True, beyaz)
                tekrar_oyna_metni = font.render(f"Tekrar Oyna {rest_of_time}", True, beyaz)
                ekran.blit(skor_metni, (100, 200))
                ekran.blit(tekrar_oyna_metni, (150, 450))
                pygame.display.update()
            else:                    
                pygame.quit()
                print("Oyun Bitti!")
                print("toplam Skorunuz:", total_score)
                exit()
        
