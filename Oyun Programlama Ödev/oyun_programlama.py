import pygame  # Pygame kütüphanesini içe aktarır
import random  # Rastgele sayı üretmek için random kütüphanesini içe aktarır
import sys  # Sistem fonksiyonlarını kullanmak için sys kütüphanesini içe aktarır
import os  # Dosya ve dizin işlemleri için os kütüphanesini içe aktarır

# Pygame'i başlat
pygame.init()  # Pygame'i başlatır

# Ekran boyutları
screen_width = 800  # Ekran genişliğini 800 piksel olarak ayarlar
screen_height = 600  # Ekran yüksekliğini 600 piksel olarak ayarlar

# Renk tanımları
white = (255, 255, 255)  # Beyaz rengi tanımlar
black = (0, 0, 0)  # Siyah rengi tanımlar

# Ekranı oluştur
screen = pygame.display.set_mode((screen_width, screen_height))  # Ekranı belirtilen boyutlarda oluşturur
pygame.display.set_caption("Uzay Savaşı")  # Ekran başlığını ayarlar

# Ses dosyalarını yükleme
shoot_sound = pygame.mixer.Sound("laser.wav")  # Ateş etme sesini yükler
hit_sound = pygame.mixer.Sound("boom1.wav")  # Vurma sesini yükler
crash_sound = pygame.mixer.Sound("atari_boom.wav")  # Çarpışma sesini yükler

# Müzik dosyasını yükleme ve çalma
pygame.mixer.music.load("SpaceMusic.mp3")  # Müzik dosyasını yükler
pygame.mixer.music.play(-1)  # Müziği döngü halinde çalar

# Uzay gemisi
spaceship = pygame.image.load("spaceship.png")  # Uzay gemisi resmini yükler
spaceship = pygame.transform.scale(spaceship, (50, 50))  # Uzay gemisini 50x50 piksel boyutunda ölçeklendirir
spaceship_rect = spaceship.get_rect()  # Uzay gemisinin dikdörtgenini alır
spaceship_rect.center = (screen_width // 2, screen_height - 50)  # Uzay gemisini ekranın altında ortalar

# Meteor animasyon çerçevelerini yükleme
meteor_frames = []  # Meteor çerçeveleri için bir liste oluşturur
meteor_folder = "Meteor"  # Meteor resimlerinin bulunduğu klasör adı
for i in range(1, 12):  # 1'den 11'e kadar olan çerçeveleri yükler
    frame_path = os.path.join(meteor_folder, f"meteor{i}.png")  # Her bir çerçevenin dosya yolunu oluşturur
    frame = pygame.image.load(frame_path)  # Çerçeve resmini yükler
    frame = pygame.transform.scale(frame, (50, 50))  # Çerçeveyi 50x50 piksel boyutunda ölçeklendirir
    meteor_frames.append(frame)  # Çerçeveyi listeye ekler

# Arka plan resimlerini yükleme
background_images = []  # Arka plan resimleri için bir liste oluşturur
background_folder = "Background"  # Arka plan resimlerinin bulunduğu klasör adı
for i in range(1, 7):  # 1'den 6'ya kadar olan arka plan resimlerini yükler
    bg_path = os.path.join(background_folder, f"space{i}.png")  # Her bir arka plan resminin dosya yolunu oluşturur
    bg_image = pygame.image.load(bg_path)  # Arka plan resmini yükler
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))  # Arka plan resmini ekran boyutlarına ölçeklendirir
    background_images.append(bg_image)  # Arka plan resmini listeye ekler

# Arka plan animasyon değişkenleri
background_index = 0  # İlk arka plan resminin indeksini ayarlar
background_timer = 0  # Arka plan değişimi için bir zamanlayıcı oluşturur
background_interval = 100  # Her arka plan resminin ekranda kalma süresini milisaniye cinsinden ayarlar

# Animasyon değişkenleri
frame_rate = 5  # Kaç oyun döngüsünde bir çerçeve değişeceğini ayarlar

# Mermi tanımları
bullet_image = pygame.image.load("bullet.png")  # Mermi resmini yükler
bullet_image = pygame.transform.scale(bullet_image, (80, 90))  # Mermiyi 80x90 piksel boyutunda ölçeklendirir
bullet_speed = 15  # Mermi hızını ayarlar

# Skor
score = 0  # Başlangıç skorunu sıfır olarak ayarlar
font = pygame.font.SysFont(None, 36)  # Skor metni için bir yazı tipi oluşturur

# Saat nesnesi (oyun döngüsünü kontrol etmek için)
clock = pygame.time.Clock()  # Oyun döngüsünü kontrol etmek için bir saat nesnesi oluşturur

