import pygame, math, random, sys, re
from pygame.locals import *  # お呪い　不要？

GAME_MODE = {'START': 0, 'PLAY': 1, 'GAMEOVER': 2}
# BARRIER_MODE = {'RED': 0, 'GREEN': 1, 'YELLOW': 2}
SCR_RECT = Rect(0, 0, 576, 768)  # スクリーンサイズ


class Game:
    enemy_prob = 60

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("AreaGuard")
        self.load_images()
        self.init_game()
        clock = pygame.time.Clock()
        while 1:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self):
        self.game_state = GAME_MODE['START']
        # self.barrier_color = BARRIER_MODE['GREEN']
        self.all_sprite = pygame.sprite.RenderUpdates()
        # self.barrier = pygame.sprite.Group()
        self.pc = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.razers = pygame.sprite.Group()
        # Barrier.containers = self.all_sprite, self.barrier
        Player.containers = self.all_sprite, self.pc
        Enemy.containers = self.all_sprite, self.enemies
        Razer.containers = self.all_sprite, self.razers
        #self.barrier = Barrier()
        self.player = Player()
        self.score = 0

    def update(self):
        if self.game_state == GAME_MODE['PLAY']:
            if not random.randrange(self.enemy_prob):
                Enemy()
            self.all_sprite.update()
            self.collision_detection()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.game_state == GAME_MODE['START']:
            # タイトル画面描画
            title_font = pygame.font.SysFont(None, 80)
            title = title_font.render('AreaGuard', False, (255, 0, 128))
            screen.blit(title, ((SCR_RECT.width - title.get_width()) / 2, 200))
            # エネミーのみ描画
            enemy_image = Enemy.image
            screen.blit(enemy_image, ((SCR_RECT.width - enemy_image.get_width()) / 2, 300))
            # PUSH SPACE KEYを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255, 255, 255))
            screen.blit(push_space, ((SCR_RECT.width - push_space.get_width()) / 2, 400))

        if self.game_state == GAME_MODE['PLAY']:
            # ゲームプレイ
            self.all_sprite.draw(screen)
            # 得点表示
            score_font = pygame.font.SysFont(None, 80)
            score = score_font.render("{0:0>4d}".format(self.score), False, (255, 255, 255))
            screen.blit(score, (SCR_RECT.left, SCR_RECT.top))

        if self.game_state == GAME_MODE['GAMEOVER']:
            # GAME OVERを描画
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("GAME OVER", False, (255, 0, 0))
            screen.blit(gameover, ((SCR_RECT.width - gameover.get_width()) / 2,
                                   (SCR_RECT.height - gameover.get_height()) / 4))
            # PUSH STARTを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255, 255, 255))
            screen.blit(push_space, ((SCR_RECT.width - push_space.get_width()) / 2,
                                     (SCR_RECT.height - push_space.get_height()) * 3 / 4))
            # 得点表示
            score_font = pygame.font.SysFont(None, 60)
            score = score_font.render("You killed {0:0>4d} enemies!".format(self.score), False, (255, 255, 255))
            screen.blit(score, ((SCR_RECT.width - score.get_width()) / 2,
                                (SCR_RECT.height - score.get_height()) / 2))

    def collision_detection(self):
        player_collided = pygame.sprite.groupcollide(self.enemies, self.pc, True, True)
        for enemy in player_collided.keys():
            self.game_state = GAME_MODE["GAMEOVER"]

        razer_collided = pygame.sprite.groupcollide(self.enemies, self.razers, True, True)
        for razer in razer_collided.keys():
            self.score += 1

        """barrier_collided = pygame.sprite.groupcollide(self.enemies, self.barrier, True, True)
        for barrier in barrier_collided.keys():
            if self.barrier_color == BARRIER_MODE['GREEN']:
                self.barrier_color = BARRIER_MODE['YELLOW']
            if self.barrier_color == BARRIER_MODE['YELLOW']:
                self.barrier_color = BARRIER_MODE['RED']
            if self.barrier_color == BARRIER_MODE['RED']:
                self.game_state = GAME_MODE['GAMEOVER']"""

    def load_images(self):
        # スプライトの画像を登録
        Player.image = load_image("pc_img.png")
        Enemy.image = load_image("enemy_img.png")
        Razer.image = load_image("razer_img.png")

    # Barrier.image = load_image("barrier_green.png")


    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.game_state == GAME_MODE['START']:  # スタート画面でスペースキーを押したらスタート
                    self.game_state = GAME_MODE['PLAY']
                elif self.game_state == GAME_MODE['GAMEOVER']:  # ゲームオーバー
                    self.init_game()  # ゲームを初期化して再開
                    self.game_state = GAME_MODE['PLAY']


class Player(pygame.sprite.Sprite):
    speed = 4  # 移動速度
    charge = 15  # レーザーがチャージされるまでの時間

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom  # プレイヤーは画面の一番下からスタート
        self.rect.left = (SCR_RECT.width - self.rect.width) / 2
        self.charge_timer = 0

    def update(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        # 画面からはみ出さないようにする
        self.rect = self.rect.clamp(SCR_RECT)

        if pressed_key[K_SPACE]:
            # 連射時リロード時間が0になるまで発射できない。
            if self.charge_timer > 0:
                # リロード中
                self.charge_timer -= 1
            else:
                # 発射！
                Razer(self.rect.center, self.rect.top)  # 作成すると同時にall_spriteに追加される。
                self.charge_timer = self.charge
        else:  # 連射終了、リロード
            self.charge_timer = 0


"""class Barrier(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.left = SCR_RECT.left
        self.rect.bottom = SCR_RECT.bottom


    def update(self):
        if Game.barrier_color == BARRIER_MODE['YELLOW']:
            self.image = load_image("barrier_yellow.png")
        if Game.barrier_color == BARRIER_MODE['RED']:
            self.image = load_image("barrier_red.png")"""

class Enemy(pygame.sprite.Sprite):
    speed = 3  # 移動速度

    def __init__(self):
        """
        初期化処理

        .. note::
          敵は上からランダムに出てきます。
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(SCR_RECT.width / self.rect.width) * self.rect.width
        self.rect.bottom = SCR_RECT.top

    def update(self):  # 速度設定
        mov_vec = [(0, self.speed), (0, self.speed + 1), (0, self.speed + 2), (0, self.speed - 1), (0, self.speed - 2)]
        self.rect.move_ip(random.choice(mov_vec))


class Razer(pygame.sprite.Sprite):
    speed = 9  # レーザーの移動速度

    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos_x
        self.rect.bottom = pos_y

    def update(self):
        self.rect.move_ip(0, -self.speed)  # 上へ移動
        if self.rect.top < 0:  # 上辺に達したら削除
            self.kill()


def load_image(filename, colorkey=None):
    # 画像ファイルがpngかgifか判定するための正規表現
    filecase = re.compile(r'[a-zA-Z0-9_/]+\.png|[a-zA-Z0-9_/]+\.gif')

    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image: " + filename)
        raise SystemExit(message)

    # 画像の拡張子によって処理を振り分け
    is_match = filecase.match(filename)
    if is_match:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


if __name__ == '__main__':
    Game()
