/*
 * nxt.cpp
 *
 *  Created on: Dec 26, 2019
 *      Author: javarias
 */
#include "nxt.h"
#include <cstring>
#include <sstream>
#include <iostream>
#include <iomanip>

header::header(uint16_t len, uint8_t cmd_type, uint8_t cmd):
len(len), cmd_type(cmd_type), cmd(cmd)
{
}

header::~header()
{
}

payload_printer::payload_printer(std::size_t cmd_len):
cmd_len(cmd_len), buff(new uint8_t[cmd_len])
{
}

payload_printer::payload_printer(std::size_t cmd_len, bt::conn c):
cmd_len(cmd_len), buff(new uint8_t[cmd_len])
{
    c.read(buff, cmd_len);
}

payload_printer::~payload_printer()
{
    delete[] buff;
}

uint8_t* payload_printer::payload()
{
    return buff;
}

void payload_printer::payload(uint8_t* buff)
{
    if (this->buff != buff) //same buff nothing to do
        std::memcpy(this->buff, buff, this->cmd_len);
}

std::string payload_printer::cmd_hex()
{
    std::ostringstream buf;
    buf.fill('0');
    buf << "0x|";
    for(int i = 0; i < (cmd_len - 1); i++) {
	    buf << std::hex << std::setw(2) << std::uppercase << (unsigned int) buff[i] << ":" << std::setw(2);
    }
	buf << std::hex << std::setw(2) << std::uppercase << (unsigned int) buff[cmd_len - 1] << std::setw(2);
    buf << std::setw(0) << "|";
    return buf.str();
}

void payload_printer::write(bt::conn c)
{
    c.write(buff, cmd_len);
}


SetOutputState::SetOutputState(uint8_t motor, int8_t power_set_point, uint8_t mode,
		uint8_t regulation, int8_t turn_ratio, uint8_t run_state, uint32_t tacho_limit):
header(12, 0x80, 0x04), payload_printer(14), motor(motor), power_set_point(power_set_point), mode(mode),
regulation(regulation), turn_ratio(turn_ratio), run_state(run_state), tacho_limit(tacho_limit)
{
	buff[0] = len & 0xFF;
	buff[1] = (len >> 8) & 0xFF;
	buff[2] = cmd_type;
	buff[3] = cmd;
	buff[4] = motor;
	buff[5] = power_set_point & 0xFF;
	buff[6] = mode;
	buff[7] = regulation;
	buff[8] = turn_ratio & 0xFF;
	buff[9] = run_state;
	buff[10] = tacho_limit & 0xFF;
	buff[11] = (turn_ratio >> 8) & 0xFF;
	buff[12] = (turn_ratio >> 16) & 0xFF;
	buff[13] = (turn_ratio >> 24) & 0xFF;
}

SetOutputState::~SetOutputState()
{
}

BeepCommand::BeepCommand():
header(6, 0x80, 0x03), payload_printer(8), tone(0x03), frequency(0x020B), duration(0x01F4)
{
	buff[0] = len & 0xFF;
	buff[1] = (len >> 8) & 0xFF;
	buff[2] = cmd_type;
	buff[3] = tone;
	buff[4] = frequency & 0xFF;
	buff[5] = (frequency >> 8) & 0xFF;
	buff[6] = duration & 0xFF;
	buff[7] = (duration >> 8) & 0xFF;
}

GetOutputState::GetOutputState(uint8_t motor):
header(3, 0x00, 0x06), payload_printer(5), motor(motor)
{
	buff[0] = len & 0xFF;
	buff[1] = (len >> 8) & 0xFF;
	buff[2] = cmd_type;
	buff[3] = cmd;
	buff[4] = motor;
}

std::shared_ptr<GetOutputState_ret_pack> GetOutputState::get_response(bt::conn c)
{
    this->write(c);
    std::shared_ptr<GetOutputState_ret_pack> ret_val (new GetOutputState_ret_pack(c));
    return ret_val;
}

GetOutputState_ret_pack::GetOutputState_ret_pack(bt::conn c):
header(0, 0, 0), payload_printer(27, c)
{
    len = 0 | (buff[1] << 8) | buff[0]; 
    cmd_type = buff[2];
    cmd = buff[3];
    status = buff[4];
    motor = buff[5];
    power_set_point = buff[6];
    mode = buff[7];
    regulation = buff[8];
    turn_ratio = buff[9];
    run_state = buff[10];
    tacho_limit = 0 | (buff[14] << 24) | (buff[13] << 16) | (buff[12] << 8) | buff[11];
    tacho_count = 0 | (buff[18] << 24) | (buff[17] << 16) | (buff[16] << 8) | buff[15];
    block_tacho_count = 0 | (buff[22] << 24) | (buff[21] << 16) | (buff[20] << 8) | buff[19];
    rotation_count = 0 | (buff[26] << 24) | (buff[25] << 16) | (buff[24] << 8) | buff[23];

}
