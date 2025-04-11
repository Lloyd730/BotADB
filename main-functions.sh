# === CONFIG ===
PIN="1289669821"
GAME_PACKAGE="com.drivezone.car.race.game"
GAME_ACTIVITY="com.unity3d.player.UnityPlayerActivityExtension"
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

# Tap functions
function tap_rewards_daily1st(){
    tap 2287 845
}

# First click to open the container part
function tap_container1st(){
    tap 2097 833
}

function tap_X(){ # Click on X in the banners
    tap 2011 165
}

function tap_back(){ # Tap back
    keyevent KEYCODE_BACK
}

function unlocking_device(){
    # Turn on the screen
    keyevent 26 
    sleep 1
    swipe 500 1500 500 500
    sleep 2

    # Desbloqueio do celular 
    adb shell input text "$PIN"  # Change "1234" with the devices PIN
    keyevent 66  # Press "Enter"
    sleep 2
}

function closing(){
    adb shell am force-stop "$GAME_PACKAGE"
    sleep 1
    keyevent 26
    sleep 1
}

function open_Game(){
    adb shell am start -n "$GAME_ACTIVITY"
}

function check_smth() {

    local IMAGE="$1"
    source "$VENV_PATH/bin/activate"

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
    source "$VENV_PATH/bin/activate"
    
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


function first_ACT(){

    # This close all the banners
    echo "Close Banners"
    while true; do
       if ! check_smth x2.png; then
            break
        else
            tap_X
            sleep 3
        fi
    done

    # From here it opens the banners and close them
    sleep 3
    tap_container1st
    sleep 5

    while check_only watch.png || check_only img-getrew.png; do

        if check_smth watch.png; then
            sleep 15

            while true; do
                if check_smth x.png; then
                    break
                else
                    sleep 15
                fi
            done
        elif check_smth img-getrew.png; then
            echo "Get Reward"
        fi

        sleep 10
        if check_smth accept.png; then
            sleep 10
        fi
    done
}

function second_ACT(){
    # It watches the ads and closes them
    tap_rewards_daily1st
    sleep 4

    while check_smth watch2.png; do
        
        echo "loop started"
        sleep 3
        while true; do
            echo "Check to close"
            if check_smth x.png; then
                sleep 7
                break
            else
                sleep 15
            fi
        done

        if check_smth accept.png; then
            sleep 7
        fi
        echo "Loop ended"
    done
}