# Oyun döngüsü
def game_loop():
    global score, background_index, background_timer  # Global değişkenleri tanımlar
    score = 0  # Skoru sıfırlar
    meteor_speed = 7  # Meteor hızını ayarlar
    spaceship_speed = 8  # Uzay gemisi hızını ayarlar
    running = True  # Oyun döngüsünün devam etmesi için bir değişken oluşturur
    current_frame = 0  # Şu anki çerçeveyi sıfır olarak ayarlar
    frame_counter = 0  # Çerçeve sayacını sıfır olarak ayarlar
    bullets = []  # Mermiler için bir liste oluşturur
    meteors = []  # Meteorlar için bir liste oluşturur
    
    # Uzay gemisi pozisyonunu resetler
    spaceship_rect.center = (screen_width // 2, screen_height - 50)  # Uzay gemisinin pozisyonunu resetler
    
    # Meteorları resetler ve yeniden oluşturur
    for i in range(7):  # 7 tane meteor oluşturur
        meteor_rect = meteor_frames[0].get_rect()  # Meteorun collider ını alır
        meteor_rect.x = random.randint(0, screen_width - meteor_rect.width)  # Meteorun x koordinatını rastgele belirler
        meteor_rect.y = random.randint(-screen_height, -meteor_rect.height)  # Meteorun y koordinatını rastgele belirler
        meteors.append(meteor_rect)  # Meteoru listeye ekler

    while running:  # Oyun döngüsü
        for event in pygame.event.get():  # Olayları kontrol eder
            if event.type == pygame.QUIT:  # Pencere kapatma olayı
                pygame.quit()  # Pygame'i kapatır
                sys.exit()  # Programı sonlandırır
            if event.type == pygame.KEYDOWN:  # Tuşa basma olayı
                if event.key == pygame.K_SPACE:  # Boşluk tuşuna basma olayı
                    # Mermiler oluşturur
                    bullet_rect_left = bullet_image.get_rect()  # Sol merminin dikdörtgenini alır
                    bullet_rect_right = bullet_image.get_rect()  # Sağ merminin dikdörtgenini alır
                    bullet_rect_left.midtop = spaceship_rect.midtop  # Sol mermiyi uzay gemisinin sol üst kenarına hizalar
                    bullet_rect_right.midtop = spaceship_rect.midtop  # Sağ mermiyi uzay gemisinin sağ üst kenarına hizalar
                    bullet_rect_left.x += 5  # Sol mermiyi daha sola kaydırır
                    bullet_rect_right.x += 35  # Sağ mermiyi daha sağa kaydırır
                    bullets.append(bullet_rect_left)  # Sol mermiyi listeye ekler
                    bullets.append(bullet_rect_right)  # Sağ mermiyi listeye ekler
                    shoot_sound.play()  # Ateş etme sesini çalar
        
        # Tuş basımları
        keys = pygame.key.get_pressed()  # Basılı tuşları kontrol eder
        if keys[pygame.K_LEFT] and spaceship_rect.left > 0:  # Sol tuşuna basılıysa ve uzay gemisi ekranın soluna çarpmamışsa
            spaceship_rect.x -= spaceship_speed  # Uzay gemisini sola hareket ettirir
        if keys[pygame.K_RIGHT] and spaceship_rect.right < screen_width:  # Sağ tuşuna basılıysa ve uzay gemisi ekranın sağına çarpmamışsa
            spaceship_rect.x += spaceship_speed  # Uzay gemisini sağa hareket ettirir
        
        # Meteor hareketi
        for meteor_rect in meteors:  # Her bir meteor için
            meteor_rect.y += meteor_speed  # Meteoru aşağı hareket ettirir
            if meteor_rect.top > screen_height:  # Meteor ekranın altına geçmişse
                meteor_rect.x = random.randint(0, screen_width - meteor_rect.width)  # Meteorun x koordinatını rastgele belirler
                meteor_rect.y = random.randint(-screen_height, -meteor_rect.height)  # Meteorun y koordinatını rastgele belirler
                score -= 1  # Skoru azaltır
        
        # Animasyon çerçevesini değiştirme
        frame_counter += 1  # Çerçeve sayacını arttırır
        if frame_counter >= frame_rate:  # Çerçeve sayacı frame_rate değerine ulaşmışsa
            frame_counter = 0  # Çerçeve sayacını sıfırlar
            current_frame = (current_frame + 1) % len(meteor_frames)  # Şu anki çerçeveyi değiştirir
        
        # Mermileri hareket ettir ve ekrandan çıkanları sil
        bullets[:] = [bullet for bullet in bullets if bullet.bottom > 0]  # Ekrandan çıkan mermileri listeden kaldırır
        for bullet in bullets:  # Her bir mermi için
            bullet.y -= bullet_speed  # Mermiyi yukarı hareket ettirir
        
        # Çarpışma kontrolü
        spaceship_collider = spaceship_rect.inflate(-20, -20)  # Uzay gemisinin çarpışma alanını küçültür
        
        for meteor_rect in meteors:  # Her bir meteor için
            meteor_collider = meteor_rect.inflate(-20, -20)  # Meteorun çarpışma alanını küçültür
            if spaceship_collider.colliderect(meteor_collider):  # Uzay gemisi meteorla çarpışırsa
                crash_sound.play()  # Çarpışma sesini çalar
                running = False  # Oyun döngüsünü durdurur
                game_over_screen()  # Oyun bitiş ekranını gösterir
        
            for bullet in bullets:  # Her bir mermi için
                bullet_collider = bullet.inflate(-5, -5)  # Merminin çarpışma alanını küçültür
                if bullet_collider.colliderect(meteor_collider):  # Mermi meteorla çarpışırsa
                    bullets.remove(bullet)  # Mermiyi listeden kaldırır
                    meteors.remove(meteor_rect)  # Meteoru listeden kaldırır
                    meteor_rect = meteor_frames[0].get_rect()  # Yeni bir meteor dikdörtgeni alır
                    meteor_rect.x = random.randint(0, screen_width - meteor_rect.width)  # Yeni meteorun x koordinatını rastgele belirler
                    meteor_rect.y = random.randint(-screen_height, -meteor_rect.height)  # Yeni meteorun y koordinatını rastgele belirler
                    meteors.append(meteor_rect)  # Yeni meteoru listeye ekler
                    score += 1  # Skoru arttırır
                    hit_sound.play()  # Vurma sesini çalar
                    break

        # Arka plan animasyonu
        background_timer += clock.get_time()  # Arka plan zamanlayıcısını arttırır
        if background_timer >= background_interval:  # Zamanlayıcı background_interval değerine ulaşmışsa
            background_timer = 0  # Zamanlayıcıyı sıfırlar
            background_index = (background_index + 1) % len(background_images)  # Arka plan resmini değiştirir

        # Ekranı çizme
        screen.blit(background_images[background_index], (0, 0))  # Arka plan resmini ekrana çizer
        screen.blit(spaceship, spaceship_rect)  # Uzay gemisini ekrana çizer
        for meteor_rect in meteors:  # Her bir meteor için
            screen.blit(meteor_frames[current_frame], meteor_rect)  # Meteoru ekrana çizer
        for bullet in bullets:  # Her bir mermi için
            screen.blit(bullet_image, bullet)  # Mermiyi ekrana çizer
        
        # Skoru ekranda gösterme
        score_text = font.render(f"Score: {score}", True, white)  # Skor metnini oluşturur
        screen.blit(score_text, (10, 10))  # Skor metnini ekrana çizer
        
        # Ekranı güncelleme
        pygame.display.flip()  # Ekranı günceller

        # Oyun döngüsünü yavaşlatma
        clock.tick(60)  # FPS'yi 60 ile sınırlandırır

def game_over_screen():
    game_over_font = pygame.font.SysFont(None, 72)  # Oyun bitiş metni için bir yazı tipi oluşturur
    restart_font = pygame.font.SysFont(None, 48)  # Yeniden başlatma metni için bir yazı tipi oluşturur
    game_over_text = game_over_font.render("Game Over", True, white)  # Oyun bitiş metnini oluşturur
    restart_text = restart_font.render("Press R to Restart or Q to Quit", True, white)  # Yeniden başlatma metnini oluşturur
    
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))  # Oyun bitiş metnini ekrana çizer
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))  # Yeniden başlatma metnini ekrana çizer
    pygame.display.flip()  # Ekranı günceller
    
    waiting = True  # Bekleme değişkenini ayarlar
    while waiting:  # Bekleme döngüsü
        for event in pygame.event.get():  # Olayları kontrol eder
            if event.type == pygame.QUIT:  # Pencere kapatma olayı
                pygame.quit()  # Pygame'i kapatır
                sys.exit()  # Programı sonlandırır
            if event.type == pygame.KEYDOWN:  # Tuşa basma olayı
                if event.key == pygame.K_r:  # R tuşuna basma olayı
                    waiting = False  # Bekleme döngüsünü durdurur
                    game_loop()  # Oyun döngüsünü yeniden başlatır
                if event.key == pygame.K_q:  # Q tuşuna basma olayı
                    pygame.quit()  # Pygame'i kapatır
                    sys.exit()  # Programı sonlandırır

# Oyunu başlat
game_loop()  # Oyun döngüsünü başlatır

# Pygame'i kapatma
pygame.quit()  # Pygame'i kapatır
sys.exit()  # Programı sonlandırır
