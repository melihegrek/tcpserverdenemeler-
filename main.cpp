#include "TCP.h"

int main() {
    TCP& client = TCP::getInstance();
    client.setIpAddress("127.0.0.1"); // IP adresini ayarlayın
    client.setPort(12345); // Port numarasını ayarlayın

    client.start();

    std::vector<char> message{'H', 'e', 'l', 'l', 'o'};
    client.insert(message);

    std::this_thread::sleep_for(std::chrono::seconds(2));
    
    client.stop();
    return 0;
}
