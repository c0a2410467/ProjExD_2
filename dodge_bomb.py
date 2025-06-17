import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect):
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def game_over_screen(screen: pg.Surface):
    black_out = pg.Surface((1100, 650))
    black_out.set_alpha(200)
    black_out.fill((0, 0, 0))
    screen.blit(black_out, (0, 0))

    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1)
    screen.blit(cry_img, cry_img.get_rect(center=(350, 325)))
    screen.blit(cry_img, cry_img.get_rect(center=(750, 325)))

    font = pg.font.Font(None, 80)
    text_surf = font.render("Game Over", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(550, 325))
    screen.blit(text_surf, text_rect)

    pg.display.update()
    time.sleep(5)

def bomb():
    bb_accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_accs, bb_imgs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bb_accs, bb_imgs = bomb()

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect(center=(300, 200))

    vx, vy = +5, +5
    bb_rct = pg.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 20, 20)

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        
        avx = vx * bb_accs[ min(tmr // 500, 9)]
        avy = vy * bb_accs[ min(tmr // 500, 9)]
        bb_img = bb_imgs[ min(tmr // 500, 9)]

        old_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = old_center
        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        if kk_rct.colliderect(bb_rct):
            game_over_screen(screen)
            return

        # 描画
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
