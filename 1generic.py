import subprocess
import time
import cv2
import numpy as np

class BotConfig:
    PIN = "00000" # Change with your pin
    GAME_PACKAGE = "com.race.game" # Change with the game package 
    GAME_ACTIVITY = "com.game.activity" # Change with the game activity

class ADBBot:
    def run(self, cmd):
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)

    def tap(self, x, y):
        print(f"[+] Tapping at ({x}, {y})")
        self.run(f"adb shell input tap {x} {y}")

    def swipe(self, x1, y1, x2, y2):
        self.run(f"adb shell input swipe {x1} {y1} {x2} {y2}")

    def keyevent(self, keycode):
        print(f"[+] Keyevent {keycode}")
        self.run(f"adb shell input keyevent {keycode}")

    def input_text(self, text):
        self.run(f'adb shell input text "{text}"')

    def start_app(self, package, activity):
        self.run(f"adb shell am start -n {package}/{activity}")

    def stop_app(self, package):
        self.run(f"adb shell am force-stop {package}")

    def screenshot(self, path="screen.png"):
        self.run(f"adb exec-out screencap -p > {path}")

class ImageRecognizer:
    def find(self, screen_path, template_path, threshold=0.8):
        screen = cv2.imread(screen_path)
        template = cv2.imread(template_path)

        if screen is None or template is None:
            print(f"[!] Failed to load {template_path}")
            return None

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"[+] Match confidence for {template_path}: {max_val:.2f}")
        if max_val >= threshold:
            return max_loc  # (x, y)
        return None

class GameBot:
    def __init__(self):
        self.adb = ADBBot()
        self.cv = ImageRecognizer()

    def unlock(self):
        self.adb.keyevent(26)  # Power button
        time.sleep(2)
        self.adb.swipe(500, 1500, 500, 500)
        time.sleep(2)
        self.adb.input_text(BotConfig.PIN)
        self.adb.keyevent(66)  # Enter
        time.sleep(2)

    def open_game(self):
        self.adb.start_app(BotConfig.GAME_PACKAGE, BotConfig.GAME_ACTIVITY)

    def close_game(self):
        self.adb.stop_app(BotConfig.GAME_PACKAGE)
        self.adb.keyevent(26)

    def tap_if_image_found(self, image):
        self.adb.screenshot()
        match = self.cv.find("screen.png", image)
        if match:
            self.adb.tap(match[0], match[1])
            return True
        return False

    def check_only(self, image):
        self.adb.screenshot()
        return self.cv.find("screen.png", image) is not None
    
if __name__ == "__main__":
    bot = GameBot()