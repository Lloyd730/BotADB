#  ADB Game Automation Bot

This project contains two implementations for automating Android interaction via ADB:

1. A **Python OOP implementation** with OpenCV-based image recognition.
2. A **Bash + Python hybrid implementation** using shell commands and a virtual environment for image detection.

Both versions can:

- Unlock your Android device.
- Launch or close an app.
- Perform taps and swipes.
- Recognize UI elements by image matching.

---

## Contents

- Features
- Requirements
- Image Recognition
- Sample Usage
- License
- Set Up ADB

---

##  Features

-  Unlock Android phone with swipe + PIN
-  Launch or close any app
-  Tap or swipe on screen
-  Image-based UI detection using OpenCV
-  Screenshot capture and template matching

---

## Requirements

### System

- ADB (Android Debug Bridge)
- Python 3.8+
- ImageMagick (`identify` command for Bash bot)

Install via:

bash:

	sudo apt install adb imagemagick

Python
Install dependencies in your virtual environment:


	python3 -m venv venv
	source venv/bin/activate
	pip install opencv-python numpy pillow

# Image Recognition

Both versions depend on template matching:

- The device screen is captured using ADB.
    
- The Python script uses `cv2.matchTemplate` to locate an image on the screen.
    
- If found, it returns normalized coordinates (`x y` between `0.0` and `1.0`).
    
- The Bash version scales this to pixel coordinates using ImageMagick.
    

### Expected Python output:

If a match is found:
	0.42 0.65

If not:
	NOT_FOUND (confidence: 0.45)

# Sample Usage (Bash)

	# Open the game
	open_app
	
	# Wait 5 seconds
	sleep 5
	
	# Tap only if "play_button.png" is visible
	check_and_tap "play_button.png" || echo "Play button not found."
	
	# Close the game
	close_app

---

## Setting Up ADB (Android Debug Bridge)

ADB lets your computer communicate with your Android device for automation, debugging, and control. Follow these steps to set it up:

---

### Step 1: Enable Developer Options on your Android Device

1. Open **Settings**
2. Go to **About phone**
3. Tap **Build number** 7 times until you see: `You are now a developer!`

---

### Step 2: Enable USB Debugging

1. Go back to **Settings**
2. Open **Developer options**
3. Enable **USB Debugging**

---

### Step 3: Install ADB on Your Computer

#### On **Debian/Ubuntu/Linux**:

```bash
sudo apt update
sudo apt install adb
```

#### On **Windows**:

1. Download the SDK Platform Tools:  
   [https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools)

2. Extract the ZIP to a folder (e.g., `C:\adb`)

3. Add the folder to your **System Environment Variables > Path**

4. Open **CMD or PowerShell** and type:

```cmd
adb devices
```

You should see your device listed (if connected with USB).

---

###  Step 4: Authorize Connection

- On your phone, when prompted with **“Allow USB debugging?”**, tap **Allow**.
- To check if it's working:

```bash
adb devices
```

Output should look like:

```
List of devices attached
ZX1XXXXXXX	device
```

---

# License

This automation is provided for educational and personal use only. Use responsibly and do not violate any terms of service of the applications being automated.
