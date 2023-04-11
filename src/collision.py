import pygame


class Collision:
    def __init__(self, target, objects: list):
        self.target = target
        self.objects = objects
        