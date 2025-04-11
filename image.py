import cv2
import sys

screen_path = "screen.png"

if len(sys.argv) != 2:
    print("Usage: python3 test101.py <button_image>")
    exit(1)

button_path = sys.argv[1]

screen = cv2.imread(screen_path)
button = cv2.imread(button_path)

if screen is None or button is None:
    print("Failed to load image(s).")
    exit(1)

h, w = button.shape[:2]
screen_h, screen_w = screen.shape[:2]

result = cv2.matchTemplate(screen, button, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(result)

threshold = 0.8

if max_val >= threshold:
    x = max_loc[0] + w // 2
    y = max_loc[1] + h // 2

    norm_x = x / screen_w
    norm_y = y / screen_h

    print(f"{norm_x:.6f} {norm_y:.6f}")
    exit(0)
else:
    print(f"NOT_FOUND {max_val:.2f}")
    exit(1)
