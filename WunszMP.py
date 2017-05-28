import sys, random, pygame
from pygame.locals import *

pygame.init()

#sound = pygame.mixer.Sound('plum.wav') #dzwiek zjadanego jablka
#pygame.mixer.music.load('betowen.mp3') #muzyka w tle
#pygame.mixer.music.play(-1, 0.0) # -1 to jest zapetlanie piosenki, zero to moment od ktorego jest odtwarzana piosenka

FPS = 10    #im wiecej tym szybciej porusza sie waz
szerokosc = 500
wysokosc = 500
kratka = 20 #szerokosc jednej kratki
szerokosc_pola = int(szerokosc / kratka)
wysokosc_pola = int(wysokosc / kratka)

# kolory RGB do zmiennych
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
NIEBIESKI = (0, 0, 255)
CZERWONY = (220, 0, 0)
ZIELONY = (0, 200, 0)
ZIELONYHEAD = (0, 255, 0)
FIOLET = (147, 112, 219)
ZOLTY = (255, 255, 0)
CIEMNY_ZIELONY = (0, 150, 0)
SZARY = (30, 30, 30)
TLO_KOLOR = CZARNY

# kierunki poruszania:
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

glowa = 0  # do koordynatow pogladowo zeby nie pisac zero jako glowa, dla czytelnosci kodu


def main():
    global zegar_fps, mapa, czcionka
    pygame.init()
    zegar_fps = pygame.time.Clock()
    mapa = pygame.display.set_mode((szerokosc, wysokosc))
    czcionka = pygame.font.SysFont("Comic Sans MS", 18)
    pygame.display.set_caption('WunszMP')

    ekran_startowy()
    while True:
        odpalenie_gry()
        gameover_screen()


def ekran_startowy():
    czcionka_start = pygame.font.Font('freesansbold.ttf', 100)
    start_powierzchnia = czcionka_start.render('SNAKE!', True, BIALY)
    kat = 10

    while True:
        mapa.fill(TLO_KOLOR)
        obrocony_napis = pygame.transform.rotate(start_powierzchnia, kat)
        obrocone_pole = obrocony_napis.get_rect()
        obrocone_pole.center = (szerokosc / 2, wysokosc / 2)
        mapa.blit(obrocony_napis, obrocone_pole)

        menu_poczatkowe()
        pygame.display.update()
        if SprawdzCzyKlawisz():
            pygame.event.get()
            return


def menu_poczatkowe():
    press_key = czcionka.render('Wcisnij klawisz zeby zagrac', True, NIEBIESKI)
    klawisz = press_key.get_rect()
    klawisz.topleft = (szerokosc/4, wysokosc - 30)
    mapa.blit(press_key, klawisz)


def gameover_screen():
    czcionka2 = pygame.font.Font('freesansbold.ttf', 120)
    game = czcionka2.render('Game', True, FIOLET)
    over = czcionka2.render('Over', True, FIOLET)
    game_pole = game.get_rect()
    over_pole = over.get_rect()
    game_pole.midtop = (szerokosc / 2, 10)
    over_pole.midtop = (szerokosc / 2, game_pole.height + 10 + 25)

    mapa.blit(game, game_pole)
    mapa.blit(over, over_pole)
    menu_poczatkowe()
    pygame.display.update()
    pygame.time.wait(500)
    SprawdzCzyKlawisz()


def SprawdzCzyKlawisz():
    if len(pygame.event.get(QUIT)) > 0:
        zatrzymanie_gry()

    klawisz_event = pygame.event.get(KEYUP)
    if len(klawisz_event) == 0:
        return None
    if klawisz_event[0].key == K_ESCAPE:
        zatrzymanie_gry()
    return klawisz_event[0].key


def zatrzymanie_gry():
    #pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


def siatka():
    for x in range(0, szerokosc, kratka): # linie pionowe
        pygame.draw.line(mapa, SZARY, (x, 0), (x, wysokosc))
    for y in range(0, wysokosc, kratka): # linie poziome
        pygame.draw.line(mapa, SZARY, (0, y), (szerokosc, y))


def losowanie_miejsca():
    return {'x': random.randint(0, szerokosc_pola - 1), 'y': random.randint(0, wysokosc_pola - 1)}


def drawjedzonko(wspolrzedne):
    x = wspolrzedne['x'] * kratka
    y = wspolrzedne['y'] * kratka
    kwadracik_jedzonka = pygame.Rect(x, y, kratka, kratka)
    pygame.draw.rect(mapa, CZERWONY, kwadracik_jedzonka)


