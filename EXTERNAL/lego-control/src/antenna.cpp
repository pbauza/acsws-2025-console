#include "antenna.h"
#include <iostream>


using namespace model;

Motor::Motor(motor_port port, bt::conn* lego):
port_(port & 0xFF), lego_(lego), status_cmd_(GetOutputState(port_))
{
}

int Motor::move_to(unsigned short power, unsigned short min_power, int tacho_value, std::chrono::milliseconds timeout)
{
    if(abs(power) > 100)
        power = 100;

    int ct = current_tacho();
    
    if (abs(ct - tacho_value) < 150)
        power = min_power;
    else if ((ct - tacho_value) > 0 ) {
        power = -power;
        min_power = -min_power;
    }
    else if ((ct - tacho_value) > 0)
        return ct;

    auto start = std::chrono::steady_clock::now();
    auto end = std::chrono::steady_clock::now();
    move(power);

    auto diff = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    do {
        ct = current_tacho();
        if (abs(ct - tacho_value) < 250 && power > min_power) {
            move(min_power);
        }
        end = std::chrono::steady_clock::now();
        diff = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cout << "time diff: " << diff.count() << " ms" << std::endl;
        std::cout << "timeout: " << timeout.count() << " ms" << std::endl;
    } while (abs(ct - tacho_value) > 10 && (diff.count() < timeout.count()));
   
   stop_now();

   return current_tacho();
}

void Motor::stop_now()
{
       SetOutputState cmd (port_, 0, MOTORON|BRAKE|REGULATED, REGULATION_MODE_IDLE, 0, MOTOR_RUN_STATE_RUNNING, 0);
       cmd.write(*lego_);
}

int Motor:: current_tacho() 
{
    return status_cmd_.get_response(*lego_)->tacho_count;
}

void Motor::move(short power)
{
    if (power > 100)
        power = 100;
    else if (power < -100)
        power = -100;
    SetOutputState cmd (port_, power & 0xFF , MOTORON|BRAKE|REGULATED, REGULATION_MODE_IDLE, 0, MOTOR_RUN_STATE_RUNNING, 0);
    cmd.write(*lego_);
}
