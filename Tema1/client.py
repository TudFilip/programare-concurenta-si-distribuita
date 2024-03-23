import socket
import time

HOST = "127.0.0.1"
PORT_TO_PROTOCOL = {
    "TCP": 8001,
    "UDP": 8002,
}
STREAM_SERVER = "STREAM_SERVER"
STOP_AND_WAIT_SERVER = "STOP_AND_WAIT_SERVER"

class TCPClient:
    def __init__(self, host, port, file_name, size, ack):
        self.__host = host
        self.__port = port
        self.__file_name = file_name
        self.__size = size
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__ack = ack

    def start(self):
        self.__sock.connect((self.__host, self.__port))
        print(f"TCP Client: Connected to {self.__host}:{self.__port}")

        start_time = time.time()

        bytes_written = 0
        count = 0

        with open(f"data/client/{self.__file_name}", "rb") as test_file:
            while True:
                data = test_file.read(self.__size)
                if not data:
                    print("TCP Client: Finish transmitting the file")
                    self.__sock.close()
                    print("TCP Client: Closing connection")
                    break

                self.__sock.send(data)

                if self.__ack == STOP_AND_WAIT_SERVER:
                    print(f"TCP Client: Waiting for server confirmation on chunk {count}")
                    while len(self.__sock.recv(1)) < 0:
                        pass
                    print(f"TCP Client: Confirmation received")

                count += 1
                bytes_written += len(data)
                print(f"TCP Client: Sent {len(data)} bytes")

        stop_time = time.time()
        print(f"TCP Client: It took {stop_time - start_time} seconds")
        print(f"TCP Client: Sent {count} chunks")
        print(f"TCP Client: Sent {bytes_written} bytes")


class UDPClient:
    def __init__(self, host, port, file_name, size, ack):
        self.__host = host
        self.__port = port
        self.__file_name = file_name
        self.__size = size
        self.__ack = ack
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__communication_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__communication_socket.bind((self.__host, self.__port + 1))
        self.__communication_socket.settimeout(3)

    def start(self):
        start_time = time.time()

        bytes_written = 0
        count = 0
        with open(f"data/client/{self.__file_name}", "rb") as test_file:
            while True:
                data = test_file.read(self.__size)

                if len(data) == 0:
                    print("UDP Client: Finish transmitting the file")
                    self.__sock.sendto(data, (self.__host, self.__port))
                    self.__sock.close()
                    print("UDP Client: Closing connection")
                    break

                self.__sock.sendto(data, (self.__host, self.__port))

                if self.__ack == STOP_AND_WAIT_SERVER:
                    print(f"UDP Client: Waiting for server confirmation on chunk {count}")
                    # data, _ = self.__communication_socket.recvfrom(1)
                    while len(self.__communication_socket.recvfrom(1)) < 0:
                        pass
                    print(f"UDP Client: Confirmation received")

                count += 1
                bytes_written += len(data)

                print(f"UDP Client: Sent {len(data)} bytes")

        stop_time = time.time()
        print(f"UDP Client: It took {stop_time - start_time} seconds")
        print(f"UDP Client: Sent {count} chunks")
        print(f"UDP Client: Sent {bytes_written} bytes")


def start_client(protocol, file_path, chunk_size, ack):
    if protocol == "TCP":
        print("TCP Client Start Running")
        tcp_client = TCPClient(HOST, PORT_TO_PROTOCOL.get("TCP"), file_path, chunk_size, ack)
        tcp_client.start()
    elif protocol == "UDP":
        print("UDP Client Start Running")
        udp_client = UDPClient(HOST, PORT_TO_PROTOCOL.get("UDP"), file_path, chunk_size, ack)
        udp_client.start()


start_client("TCP", "Curs1.pdf", 65000, STREAM_SERVER)
# start_client("UDP", "Curs1.pdf", 1024, STREAM_SERVER)
# start_client("UDP", "linuxmint-21.2-cinnamon-64bit.iso", 1024, STREAM_SERVER)
# start_client("UDP", "Curs1.pdf", 1024, STOP_AND_WAIT_SERVER)
# start_client("UDP", "linuxmint-21.2-cinnamon-64bit.iso", 1024, STOP_AND_WAIT_SERVER)
