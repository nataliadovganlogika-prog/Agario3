from socket import *
from pygame import *
from threading import Thread
from math import hypot

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("localhost", 8080))

# 👇 нік
my_name = input("Nick: ")
sock.send((my_name + "\n").encode())

# 👇 ПРАВИЛЬНО ЧИТАЄМО СТАРТ
data = sock.recv(64).decode().strip()
my_data = list(map(int, data.split(',')))

my_id = my_data[0]
my_player = my_data[1:]

sock.setblocking(False)

init()
win = display.set_mode((800, 800))
clock = time.Clock()
font = font.Font(None, 30)

players = []
lose = False
running = True


def recv():
    global players, lose

    while running:
        try:
            data = sock.recv(4096).decode().strip()

            if data == "LOSE":
                lose = True

            elif data:
                players = []

                for p in data.split('|'):
                    d = p.split(',')
                    if len(d) == 5:
                        players.append([
                            int(d[0]),
                            int(d[1]),
                            int(d[2]),
                            int(d[3]),
                            d[4]
                        ])
        except:
            pass


Thread(target=recv, daemon=True).start()


while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    win.fill((255, 255, 255))

    scale = max(0.3, min(50 / my_player[2], 1.5))

    for p in players:
        if p[0] == my_id:
            continue

        x = int((p[1] - my_player[0]) * scale + 400)
        y = int((p[2] - my_player[1]) * scale + 400)

        draw.circle(win, (0, 0, 0), (x, y), int(p[3] * scale))

        txt = font.render(p[4], True, (0, 0, 0))
        win.blit(txt, (x - txt.get_width() // 2, y - 25))

    draw.circle(win, (0, 0, 0), (400, 400), int(my_player[2] * scale))

    txt = font.render(my_name, True, (0, 0, 0))
    win.blit(txt, (400 - txt.get_width() // 2, 370))

    if lose:
        t = font.render("LOSE", True, (255, 0, 0))
        win.blit(t, (350, 400))

    display.update()
    clock.tick(60)

    keys = key.get_pressed()

    if keys[K_w]: my_player[1] -= 10
    if keys[K_s]: my_player[1] += 10
    if keys[K_a]: my_player[0] -= 10
    if keys[K_d]: my_player[0] += 10

    try:
        sock.send(f"{my_id},{my_player[0]},{my_player[1]},{my_player[2]}\n".encode())
    except:
        pass

sock.close()
quit()