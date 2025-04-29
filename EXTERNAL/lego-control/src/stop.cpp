#include "nxt.h"
#include "bt-conn.h"
#include <iostream>
#include <unistd.h>

int main(int argc, char** argv) {
    bt::conn nxt("00:16:53:13:05:B2");
    {
        int n;
        std::cout << "press enter to stop" << std::endl;
        std::cin >> n;
        SetOutputState stop_cmd (MOTOR_C, PWR_STOP, MOTORON|BRAKE|REGULATED, REGULATION_MODE_IDLE, 0,  MOTOR_RUN_STATE_RUNNING, 0);
        nxt.write(stop_cmd.payload(), 14);
        sleep(1);
    }
    return 0;
}
