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
    """
    ゲームオーバー画面を表示する。

    画面を暗くし、「Game Over」の文字と画像を表示して5秒間停止する。
    """
    black_out = pg.Surface((WIDTH, HEIGHT))
    black_out.set_alpha(200)
    black_out.fill((0, 0, 0))
    screen.blit(black_out, (0, 0))

    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1)
    screen.blit(cry_img, cry_img.get_rect(center=(350, 325)))
    screen.blit(cry_img, cry_img.get_rect(center=(750, 325)))

    font = pg.font.Font(None, 80)
    text_surf = font.render("Game Over", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
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

def load_kk_images():
    """
    各方向に回転させた画像を辞書でかえします。
    「fig/3.png」を読み込み、移動方向に応じて回転させた画像を作成し、
    (dx, dy) をキー、回転画像を値とする辞書を返す。
    """
    kk_base_img = pg.image.load("fig/3.png")
    img_l = pg.transform.rotozoom(kk_base_img, 90, 1)       
    img_lu = pg.transform.rotozoom(kk_base_img, -45, 1)     
    img_ld = pg.transform.rotozoom(kk_base_img, 45, 1)      
    img_u = pg.transform.rotozoom(kk_base_img, 0, 1)        
    img_d = pg.transform.rotozoom(kk_base_img, 180, 1)     

    kk_imgs = {
        (-5, 0): img_l,                                    
        (5, 0): pg.transform.flip(img_l, True, False),      

        (-5, -5): img_lu,                                   
        (5, -5): pg.transform.flip(img_lu, True, False),    

        (-5, 5): img_ld,                                  
        (5, 5): pg.transform.flip(img_ld, True, False),     

        (0, -5): img_u,                                     
        (0, 5): img_d,                                      

        (0, 0): img_u,
    }
    return kk_imgs

def get_kk_img(mv: tuple[int, int], kk_imgs: dict) -> pg.Surface:
    return kk_imgs.get(mv, kk_imgs[(0, 0)])

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bb_accs, bb_imgs = bomb()
    kk_imgs = load_kk_images()
    kk_img = kk_imgs[(5, 0)]  # 初期画像
    kk_rct = kk_img.get_rect(center=(300, 200))

    vx, vy = +5, +5
    bb_rct = pg.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 20, 20)

    clock = pg.time.Clock()
    tmr = 0
    last_mv = (5, 0)  # 最初は右向き

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 爆弾の加速度と画像
        stage = min(tmr // 500, 9)
        avx = vx * bb_accs[stage]
        avy = vy * bb_accs[stage]
        bb_img = bb_imgs[stage]

        # 爆弾の移動と跳ね返り
        old_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = old_center
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            game_over_screen(screen)
            return

        # 背景描画
        screen.blit(bg_img, [0, 0])

        # こうかとんの操作
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        if sum_mv != [0, 0]:
            last_mv = tuple(sum_mv)

        kk_img = get_kk_img(last_mv, kk_imgs)
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # 爆弾の描画
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
