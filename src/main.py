import pygame
from .settings import *
from .level import Level

import cv2
from cvzone.HandTrackingModule import HandDetector


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
        pygame.display.set_caption("Jam")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level()

        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.img_show = True

    def run(self):
        fingers1 = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Get image frame
            success, img = self.cap.read()
            # Find the hand and its landmarks
            hands, img = self.detector.findHands(img)  # with draw
            if hands:
                hand1 = hands[0]
                fingers1 = self.detector.fingersUp(hand1)

            dt = self.clock.tick() / 1000
            self.level.detector = fingers1
            self.level.run(dt)

            pygame.display.update()

            if self.img_show:
                cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.img_show = False

        pygame.quit()

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    game = Game()
    game.run()