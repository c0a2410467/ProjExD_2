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

def check_bound(rct:pg.Rect):
    
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def game_over_screen(screen: pg.Surface):
    black_out = pg.Surface((1100,650))
    black_out.set_alpha(200)  
    black_out.fill((0, 0, 0)) 
    screen.blit(black_out, (0, 0))

    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1)
    left_rect = cry_img.get_rect(center=(350, 325))
    right_rect = cry_img.get_rect(center=(750, 325))
    screen.blit(cry_img, left_rect)
    screen.blit(cry_img, right_rect)

    font = pg.font.Font(None, 80)
    text_surf = font.render("Game Over", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(550, 325))
    screen.blit(text_surf, text_rect)

    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  
    bb_img.set_colorkey((0, 0, 0))  
    bb_rct = bb_img.get_rect() 
    bb_rct.centerx = random.randint(0, WIDTH)  
    bb_rct.centery = random.randint(0, HEIGHT)  
    vx, vy = +5, +5  
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("gemeover")
            game_over_screen(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  
        yoko, tate = check_bound(bb_rct)
        if not yoko:  
            vx *= -1
        if not tate:  
            vy *= -1
        screen.blit(bb_img, bb_rct) 
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()