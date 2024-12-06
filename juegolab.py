import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 800
TAMAÑO_CELDA = 40
NEGRO = (0, 0, 0)
BLANCO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# Laberinto
laberinto = [
    "11111111111111111111",
    "1P000000000000000001",
    "10111101111101111101",
    "10000101000001000001",
    "11110101011111011101",
    "10010101010000010101",
    "10010101010111110101",
    "10010000010100000101",
    "10110111110101111101",
    "10000000000100000001",
    "10111110111111110101",
    "10000000100000000101",
    "10111111101111110101",
    "10000000001000000001",
    "10111111111111111101",
    "1000000000000000000s",
    "11111111111111111111"
]

# Cargar imágenes
img_personaje = pygame.image.load("img/vincent.png")
img_enemigo = pygame.image.load("img/enemigo.png")
img_moneda = pygame.image.load("img/moneda.png")

# Crear pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto de Moneditas")

# Variables de nivel
nivel_actual = 1
niveles_totales = 3
mostrar_dialogo_inicial = True
mostrar_dialogo_final = False

# Clases
class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(img_personaje, (TAMAÑO_CELDA, TAMAÑO_CELDA))
        self.rect = self.image.get_rect(topleft=(x, y))

    def mover(self, dx, dy):
        nueva_x = self.rect.x + dx
        nueva_y = self.rect.y + dy
        if self.puede_moverse(nueva_x, nueva_y):
            self.rect.x = nueva_x
            self.rect.y = nueva_y

    def puede_moverse(self, x, y):
        celda_x = x // TAMAÑO_CELDA
        celda_y = y // TAMAÑO_CELDA
        if 0 <= celda_x < len(laberinto[0]) and 0 <= celda_y < len(laberinto):
            return laberinto[celda_y][celda_x] in "0S"
        return False

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(img_enemigo, (TAMAÑO_CELDA, TAMAÑO_CELDA))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direccion = random.choice(["arriba", "abajo", "izquierda", "derecha"])
        self.tiempo_ultimo_movimiento = pygame.time.get_ticks()

    def mover(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_movimiento < 500:
            return

        self.tiempo_ultimo_movimiento = ahora
        x_anterior, y_anterior = self.rect.x, self.rect.y

        if self.direccion == "arriba":
            self.rect.y -= TAMAÑO_CELDA
        elif self.direccion == "abajo":
            self.rect.y += TAMAÑO_CELDA
        elif self.direccion == "izquierda":
            self.rect.x -= TAMAÑO_CELDA
        elif self.direccion == "derecha":
            self.rect.x += TAMAÑO_CELDA

        if not self.puede_moverse(self.rect.x, self.rect.y):
            self.rect.x, self.rect.y = x_anterior, y_anterior
            self.direccion = random.choice(["arriba", "abajo", "izquierda", "derecha"])

    def puede_moverse(self, x, y):
        celda_x = x // TAMAÑO_CELDA
        celda_y = y // TAMAÑO_CELDA
        if 0 <= celda_x < len(laberinto[0]) and 0 <= celda_y < len(laberinto):
            return laberinto[celda_y][celda_x] == "0"
        return False

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(img_moneda, (TAMAÑO_CELDA // 1.5, TAMAÑO_CELDA // 1.5))
        self.rect = self.image.get_rect(topleft=(x, y))

# Inicialización del juego
def reiniciar_juego():
    global personaje, enemigos, monedas, puntaje, mostrar_dialogo_inicial, nivel_actual
    todos_sprites.empty()
    enemigos.empty()
    monedas.empty()

    # Crear personaje
    for fila_idx, fila in enumerate(laberinto):
        for col_idx, celda in enumerate(fila):
            x = col_idx * TAMAÑO_CELDA
            y = fila_idx * TAMAÑO_CELDA
            if celda == "P":
                personaje = Personaje(x, y)
                todos_sprites.add(personaje)

    # Crear enemigos
    enemigos_posiciones = [(5, 1), (8, 5), (3, 4)]
    for pos in enemigos_posiciones:
        x, y = pos
        enemigo = Enemigo(x * TAMAÑO_CELDA, y * TAMAÑO_CELDA)
        enemigos.add(enemigo)
        todos_sprites.add(enemigo)

    # Crear monedas
    crear_monedas()

    # Resetear puntaje
    puntaje = 0
    mostrar_dialogo_inicial = True

def crear_monedas():
    while len(monedas) < 10:
        while True:
            col_idx = random.randint(1, len(laberinto[0]) - 2)
            fila_idx = random.randint(1, len(laberinto) - 2)
            if laberinto[fila_idx][col_idx] == "0":
                x = col_idx * TAMAÑO_CELDA + TAMAÑO_CELDA // 4
                y = fila_idx * TAMAÑO_CELDA + TAMAÑO_CELDA // 4
                moneda = Moneda(x, y)
                monedas.add(moneda)
                todos_sprites.add(moneda)
                break

# Inicialización de variables
todos_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
monedas = pygame.sprite.Group()
puntaje = 0

reiniciar_juego()

# Bucle principal
clock = pygame.time.Clock()
corriendo = True

while corriendo:
    pantalla.fill(NEGRO)

    # Mostrar diálogo inicial
    if mostrar_dialogo_inicial:
        fuente = pygame.font.SysFont("Arial", 30)
        texto_inicial = fuente.render(f"Nivel {nivel_actual}: ¡Recoge las monedas!", True, AMARILLO)
        pantalla.blit(texto_inicial, (200, 400))
        pygame.display.flip()
        pygame.time.delay(5000)
        mostrar_dialogo_inicial = False

    # Eventos del juego
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        personaje.mover(0, -TAMAÑO_CELDA)
    if teclas[pygame.K_s]:
        personaje.mover(0, TAMAÑO_CELDA)
    if teclas[pygame.K_a]:
        personaje.mover(-TAMAÑO_CELDA, 0)
    if teclas[pygame.K_d]:
        personaje.mover(TAMAÑO_CELDA, 0)

    # Mover enemigos
    for enemigo in enemigos:
        enemigo.mover()

    # Verificar colisiones con enemigos
    if pygame.sprite.spritecollideany(personaje, enemigos):
        fuente = pygame.font.SysFont("Arial", 40)
        texto_perdiste = fuente.render("¡Perdiste! Presiona 'R' para reiniciar.", True, ROJO)
        pantalla.blit(texto_perdiste, (200, 400))
        pygame.display.flip()
        pygame.time.delay(3000)
        reiniciar_juego()

    # Verificar si el jugador recoge una moneda
    monedas_colisionadas = pygame.sprite.spritecollide(personaje, monedas, True)
    if monedas_colisionadas:
        puntaje += len(monedas_colisionadas)

    # Dibujar laberinto
    for fila_idx, fila in enumerate(laberinto):
        for col_idx, celda in enumerate(fila):
            color = BLANCO if celda == "1" else AZUL if celda == "0" else AMARILLO
            pygame.draw.rect(pantalla, color, (col_idx * TAMAÑO_CELDA, fila_idx * TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA))

    # Mostrar puntaje
    fuente = pygame.font.SysFont("Arial", 30)
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    pantalla.blit(texto_puntaje, (10, 10))

    # Verificar si ganó el nivel
    if puntaje >= 10:
        if nivel_actual < niveles_totales:
            nivel_actual += 1
            reiniciar_juego()
        else:
            mostrar_dialogo_final = True
            break

    # Dibujar sprites
    todos_sprites.draw(pantalla)
    pygame.display.flip()
    clock.tick(30)

# Mostrar diálogo final
if mostrar_dialogo_final:
    pantalla.fill(NEGRO)
    fuente = pygame.font.SysFont("Arial", 40)
    texto_final = fuente.render("¡Felicidades! Completaste el juego.", True, VERDE)
    pantalla.blit(texto_final, (150, 400))
    pygame.display.flip()
    pygame.time.delay(5000)

# Cerrar pygame
pygame.quit()
sys.exit()
