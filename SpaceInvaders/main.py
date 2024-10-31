import pygame as pg
from engine.config import WND_SIZE, SIZE, FPS
from engine.tilemap import PhonePicture
from engine.text import Counter
from engine.colors import BLACK
from engine.player import SpaceShip
from engine.tools import SaveLoad
from engine.groups import BulletGroup, AlienGroup
from engine.enumerations import MousePressed
from engine.spawners import SpawnerAlien
from engine.monster import Alien
from engine.gui import Button, FNT_SIZE
from paths import ALIEN, SPACEBLOCK, SPACESHIP, FONT, RECORD, GAME, LASER


pg.init()
TITLE: str = 'SpaceInvaders'
WND: pg.Surface = pg.display.set_mode(WND_SIZE, pg.HWSURFACE)
ICON: pg.Surface = pg.image.load(ALIEN).convert_alpha()
pg.display.set_caption(TITLE)
pg.display.set_icon(ICON)
pg.mixer.music.load(GAME)
pg.mixer.music.set_volume(.1)


class Game:
    def __init__(self) -> None:

        # Common game objects
        self.clock: pg.time.Clock = pg.time.Clock()
        self.running: bool = True
        phone_pos: tuple[int, int] = 0, 0
        phone_image: pg.Surface = pg.image.load(SPACEBLOCK).convert_alpha()
        self.phone: PhonePicture = PhonePicture(phone_image, phone_pos)
        self.mus_started: bool = False

        # Game loop objects
        spaceship_sizes: tuple[int, int] = int(SIZE * 3.5), SIZE * 4
        spaceship_pos: tuple[int, int] = 0, WND_SIZE[1] - spaceship_sizes[1] - SIZE * 2
        spaceship_image: pg.Surface = pg.image.load(SPACESHIP).convert_alpha()
        self.spaceship: SpaceShip = SpaceShip(spaceship_image, spaceship_pos, spaceship_sizes, LASER)
        self.bullet_group: BulletGroup = BulletGroup()
        alien_image: pg.Surface = pg.image.load(ALIEN).convert_alpha()
        alien_sizes: tuple[int, int] = SIZE * 4, SIZE * 4
        self.alien_spawner: SpawnerAlien = SpawnerAlien(alien_image, alien_sizes)
        self.alien_group: AlienGroup = AlienGroup()
        self.score_counter: Counter = Counter(FONT)
        max_score: str = SaveLoad.load(RECORD)
        self.max_score: int = int(max_score)
        record_pos: tuple[int, int] = self.score_counter.pos[0] + self.score_counter.sizes[0] + SIZE * 11, self.score_counter.pos[1]
        self.record: Counter = Counter(FONT, text='Max score:', start_value=self.max_score, pos=record_pos)
        self.loaded: bool = False
        self.saved: bool = False

        # Dead loop objects
        fnt_size2: int = FNT_SIZE * 2
        text1: str = 'Restart'
        pos1: tuple[int, int] = SIZE  * 9, SIZE * 12
        self.button_restart: Button = Button(text1, FONT, pos1, fnt_size=fnt_size2)
        text2: str = 'Quit'
        pos2: tuple[int, int] = SIZE * 11, self.button_restart.pos[1] + SIZE * 4
        self.button_quit: Button = Button(text2, FONT, pos2, fnt_size=fnt_size2)

        # Init objects
        text3: str = 'Start'
        pos3: tuple[int, int] = SIZE * 10, SIZE * 12
        self.button_start: Button = Button(text3, FONT, pos3, fnt_size=fnt_size2)
        self.started: bool = False

        # Debug
        self.fps_list: list[float] = []

    def main(self) -> None:
        while self.running:
            WND.fill(BLACK)
            if self.spaceship.alive:
                self.game_loop()
            else:
                self.dead_loop()
            pg.display.flip()
            self.clock.tick(FPS)
            self.fps_list.append(self.clock.get_fps())
            self.event_loop()

    def game_loop(self) -> None:
        self.reload_score()
        self.phone.draw(WND)
        self.score_counter.draw(WND)
        self.record.draw(WND)
        self.bullet_group.draws(WND)
        self.spaceship.draw(WND)
        self.alien_group.draws(WND)
        if self.started:
            self.start_mus()
            self.saved = False
            self.spaceship.play(self.bullet_group)
            self.bullet_group.updates()
            self.global_interacts()
            self.record.change_value(self.max_score)
            self.alien_spawner.spawn(self.alien_group)
        else:
            self.init_loop()

    def start_mus(self) -> None:
        if not self.mus_started:
            pg.mixer.music.play(-1)
            self.mus_started = True

    def global_interacts(self) -> None:
        self.alien_group.updates()
        self.alien_group.kills_player(self.spaceship)
        if len(self.bullet_group) != 0:
            [self.alien_group.interacts(bullet) for bullet in self.bullet_group.group]
        if len(self.alien_group) != 0:
            deads: int = len([alien for alien in self.alien_group.group if not alien.alive])
            self.score_counter.change_value(deads)  

    def init_loop(self) -> None:
        self.button_start.draw(WND)
        self.button_start.update()
        if self.button_start.mouse == MousePressed.LEFT:
            self.started = True

    def dead_loop(self) -> None:
        pg.mixer.music.stop()
        self.mus_started = False
        self.button_restart.draw(WND)
        self.button_quit.draw(WND)
        self.button_restart.update()
        self.button_quit.update()
        if self.button_restart.mouse == MousePressed.LEFT:
            self.restart_game()
        if self.button_quit.mouse == MousePressed.LEFT:
            self.rewrite_score()
            self.running = False

    def restart_game(self) -> None:
        self.rewrite_score()
        self.loaded = False
        self.alien_group.group.clear()
        self.bullet_group.group.clear()
        Alien.back()
        self.score_counter.change_value(0)
        self.spaceship.alive = True

    def reload_score(self) -> None:
        if not self.loaded:
            score: str = SaveLoad.load(RECORD)
            self.max_score = int(score)
            self.loaded = True

    def rewrite_score(self) -> None:
        if not self.saved:
            score: int = len([alien for alien in self.alien_group.group if not alien.alive])
            if score > self.max_score:
                SaveLoad.save(RECORD, score)
            self.saved = True

    def event_loop(self) -> None:
        if not self.running:
            avg_fps: float = sum(self.fps_list) / len(self.fps_list)
            print(f'{avg_fps=}')
            pg.mixer.music.stop()
            pg.quit()
            return
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
            else:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        pg.quit()


if __name__ == '__main__':
    game: Game = Game()
    game.main()
