import pathlib
import pygame
from support import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group: pygame.sprite.Group, surf: pygame.Surface):
        super().__init__(group)
        self.surf = surf

        # animation
        self.animations = {}
        self.import_assets()
        self.status = "idle"
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.player = None


    def import_assets(self):
        _animations = {"idle": {"flip": True, "frames": []},
                       "run": {"flip": True, "frames": []},
                       "die": {"flip": True, "frames": []},
                       "crouch": {"flip": True, "frames": []},
                       "ladder_climb": {"flip": True, "frames": []},
                       "bow": {"flip": True, "frames": []},
                       "items": {"flip": True, "frames": []},
                       "air_attack1": {"flip": True, "frames": []},
                       "air_attack2": {"flip": True, "frames": []},
                       "air_attack3": {"flip": True, "frames": []},
                       "attack1": {"flip": True, "frames": []},
                       "attack2": {"flip": True, "frames": []},
                       "attack3": {"flip": True, "frames": []},
                       "bow": {"flip": True, "frames": []},
                       "bow_jump": {"flip": True, "frames": []},
                       }

        for animation, value in _animations.items():
            full_path = pathlib.Path("assets/character/Individual Sprites", animation)
            self.animations[animation] = import_folder(full_path)
            if value["flip"] == True:
                self.animations[f"{animation}_flip"] = []
                for frame in self.animations[animation]:
                    self.animations[f"{animation}_flip"].append(pygame.transform.flip(frame, True, False))
    
    def check_player(self):
        if self.player.attacking:
            self.player.enemy = self
            print("O player estar atacando")
        # else:
        #     self.player.attacking = False

    def track_colision(self):
        pygame.draw.rect(self.surf, "red", self.rect, 1)
        mask = pygame.mask.from_surface(self.image)
        mask_outline = mask.outline()
        n = 0
        for point in mask_outline:
            mask_outline[n] = (point[0] + self.rect.x, point[1] + self.rect.y)
            n += 1
        pygame.draw.polygon(self.surf, "green", mask_outline, 1)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.check_player()

        # self.input()
        # self.get_status()
        # self.update_timers()

        # self.move(dt)
        self.animate(dt)
        self.track_colision()