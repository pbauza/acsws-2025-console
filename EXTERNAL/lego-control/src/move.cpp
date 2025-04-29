#include "nxt.h"
#include "bt-conn.h"
#include "antenna.h"

#include <iostream>
#include <unistd.h>

int main(int argc, char** argv) {
    bt::conn nxt("00:16:53:13:05:B2");
    model::Motor motor (model::motor_port::A, &nxt);
    auto tc = motor.move_to(75, 25, -1000, std::chrono::milliseconds(10000));
    std::cout << "Current tacho: " << tc << std::endl;

    sleep(2);
    return 0;
}
