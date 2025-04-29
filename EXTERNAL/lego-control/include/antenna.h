#ifndef ANTENNA_H_
#define ANTENNA_H_

#include "nxt.h"
#include "bt-conn.h"
#include <chrono>

namespace model
{


enum motor_port
{
    A = 0,
    B = 1,
    C = 2
};

class Motor
{
    const uint8_t port_;
    const bt::conn* lego_;
    GetOutputState status_cmd_;

    void move(short power);


    public:
    /**
     *
     * @param power 0 <= power <= 100
     * @param min_power reduced power used when approching to tacho_value
     * @param tacho_value motor will move until tacho_value is reached
     *
     */
    int move_to(unsigned short power, unsigned short min_power, int tacho_value, std::chrono::milliseconds timeout);

    void stop_now();

    int current_tacho();

    Motor(motor_port port, bt::conn* lego);
};

};

#endif