def wonsz(snake_xy):
    for wspolrzedne in snake_xy:
        x = wspolrzedne['x'] * kratka
        y = wspolrzedne['y'] * kratka
        snake_body = pygame.Rect(x, y, kratka, kratka)
        pygame.draw.rect(mapa, CIEMNY_ZIELONY, snake_body)
        snake_body_inside = pygame.Rect(x + 4, y + 4, kratka - 8, kratka - 8)
        pygame.draw.rect(mapa, ZIELONY, snake_body_inside)

        snake_head = pygame.Rect(snake_xy[glowa]['x'] * kratka, snake_xy[glowa]['y'] * kratka, kratka, kratka)
        pygame.draw.rect(mapa, CIEMNY_ZIELONY, snake_head)
        snake_head_inside = pygame.Rect(snake_xy[glowa]['x'] * kratka + 4, snake_xy[glowa]['y'] * kratka + 4,
                                        kratka - 8, kratka - 8)
        pygame.draw.rect(mapa, ZIELONYHEAD, snake_head_inside)


def gora(wynik):
    wynik_napis = czcionka.render('WYNIK: %s' % (wynik), True, BIALY)
    wynik_pole = wynik_napis.get_rect()
    wynik_pole.topleft = (szerokosc - 100, 5)
    mapa.blit(wynik_napis, wynik_pole)


def pauza():
    czcionka2 = pygame.font.SysFont("Comic Sans MS", 50)
    pauza_key = czcionka2.render('PAUZA', True, ZOLTY)
    klawisz2 = pauza_key.get_rect()
    klawisz2.centerx = mapa.get_rect().centerx
    klawisz2.centery = mapa.get_rect().centery
    mapa.blit(pauza_key, klawisz2)


def odpalenie_gry():
    start_x = random.randint(5, szerokosc_pola - 6)
    start_y = random.randint(5, wysokosc_pola - 6)
    snake_xy = [{'x': start_x, 'y': start_y},
                {'x': start_x - 1, 'y': start_y},
                {'x': start_x - 2, 'y': start_y}]
    kierunek = RIGHT  # poczatkowy kierunek w ktorym porusza sie waz

    # Jedzenie w losowym miejscu przy uzyciu funkcji
    jedzonko = losowanie_miejsca()

    while True:  # glowna petla gry ktora w kolko sie wykonuje, kazdy ruch weza o kratke to sprawdzeine petli
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                zatrzymanie_gry()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and kierunek != RIGHT:
                    kierunek = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and kierunek != LEFT:
                    kierunek = RIGHT
                elif (event.key == K_UP or event.key == K_w) and kierunek != DOWN:
                    kierunek = UP
                elif (event.key == K_DOWN or event.key == K_s) and kierunek != UP:
                    kierunek = DOWN
                elif event.key == K_ESCAPE:
                    zatrzymanie_gry()
                if event.key == K_SPACE:
                    pauza()
                    while 1:
                        pauza()
                        pygame.display.update()
                        event = pygame.event.wait()
                        if event.type == QUIT:
                            zatrzymanie_gry()
                        if (event.type == KEYDOWN and event.key == K_ESCAPE):
                            zatrzymanie_gry()
                        if (event.type == KEYDOWN and event.key == K_SPACE):
                            break

        # sprawdzanie kolizji weza
        if snake_xy[glowa]['x'] == -1 or snake_xy[glowa]['x'] == szerokosc_pola or snake_xy[glowa]['y'] == -1 or \
                        snake_xy[glowa]['y'] == wysokosc_pola:
            return  # game over
        for snake_body in snake_xy[1:]:
            if snake_body['x'] == snake_xy[glowa]['x'] and snake_body['y'] == snake_xy[glowa]['y']:
                return  # game over

        # sprawdzamy czy waz zjadl jablko
        if snake_xy[glowa]['x'] == jedzonko['x'] and snake_xy[glowa]['y'] == jedzonko['y']:
            # jesli tak to nie usuwamy ostatniego elementu weza - ogonu
            #sound.play()
            jedzonko = losowanie_miejsca()  # ustawia nowe jablko gdzies
        else:
            del snake_xy[
                -1]  # usuwa ostatni element weza, gdyby tego nie bylo waz ze tak powiem ogon mialby w jednym miejscu i rozwijalby sie jak klebek nitki

        # przemieszczenie weza zgodnie z kierunkiem ktory wybralismy klawiszem
        if kierunek == UP:
            nowaglowa = {'x': snake_xy[glowa]['x'], 'y': snake_xy[glowa]['y'] - 1}
        elif kierunek == DOWN:
            nowaglowa = {'x': snake_xy[glowa]['x'], 'y': snake_xy[glowa]['y'] + 1}
        elif kierunek == LEFT:
            nowaglowa = {'x': snake_xy[glowa]['x'] - 1, 'y': snake_xy[glowa]['y']}
        elif kierunek == RIGHT:
            nowaglowa = {'x': snake_xy[glowa]['x'] + 1, 'y': snake_xy[glowa]['y']}
        snake_xy.insert(0, nowaglowa)
        mapa.fill(TLO_KOLOR)
        siatka()
        wonsz(snake_xy)
        drawjedzonko(jedzonko)
        gora(len(snake_xy) - 3)
        pygame.display.update()
        zegar_fps.tick(FPS)

main()