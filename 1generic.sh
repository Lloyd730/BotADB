# === CONFIG ===
PIN="00000"
GAME_PACKAGE="com.package.game"
GAME_ACTIVITY="com.action.game"
VENV_PATH="venv"
PY_SCRIPT="image.py"

function tap() {
    echo "[+] Tapping at $1 $2"
    adb shell input tap "$1" "$2"
}

function adb_swipe() {
    local x1=$1
    local y1=$2
    local x2=$3
    local y2=$4
    adb shell input swipe "$x1" "$y1" "$x2" "$y2"
}

function keyevent() {
    echo "[+] Sending keyevent $1"
    adb shell input keyevent "$1"
}

function tap_back(){ # Tap back
    keyevent KEYCODE_BACK
}

function unlocking_device(){
    # Turn on the screen
    keyevent 26 
    sleep 1
    adb_swipe 500 1500 500 500
    sleep 2

    # Desbloqueio do celular 
    adb shell input text "$PIN"  # Change "1234" with the devices PIN
    keyevent 66  # Press "Enter"
    sleep 2
}

function openVirtualEnvironment(){
    source "$VENV_PATH/bin/activate"
}

function close_app(){
    adb shell am force-stop "$GAME_PACKAGE"
    sleep 1
    keyevent 26
    sleep 1
}

function open_app(){
    adb shell am start -n "$GAME_PACKAGE/$GAME_ACTIVITY"
}

function check_and_tap() {

    local IMAGE="$1"
    openVirtualEnvironment

    echo "[+] Taking screenshot..."
    adb exec-out screencap -p > screen.png
    # Get actual image resolution from the screenshot
    read screen_width screen_height <<< $(identify -format "%w %h" screen.png)
    echo "[+] Image resolution from screenshot: $screen_width x $screen_height"
    echo "[+] Running image check for $IMAGE"
    output=$(python3 "$PY_SCRIPT" "$IMAGE")

    deactivate

    # Check for match failure
    if [[ $output == NOT_FOUND* ]]; then
        echo "[!] $output"
        return 1
    fi

    # Split output into variables
    read norm_x norm_y <<< "$output"

    if [[ -z "$norm_x" || -z "$norm_y" ]]; then
        echo "[!] Invalid coordinates from Python: '$output'"
        return 1
    fi

    # Convert normalized to actual coordinates
    tap_x=$(awk "BEGIN { printf \"%d\", $norm_x * $screen_width }")
    tap_y=$(awk "BEGIN { printf \"%d\", $norm_y * $screen_height }")

    echo "[+] Match found at ($tap_x, $tap_y). Tapping..."
    tap "$tap_x" "$tap_y"

    return 0
}

function check_only() {
    local IMAGE="$1"
    
    openVirtualEnvironment    
    echo "[+] Taking screenshot..."
    adb exec-out screencap -p > screen.png
    echo "[+] Running image check for $IMAGE"
    output=$(python3 "$PY_SCRIPT" "$IMAGE")
    deactivate

    if [[ $output == NOT_FOUND* ]]; then
        return 1
    fi

    return 0
}
