// adb_bot.cpp
#include <iostream>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <string>
#include <thread>
#include <chrono>

class ADBBot {
private:
    int screen_width = 1080;
    int screen_height = 1920;

    std::string run_command(const std::string& cmd) {
        std::string result;
        FILE* pipe = popen(cmd.c_str(), "r");
        if (!pipe) return "";
        char buffer[128];
        while (fgets(buffer, sizeof buffer, pipe) != nullptr) {
            result += buffer;
        }
        pclose(pipe);
        return result;
    }

public:
    void tap(int x, int y) {
        std::string cmd = "adb shell input tap " + std::to_string(x) + " " + std::to_string(y);
        std::system(cmd.c_str());
    }

    void keyevent(int keycode) {
        std::string cmd = "adb shell input keyevent " + std::to_string(keycode);
        std::system(cmd.c_str());
    }

    void swipe(int x1, int y1, int x2, int y2) {
        std::string cmd = "adb shell input swipe " + std::to_string(x1) + " " + std::to_string(y1) +
                          " " + std::to_string(x2) + " " + std::to_string(y2);
        std::system(cmd.c_str());
    }

    bool check_image(const std::string& image_name, int& tap_x, int& tap_y) {
        std::string command = "python3 image.py " + image_name + " > output.txt 2>&1";
        std::system(command.c_str());

        std::ifstream file("output.txt");
        std::string line;
        std::getline(file, line);
        if (line.find("NOT_FOUND") != std::string::npos) return false;

        float norm_x, norm_y;
        std::istringstream(line) >> norm_x >> norm_y;
        tap_x = static_cast<int>(norm_x * screen_width);
        tap_y = static_cast<int>(norm_y * screen_height);
        return true;
    }

    void wait(int seconds) {
        std::this_thread::sleep_for(std::chrono::seconds(seconds));
    }

    void perform_first_act() {
        std::cout << "[+] Closing Banners...\n";
        int x, y;
        while (check_image("x2.png", x, y)) {
            tap(x, y);
            wait(3);
        }

        wait(3);
        tap(2097, 833); // tap_container1st
        wait(5);

        while (check_image("watch.png", x, y) || check_image("img-getrew.png", x, y)) {
            if (check_image("watch.png", x, y)) {
                wait(15);
                while (!check_image("x.png", x, y)) {
                    wait(15);
                }
                tap(x, y);
            } else if (check_image("img-getrew.png", x, y)) {
                std::cout << "[+] Get Reward\n";
                tap(x, y);
            }
            wait(10);
            if (check_image("accept.png", x, y)) {
                tap(x, y);
                wait(10);
            }
        }
    }

    void perform_second_act() {
        int x, y;
        tap(2287, 845); // tap_rewards_daily1st
        wait(4);

        while (check_image("watch2.png", x, y)) {
            wait(3);
            std::cout << "[+] Watching ad...\n";
            while (!check_image("x.png", x, y)) {
                wait(15);
            }
            tap(x, y);

            if (check_image("accept.png", x, y)) {
                tap(x, y);
                wait(7);
            }
            std::cout << "[+] Ad closed\n";
        }
    }
};

int main() {
    ADBBot bot;
    bot.perform_first_act();
    bot.perform_second_act();
    return 0;
}
