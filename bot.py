import subprocess
import time
import cv2
import numpy as np

class BotConfig:
    PIN = "00000" # Change with your pin
    GAME_PACKAGE = "com.drivezone.car.race.game" # This is the game package
    GAME_ACTIVITY = "com.unity3d.player.UnityPlayerActivityExtension" # This is the game activity

    # Static tap positions (update these to match your device)
    TAP_X = (2011, 165)         # tap_X
    TAP_CONTAINER = (2097, 833) # tap_container1st
    TAP_REWARDS = (2287, 845)   # tap_rewards_daily1st

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

    def tap_X(self):
        self.adb.tap(*BotConfig.TAP_X)

    def tap_container1st(self):
        self.adb.tap(*BotConfig.TAP_CONTAINER)

    def tap_rewards_daily1st(self):
        self.adb.tap(*BotConfig.TAP_REWARDS)

    def first_ACT(self):
        print("[*] Closing banners...")
        while True:
            if not self.tap_if_image_found("x2.png"):
                break
            self.tap_X()
            time.sleep(3)

        time.sleep(7)
        self.tap_container1st()
        time.sleep(5)

        while self.check_only("watch.png") or self.check_only("img-getrew.png"):
            if self.tap_if_image_found("watch.png"):
                print("[+] Watching ad...")
                time.sleep(15)
                while not self.tap_if_image_found("x.png"):
                    print("[*] Waiting to close ad...")
                    time.sleep(15)
            elif self.tap_if_image_found("img-getrew.png"):
                print("[+] Get Reward")

            time.sleep(10)
            if self.tap_if_image_found("accept.png"):
                time.sleep(10)

    def second_ACT(self):
        self.tap_rewards_daily1st()
        time.sleep(4)

        while self.tap_if_image_found("watch2.png"):
            print("[+] Starting ad loop")
            time.sleep(3)
            while not self.tap_if_image_found("x.png"):
                print("[*] Waiting to close ad...")
                time.sleep(15)
            time.sleep(7)
            if self.tap_if_image_found("accept.png"):
                time.sleep(7)
            print("[+] Ad cycle complete.")

# === MAIN ===

if __name__ == "__main__":
    bot = GameBot()
    bot.unlock()
    bot.open_game()
    time.sleep(30)

    bot.first_ACT()
    bot.second_ACT()

    bot.close_game()
