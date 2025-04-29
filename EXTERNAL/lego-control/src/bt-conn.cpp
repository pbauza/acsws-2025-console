#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/rfcomm.h>

#include "bt-conn.h"
#include <iostream>


using namespace bt;

conn::conn(const std::string& mac_addr):
    addr_(), socket_fd_(0)
{
    int status;

    socket_fd_ = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);
    addr_.rc_family = AF_BLUETOOTH;
    addr_.rc_channel = (uint8_t) 1;
    str2ba(mac_addr.c_str(), &addr_.rc_bdaddr);

    status =  connect(socket_fd_, (struct sockaddr *)&addr_, sizeof(addr_));
    if (status != 0)
        throw status;
}

conn::~conn()
{
    //close(socket_fd_);
}


void conn::write(uint8_t* payload, size_t size)
{
    int status;

    status = ::write(socket_fd_, payload, size);
    if (status < 0)
        throw status;
}

void conn::read(uint8_t* payload, size_t size)
{
    int status;

    status = ::read(socket_fd_, payload, size);
    if (status < 0 )
        throw status;
    return;
}

//int main(int argc, char **argv)
//{
//    struct sockaddr_rc addr = { 0 };
//    int s, status;
//    char dest[18] = "01:23:45:67:89:AB";
//
//    // allocate a socket
//    s = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);
//    //
//    //         // set the connection parameters (who to connect to)
//    addr.rc_family = AF_BLUETOOTH;
//    addr.rc_channel = (uint8_t) 1;
//    str2ba( dest, &addr.rc_bdaddr );
//
//    // connect to server
//    status = connect(s, (struct sockaddr *)&addr, sizeof(addr));
//
//    // send a message
//    if( status == 0 ) {
//        status = write(s, "hello!", 6);
//    }
//
//    if( status < 0 ) perror("uh oh");
//
//    close(s);
//    return 0;
//}
