#ifndef BT_CONN_H_
#define BT_CONN_H_

#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/rfcomm.h>
#include <string>

namespace bt 
{

    class conn 
    {
        public:
            conn(const std::string& mac_addr);
            ~conn();

            void write(uint8_t* msg, size_t size);
            void read(uint8_t* msg, size_t size);

        private:
            struct sockaddr_rc addr_;
            int socket_fd_;
    };
};

#endif
