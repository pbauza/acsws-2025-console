#include "nxt.h"
#include "bt-conn.h"
#include <iostream>
#include <unistd.h>

int main(int argc, char** argv) {
    bt::conn nxt("00:16:53:13:05:B2");
//    {
//        BeepCommand beep_cmd;
//        nxt.write(beep_cmd.payload(), 8);
//        std::cout << "cmd: " << beep_cmd.cmd_hex() << std::endl;
//        sleep(1);
//    }
//    {
//        SetOutputState start_cmd (0x80, MOTOR_C, PWR_14_FW, MOTORON|BRAKE|REGULATED, REGULATION_MODE_IDLE, 0,  MOTOR_RUN_STATE_RUNNING, 0);
//        nxt.write(start_cmd.payload(), 14);
//        sleep(5);
//    }
//    {
//        SetOutputState start_cmd (0x80, MOTOR_C, PWR_HALF_FW, MOTORON|BRAKE|REGULATED, REGULATION_MODE_IDLE, 0,  MOTOR_RUN_STATE_RUNNING, 0);
//        nxt.write(start_cmd.payload(), 14);
//        sleep(5);
//    }
//    {
//        SetOutputState stop_cmd (0x80, MOTOR_C, PWR_STOP, MOTORON|BRAKE|REGULATED, REGULATION_MODE_IDLE, 0,  MOTOR_RUN_STATE_RUNNING, 0);
//        nxt.write(stop_cmd.payload(), 14);
//        sleep(1);
//    }
//    {
//        SetOutputState start_cmd (0x80, MOTOR_C, PWR_FULL_BW, MOTORON|BRAKE|REGULATED, REGULATION_MODE_IDLE, 0,  MOTOR_RUN_STATE_RUNNING, 0);
//        nxt.write(start_cmd.payload(), 14);
//        sleep(5);
//    }
//    {
//        SetOutputState stop_cmd (0x80, MOTOR_C, PWR_STOP, MOTORON|BRAKE|REGULATED, REGULATION_MODE_IDLE, 0,  MOTOR_RUN_STATE_RUNNING, 0);
//        nxt.write(stop_cmd.payload(), 14);
//        sleep(1);
//    }
    {
        GetOutputState cmd (MOTOR_C);
        std::cout << "GetOutputState: " << cmd.cmd_hex() << std::endl;
        std::shared_ptr<GetOutputState_ret_pack> r = cmd.get_response(nxt);
        std::cout << "Returning status " << r->cmd_hex() << std::endl;
        std::cout << "RotationCount: " << r->rotation_count << std::endl;
    }
    return 0;
}
