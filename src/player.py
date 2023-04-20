import pathlib
import pygame
from .settings import *
from .support import *
from .timer_action import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups: pygame.sprite.Group, surf: pygame.Surface) -> None:
        super().__init__(groups)
        self.surf = surf

        self.detector = None

        # animation
        self.animations = {}
        self.import_assets()
        self.status = "idle"
        self.frame_index = 0

        # general setup
        # self.image = pygame.Surface((32, 64))
        # self.image.fill("green")
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # timers
        self.timers = {
            "tool_use": Timer(350, self.use_tool),
            "attack": Timer(350, self.attack),
        }

        # weapon
        self.weapon = {"sword": ["air_attack1",
                                "air_attack2", 
                                "air_attack3",
                                "attack1",
                                "attack2",
                                "attack3",],
                        "bow": ["bow",
                                "bow_jump",],
                      }
        self.selected_weapon = "sword"

        # tools
        self.selected_tool = "items"

        # attacking
        self.attacking = False
        self.K_z = 0
        self.K_x = 0
        self.K_c = 0
        self.K_SPACE = 1
        self.commands = [self.K_z]

        # enemy
        self.enemy = None
    
    def check_enemy(self):
        # if self.enemy is not None:
        #     if self.enemy.player.attacking:
        #         print("o inimigo sabe q estou atacando.")
        pass
    
    def track_colision(self):
        pygame.draw.rect(self.surf, "red", self.rect, 1)
        mask = pygame.mask.from_surface(self.image)
        mask_outline = mask.outline()
        n = 0
        for point in mask_outline:
            mask_outline[n] = (point[0] + self.rect.x, point[1] + self.rect.y)
            n += 1
        pygame.draw.polygon(self.surf, "green", mask_outline, 1)

    def use_tool(self):
        # print(self.selected_tool)
        pass
    
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
    
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def attack(self):
        # self.status = "attack3"
        pass

    def input(self):
        keys = pygame.key.get_pressed()

        # change weapon
        if self.detector is not None:
            # if keys[pygame.K_1]:
            if (self.detector[3] == 1) and (self.detector[4] == 1):
                self.selected_weapon = "sword"
            # elif keys[pygame.K_2]:
            if (self.detector[0] == 1) and (self.detector[4] == 1):
                self.selected_weapon = "bow"

        if not self.timers["tool_use"].active:
            # directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "ladder_climb"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "crouch"
            else:
                self.direction.y = 0

            if self.detector is not None:
                # if keys[pygame.K_RIGHT]:
                if self.detector[1] == 1:
                    self.direction.x = 1
                    self.status = "run"
                # elif keys[pygame.K_LEFT]:
                elif self.detector[2] == 1:
                    self.direction.x = -1
                    self.status = "run_flip"
                else:
                    self.direction.x = 0
        
            # tool use
            if keys[pygame.K_t]:
                self.timers["tool_use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

        if not self.timers["attack"].active:
        # attack
            if self.detector is not None:

            # if keys[pygame.K_SPACE]:
                if self.detector[0] == 1:
                    self.attacking = True
                    self.timers["attack"].activate()
                    # self.status = "attack3"
                    self.frame_index += 1
                else:
                    self.attacking = False

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            if not self.status.startswith("idle") and not self.status.endswith("idle"):
                if "flip" in self.status:
                    self.status = "idle_flip"
                else:
                    self.status = "idle"
        # tool use
        if self.timers["tool_use"].active:
            self.status = self.selected_tool
        
        # attack
        if self.timers["attack"].active:
            if self.status.endswith("flip"):
                self.status = f"{self.weapon[self.selected_weapon][-1]}_flip"
            else:
                self.status = self.weapon[self.selected_weapon][-1]
        
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

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
        self.check_enemy()

        self.input()
        self.get_status()
        self.update_timers()

        self.move(dt)
        self.animate(dt)
        self.track_colision()