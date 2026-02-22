import tkinter as tk
import math
import random
from PIL import Image, ImageTk



WIDTH = 800
HEIGHT = 600


# VENTANA


root = tk.Tk()
root.title("SkyRage")


asteroid_img = ImageTk.PhotoImage(Image.open("asteroid.png").resize((50,50)))
bullet_img = ImageTk.PhotoImage(Image.open("bullet.png").resize((10,10)))
logo_img = ImageTk.PhotoImage(Image.open("logo.png").resize((500, 150)))

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

score = 0
keys = set()
rankings = [0, 0, 0, 0, 0]

def change_state(state):
    global game_state
    game_state = state

# MENU

MENU = "menu"
GAME = "game"
RANKING = "ranking"
CONTROLS = "controls"
GAME_OVER= "game_over"

game_state = MENU

def start_game():
    global game_state
    reset_game()     # Reinicia jugador, asteroides y puntuación
    game_state = GAME


def show_ranking():
    global game_state
    game_state = RANKING

def show_controls():
    global game_state
    game_state = CONTROLS

buttons = [
    {"text": "JUGAR", "x1": 300, "y1": 300, "x2": 500, "y2": 350, "action": start_game},
    {"text": "RANKING", "x1": 300, "y1": 370, "x2": 500, "y2": 420, "action": lambda: change_state(RANKING)},
    {"text": "CONTROLES", "x1": 300, "y1": 440, "x2": 500, "y2": 490, "action": lambda: change_state(CONTROLS)}
]



def draw_menu():
    # Logo
    canvas.create_image(WIDTH/2, 150, image=logo_img)

    # Botones
    for b in buttons:
        canvas.create_rectangle(b["x1"], b["y1"], b["x2"], b["y2"], outline="white")
        canvas.create_text((b["x1"]+b["x2"])//2, (b["y1"]+b["y2"])//2,
                           text=b["text"], fill="white", font=("Arial", 20))



def draw_ranking():
    canvas.create_text(WIDTH//2, 100, text="MEJORES PUNTUACIONES", fill="white", font=("Arial",28))
    for i,s in enumerate(rankings):
        canvas.create_text(WIDTH//2, 180 + i*40, text=f"{i+1}. {s}", fill="white", font=("Arial",20))
    canvas.create_text(WIDTH//2, 520, text="Pulsa ESC para volver", fill="gray")

# Dibujar controles
def draw_controls():
    canvas.create_text(WIDTH//2, 150, text="CONTROLES", fill="white", font=("Arial",28))
    canvas.create_text(WIDTH//2, 260,
        text="W / ↑  → Acelerar\nA / ←  → Girar izquierda\nD / →  → Girar derecha\nESPACIO → Disparar",
        fill="white", font=("Arial",18), justify="center")
    canvas.create_text(WIDTH//2, 520, text="Pulsa ESC para volver", fill="gray")

def draw_game_over():
    canvas.create_text(WIDTH//2, 200, text="GAME OVER", fill="red", font=("Arial", 40, "bold"))
    canvas.create_text(WIDTH//2, 300, text=f"PUNTUACION FINAL: {score}", fill="white", font=("Arial", 25))
    canvas.create_text(WIDTH//2, 450, text="Pulsa ESC para el Menu", fill="gray", font=("Arial", 15))


# CLASES



class Player:
    def __init__(self):
        self.base_img = Image.open("player.png").resize((40,40))
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.angle = 0
        self.speed = 0
        self.size = 12
        self.vx = 0
        self.vy = 0


    def move(self):
        if "a" in keys or "Left" in keys:
            self.angle -= 5

        if "d" in keys or "Right" in keys:
            self.angle += 5

        if "w" in keys or "Up" in keys:
            rad = math.radians(self.angle)
            self.vx += math.cos(rad) * 0.15
            self.vy += math.sin(rad) * 0.15


    # friccion espacial
        self.vx *= 0.995
        self.vy *= 0.995

        self.x += self.vx
        self.y += self.vy

        self.x %= WIDTH
        self.y %= HEIGHT


    def draw(self):
        rotated_img = ImageTk.PhotoImage(self.base_img.rotate(-self.angle))
        self.sprite = rotated_img  # evitar que se borre
        return canvas.create_image(self.x, self.y, image=self.sprite)
    



class Bullet:
    def __init__(self,x,y,angle):
        self.x = x
        self.y = y
        self.dx = math.cos(angle)*10
        self.dy = math.sin(angle)*10
        self.life = 60

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

    def draw(self):
        return canvas.create_image(self.x, self.y, image=bullet_img)
    
    def shoot(e):
        bullets.append(
            Bullet(
                player.x,
                player.y,
                math.radians(player.angle)
            )
        )


class Asteroid:
    def __init__(self):
        self.x = random.randint(0,WIDTH)
        self.y = random.randint(0,HEIGHT)
        self.dx = random.uniform(-2,2)
        self.dy = random.uniform(-2,2)
        self.size = 25

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self):
        return canvas.create_image(self.x, self.y, image=asteroid_img)



# CREACIÓN


player = Player()
bullets = []
asteroids = [Asteroid() for _ in range(6)]


# CONTROLES


def key_down(e):
    keys.add(e.keysym)

def key_up(e):
    if e.keysym in keys:
        keys.remove(e.keysym)


def shoot(e):
    bullets.append(
        Bullet(player.x, player.y,
               math.radians(player.angle))
    )

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
root.bind("<KeyPress-space>", shoot)


# FUNCIONES


def distance(a,b,c,d):
    return math.sqrt((a-c)**2 + (b-d)**2)

def reset_game():
    global player, bullets, asteroids, score
    player = Player()
    bullets = []
    asteroids = [Asteroid() for _ in range(6)]
    score = 0

def save_score():
    global rankings
    rankings.append(score)
    rankings = sorted(rankings, reverse=True)[:5]

def mouse_click(e):
    global game_state
    if game_state == MENU:
        for b in buttons:
            if b["x1"] <= e.x <= b["x2"] and b["y1"] <= e.y <= b["y2"]:
                b["action"]()
                break


def esc_key(e):
    global game_state
    if game_state in (RANKING, CONTROLS, GAME_OVER):
        game_state = MENU


# BUCLE PRINCIPAL


def update():
    global score, game_state  # <-- IMPORTANTE
    canvas.delete("all")

    if game_state == MENU:
        draw_menu()
    elif game_state == RANKING:
        draw_ranking()
    elif game_state == CONTROLS:
        draw_controls()
    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == GAME:
        player.move()
        player.draw()

        for b in bullets[:]:
            b.move()
            if b.life <= 0:
                bullets.remove(b)
            else:
                b.draw()

        for a in asteroids:
            a.move()
            a.draw()

        
        # Colisión jugador
        for a in asteroids:
            if distance(player.x,player.y,a.x,a.y) < a.size:
                save_score()
                game_state = GAME_OVER
                break

        # Colisiones bala-asteroide
        for b in bullets[:]:
            for a in asteroids[:]:
                if distance(b.x,b.y,a.x,a.y) < a.size:
                    bullets.remove(b)
                    asteroids.remove(a)
                    asteroids.append(Asteroid())
                    score += 50
                    break


        canvas.create_text(80,20, text=f"Puntos: {score}", fill="white", font=("Arial",16))

    root.after(16, update)



root.bind("<Button-1>", mouse_click)
root.bind("<Escape>", esc_key)

update()
root.mainloop()
