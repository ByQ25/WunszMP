import sys, random, pygame, socket, pickle
from pygame.locals import *


# Data Transfer Object
class DTO(object):
    def __int__(self, action: int, snakes: list):
        self.action = action
        self.snakes = snakes


# Main game object:
class WunszGame(object):
    # kolory RGB do zmiennych
    BIALY = (255, 255, 255)
    CZARNY = (0, 0, 0)
    NIEBIESKI = (0, 0, 255)
    CZERWONY = (220, 0, 0)
    FIOLET = (147, 112, 219)
    S_ZIELONY = (0, 200, 0)
    S_ZIELONYHEAD = (0, 255, 0)
    S_CIEMNY_ZIELONY = (0, 150, 0)
    ZOLTY = (255, 255, 0)
    SZARY = (30, 30, 30)
    TLO_KOLOR = CZARNY
    snakes = []

    class Snake(object):
        def __init__(self, nr, start_x, start_y):
            if nr == 0:
                # Orange snake (innerbody, innerhead, outerbody:
                self.kolor = ((251, 136, 0), (255, 168, 0), (217, 117, 0))
            elif nr == 1:
                # Blue snake:
                self.kolor = ((0, 80, 232), (0, 100, 255), (0, 66, 217))
            elif nr == 2:
                # Green snake:
                self.kolor = ((0, 200, 0), (0, 255, 0), (0, 150, 0))
            elif nr == 3:
                # Yellow snake:
                self.kolor = ((255, 215, 0), (255, 255, 0), (163, 161, 49))
            else:
                raise Exception("Snake number out of bounds.")
            self.kierunek = 2  # RIGHT
            self.snake_xy = [{'x': start_x, 'y': start_y}, {'x': start_x - 1, 'y': start_y}, {'x': start_x - 2, 'y': start_y}]

    class Player(object):
        def __init__(self, conn_socket, is_alive, snake):
            self.conn_socket = conn_socket
            self.is_alive = is_alive
            self.snake = snake

    def __init__(self, fps=10, width=768, height=768, squaresize=16):
        self.__FPS = fps  # im wiecej tym szybciej porusza sie waz
        self.__szerokosc = width
        self.__wysokosc = height
        self.__kratka = squaresize  # szerokosc jednej kratki
        self.__szerokosc_pola = int(width / squaresize)
        self.__wysokosc_pola = int(height / squaresize)
        # Inicjalizacja PyGame:
        pygame.init()
        # Ogólne:
        self.__zegar_fps = pygame.time.Clock()
        self.__mapa = pygame.display.set_mode((width, height))
        self.__czcionka = pygame.font.SysFont("Comic Sans MS", 18)
        self.__sound = pygame.mixer.Sound('materials\\Ding.wav')  # dzwiek zjadanego jablka
        # Kierunki:
        self.__LEFT = 0
        self.__UP = 1
        self.__RIGHT = 2
        self.__DOWN = 3
        pygame.display.set_caption('WunszMP')

    def start_game(self):
        pygame.mixer.music.load('materials\\Raw.mp3')  # muzyka w tle
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, 0.0)  # -1 - zapetlanie piosenki, 0 - moment od ktorego jest odtwarzana
        self.__ekran_startowy()
        # while True:
        # self.__odpalenie_gry()
        # self.__gameover_screen()

    def __ekran_startowy(self):
        czcionka_start = pygame.font.Font('freesansbold.ttf', 100)
        start_powierzchnia = czcionka_start.render('SNAKE!', True, self.BIALY)
        kat = 10
        pygame.event.pump()
        self.__mapa.fill(self.TLO_KOLOR)
        obrocony_napis = pygame.transform.rotate(start_powierzchnia, kat)
        obrocone_pole = obrocony_napis.get_rect()
        obrocone_pole.center = (self.__szerokosc / 2, self.__wysokosc / 2)
        self.__mapa.blit(obrocony_napis, obrocone_pole)
        self.__menu_poczatkowe()
        pygame.display.update()
        # Waiting for the user to press a key:
        while True:
            klawisz = self.__sprawdz_czy_klawisz()
            if klawisz == K_F1:
                self.__uruchom_serwer()
            elif klawisz == K_F2:
                self.__uruchom_klienta()
            elif klawisz:
                while True:
                    self.__odpalenie_gry()
                    self.__gameover_screen()

    def __uruchom_serwer(self):
        pass

    def __uruchom_klienta(self):
        pass

    def __menu_poczatkowe(self):
        press_key = self.__czcionka.render('Wcisnij klawisz zeby zagrac', True, self.NIEBIESKI)
        klawisz = press_key.get_rect()
        klawisz.topleft = (self.__szerokosc/3, self.__wysokosc - 30)
        self.__mapa.blit(press_key, klawisz)

    def __gameover_screen(self):
        czcionka2 = pygame.font.Font('freesansbold.ttf', 120)
        game = czcionka2.render('Game', True, self.FIOLET)
        over = czcionka2.render('Over', True, self.FIOLET)
        game_pole = game.get_rect()
        over_pole = over.get_rect()
        game_pole.midtop = (self.__szerokosc / 2, 10)
        over_pole.midtop = (self.__szerokosc / 2, game_pole.height + 10 + 25)

        self.__mapa.blit(game, game_pole)
        self.__mapa.blit(over, over_pole)
        self.__menu_poczatkowe()
        pygame.display.update()
        pygame.time.wait(500)
        self.__sprawdz_czy_klawisz()

    def __sprawdz_czy_klawisz(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.__zatrzymanie_gry()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.__zatrzymanie_gry()
                else:
                    return event.key
            return None

    @staticmethod
    def __zatrzymanie_gry():
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()

    def __siatka(self):
        for x in range(0, self.__szerokosc, self.__kratka):  # linie pionowe
            pygame.draw.line(self.__mapa, self.SZARY, (x, 0), (x, self.__wysokosc))
        for y in range(0, self.__wysokosc, self.__kratka):  # linie poziome
            pygame.draw.line(self.__mapa, self.SZARY, (0, y), (self.__szerokosc, y))

    def __losowanie_miejsca(self):
        while True:  # Losuje dopoki nie znajdzie wolnego miejsca.
            point = {'x': random.randint(0, self.__szerokosc_pola - 1), 'y': random.randint(0, self.__wysokosc_pola - 1)}
            free = True
            for s in self.snakes:
                for xy in s.snake_xy:
                    if xy['x'] == point['x'] and xy['y'] == point['y']:
                        free = False
                        break
                if not free:
                    break
            if free:
                return point

    def __drawjedzonko(self, wspolrzedne):
        x = wspolrzedne['x'] * self.__kratka
        y = wspolrzedne['y'] * self.__kratka
        kwadracik_jedzonka = pygame.Rect(x, y, self.__kratka, self.__kratka)
        pygame.draw.rect(self.__mapa, self.CZERWONY, kwadracik_jedzonka)

    # Drawing snake:
    def __wonsz(self, snake):
        snake_xy = snake.snake_xy
        kolor = snake.kolor
        for wspolrzedne in snake_xy:
            x = wspolrzedne['x'] * self.__kratka
            y = wspolrzedne['y'] * self.__kratka
            snake_body = pygame.Rect(x, y, self.__kratka, self.__kratka)
            pygame.draw.rect(self.__mapa, kolor[2], snake_body)
            snake_body_inside = pygame.Rect(x + 4, y + 4, self.__kratka - 8, self.__kratka - 8)
            pygame.draw.rect(self.__mapa, kolor[0], snake_body_inside)
            snake_head = pygame.Rect(snake_xy[0]['x'] * self.__kratka,
                                     snake_xy[0]['y'] * self.__kratka,
                                     self.__kratka, self.__kratka)
            pygame.draw.rect(self.__mapa, kolor[2], snake_head)
            snake_head_inside = pygame.Rect(snake_xy[0]['x'] * self.__kratka + 4,
                                            snake_xy[0]['y'] * self.__kratka + 4,
                                            self.__kratka - 8, self.__kratka - 8)
            pygame.draw.rect(self.__mapa, kolor[1], snake_head_inside)

    def __gora(self, wynik):
        wynik_napis = self.__czcionka.render('WYNIK: %s' % wynik, True, self.BIALY)
        wynik_pole = wynik_napis.get_rect()
        wynik_pole.topleft = (self.__szerokosc - 100, 5)
        self.__mapa.blit(wynik_napis, wynik_pole)

    def __pauza(self):
        czcionka2 = pygame.font.SysFont("Comic Sans MS", 50)
        pauza_key = czcionka2.render('PAUZA', True, self.ZOLTY)
        klawisz2 = pauza_key.get_rect()
        klawisz2.centerx = self.__mapa.get_rect().centerx
        klawisz2.centery = self.__mapa.get_rect().centery
        self.__mapa.blit(pauza_key, klawisz2)

    def __odpalenie_gry(self):
        # Losowanie pozycji weza do singla:
        # start_x = random.randint(5, self.__szerokosc_pola - 6)
        # start_y = random.randint(5, self.__wysokosc_pola - 6)

        self.snakes.append(self.Snake(0, 3, 1))
        self.snakes.append(self.Snake(1, 3, 4))
        self.snakes.append(self.Snake(2, 3, 7))
        self.snakes.append(self.Snake(3, 3, 10))
        kierunek = self.__RIGHT  # poczatkowy kierunek w ktorym porusza sie waz

        # Jedzenie w losowym miejscu przy uzyciu funkcji
        self.__jedzonko = self.__losowanie_miejsca()

        while True:  # glowna petla gry, ktora w kolko sie wykonuje, kazdy ruch weza o kratke to sprawdzeine petli
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    self.__zatrzymanie_gry()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and kierunek != self.__RIGHT:
                        kierunek = self.__LEFT
                    elif (event.key == K_RIGHT or event.key == K_d) and kierunek != self.__LEFT:
                        kierunek = self.__RIGHT
                    elif (event.key == K_UP or event.key == K_w) and kierunek != self.__DOWN:
                        kierunek = self.__UP
                    elif (event.key == K_DOWN or event.key == K_s) and kierunek != self.__UP:
                        kierunek = self.__DOWN
                    elif event.key == K_ESCAPE:
                        self.__zatrzymanie_gry()
                    if event.key == K_SPACE:
                        self.__pauza()
                        while 1:
                            self.__pauza()
                            pygame.display.update()
                            event = pygame.event.wait()  # Program'll be put to sleep by the OS, until events occure.
                            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                                self.__zatrzymanie_gry()
                            if event.type == KEYDOWN and event.key == K_SPACE:
                                break

            self.__mapa.fill(self.TLO_KOLOR)
            self.__siatka()
            apple_eaten = False
            for s in self.snakes:
                s.kierunek = kierunek
                if self.__check_collisions(s):
                    return
                if not apple_eaten:
                    if self.__check_apple(s):
                        self.__sound.play()
                self.__move_head(s)
                self.__wonsz(s)  # Drawing snake.
            self.__drawjedzonko(self.__jedzonko)
            self.__gora(len(self.snakes[0].snake_xy) - 3)
            pygame.display.update()
            self.__zegar_fps.tick(self.__FPS)

    def __check_collisions(self, snake) -> bool:
        snake_xy = snake.snake_xy
        # sprawdzanie kolizji weza (borders):
        if (snake_xy[0]['x'] == -1
            or snake_xy[0]['x'] == self.__szerokosc_pola
            or snake_xy[0]['y'] == -1
            or snake_xy[0]['y'] == self.__wysokosc_pola):
            return True  # game over

        # sprawdzanie kolizji weza (with itself):
        for snake_body in snake_xy[1:]:
            if snake_body['x'] == snake_xy[0]['x'] and snake_body['y'] == snake_xy[0]['y']:
                return True  # game over

    def __check_apple(self, snake) -> bool:
        # sprawdzamy czy waz zjadl jablko
        snake_xy = snake.snake_xy
        if snake_xy[0]['x'] == self.__jedzonko['x'] and snake_xy[0]['y'] == self.__jedzonko['y']:
            # jesli tak to nie usuwamy ostatniego elementu weza - ogona

            self.__jedzonko = self.__losowanie_miejsca()  # ustawia nowe jablko gdzies
            return True
        else:
            del snake.snake_xy[-1]  # usuwa ostatni element weza
            return False

    def __move_head(self, snake):
        snake_xy = snake.snake_xy
        kierunek = snake.kierunek
        # przemieszczenie weza zgodnie z kierunkiem ktory wybralismy klawiszem
        if kierunek == self.__UP:
            nowaglowa = {'x': snake_xy[0]['x'], 'y': snake_xy[0]['y'] - 1}
        elif kierunek == self.__DOWN:
            nowaglowa = {'x': snake_xy[0]['x'], 'y': snake_xy[0]['y'] + 1}
        elif kierunek == self.__LEFT:
            nowaglowa = {'x': snake_xy[0]['x'] - 1, 'y': snake_xy[0]['y']}
        elif kierunek == self.__RIGHT:
            nowaglowa = {'x': snake_xy[0]['x'] + 1, 'y': snake_xy[0]['y']}
        else:
            raise Exception("Niezdefiniowany kierunek poruszania się")
        snake.snake_xy.insert(0, nowaglowa)

if __name__ == "__main__":
    WunszGame().start_game()
