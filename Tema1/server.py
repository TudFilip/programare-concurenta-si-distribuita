import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT_TO_PROTOCOL = {
    "TCP": 8001,
    "UDP": 8002,
}
STREAM_SERVER = "STREAM_SERVER"
STOP_AND_WAIT_SERVER = "STOP_AND_WAIT_SERVER"

class TCPServer:
    def __init__(self, host, port, size, ack):
        self.__host = host
        self.__port = port
        self.__size = size
        self.__ack = ack
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.__host, self.__port))

    def start(self):
        self.__sock.listen(2)

        print(f"TCP Server: Listening on {self.__host}:{self.__port}")

        while True:
            conn, addr = self.__sock.accept()
            conn.settimeout(60)
            if self.__ack == STREAM_SERVER:
                threading.Thread(target=self.__start_as_stream, args=(conn, addr,)).start()
            else:
                threading.Thread(target=self.__start_as_stop_and_wait, args=(conn, addr,)).start()

    def __start_as_stream(self, conn, addr):
        client_ip = addr[0]
        print(f"TCP Server: Client {client_ip} connected")

        count = 0
        bytes_read = 0

        now = datetime.now()
        current_timestamp = now.strftime("%d-%m-%Y_%H-%M")
        with open(f"data/server/TCP_STREAM_{current_timestamp}.pdf", "wb") as out:
            try:
                while True:
                    data = conn.recv(self.__size)

                    if not data:
                        print("TCP Server: Done reading data from client")
                        conn.close()
                        break

                    count = count + 1
                    bytes_read = bytes_read + len(data)
                    out.write(data)
            except:
                print("TCP Server: Error during receiving data")
        print("TCP Server: Received {} chunks".format(count))
        print("TCP Server: Received {} bytes".format(bytes_read))

    def __start_as_stop_and_wait(self, conn, addr):
        client_ip = addr[0]
        print(f"TCP Server: Client {client_ip} connected")

        count = 0
        bytes_read = 0
        _data = None

        now = datetime.now()
        current_timestamp = now.strftime("%d-%m-%Y_%H-%M")
        with open(f"data/server/TCP_STOP_AND_WAIT_{current_timestamp}.pdf", "wb") as out:
            try:
                while True:
                    data = conn.recv(self.__size)

                    if not data:
                        print("TCP Server: Done reading data from client")
                        conn.close()
                        break

                    out.write(data)

                    bytes_read += len(data)
                    count += 1

                    print("TCP Server: Sending ack bytes")
                    ack_bytes = bytearray()
                    ack_bytes.append(1)
                    conn.send(ack_bytes)

                    print(f"TCP Server: Send client a confirmation message for chunk {count}")
            except:
                print("TCP Server: Error during receiving data")
        print("TCP Server: Received {} chunks".format(count))
        print("TCP Server: Received {} bytes".format(bytes_read))


class UDPServer:
    def __init__(self, host, port, size, ack):
        self.__host = host
        self.__port = port
        self.__size = size
        self.__ack = ack
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((self.__host, self.__port))

    def start_as_stop_and_wait(self):
        count = 0
        bytes_read = 0

        now = datetime.now()
        current_timestamp = now.strftime("%d-%m-%Y_%H-%M")
        with open(f"data/server/UDP_STOP_AND_WAIT_{current_timestamp}.iso", "wb") as out:
            try:
                _data = None
                while True:
                    data, addr = self.__sock.recvfrom(self.__size)

                    if not data:
                        print("UDP Server: Done reading data from client")
                        break

                    out.write(data)

                    bytes_read += len(data)
                    if data != _data:
                        print(f"UDP Server: Received {len(data)} bytes")
                        _data = data
                        count += 1

                    print("UDP Server: Sending ack bytes")

                    ip, port = addr
                    ack_bytes = bytearray()
                    ack_bytes.append(1)
                    self.__sock.sendto(ack_bytes, (ip, self.__port + 1))

                    print(f"UDP Server: Send client a confirmation message for chunk {count}")
            except:
                print("UDP Server: Error during receiving data")
                print(f"UDP Server: Received {count} messages")

        print(f"UDP Server: Received {count} chunks")
        print(f"UDP Server: Received {bytes_read} bytes")

    def start_as_stream(self):
        count = 0
        bytes_read = 0

        now = datetime.now()
        current_timestamp = now.strftime("%d-%m-%Y_%H-%M")
        with open(f"data/server/UDP_STREAM_{current_timestamp}.iso", "wb") as out:
            try:
                while True:
                    data, addr = self.__sock.recvfrom(self.__size)

                    if not data:
                        print("UDP Server: Done reading data from client")
                        break

                    bytes_read += len(data)
                    count += 1
                    print(f"UDP Server: Received {len(data)} bytes")

                    out.write(data)
            except:
                print("UDP Server: Error during receiving data")
                print(f"UDP Server: Received {count} messages")

        print(f"UDP Server: Received {count} chunks")
        print(f"UDP Server: Received {bytes_read} bytes")


def start_server(protocol, chunk_size, ack):
    if protocol == "TCP":
        print("TCP Server Start Running")
        tcp_server = TCPServer(HOST, PORT_TO_PROTOCOL.get("TCP"), chunk_size, ack)
        tcp_server.start()
    elif protocol == "UDP":
        print("UDP Server Start Running")
        udp_server = UDPServer(HOST, PORT_TO_PROTOCOL.get("UDP"), chunk_size, ack)
        if ack == STREAM_SERVER:
            udp_server.start_as_stream()
        elif ack == STOP_AND_WAIT_SERVER:
            udp_server.start_as_stop_and_wait()
    else:
        print("Wrong protocol")


start_server("TCP", 65000, STREAM_SERVER)
# start_server("TCP", 65000, STOP_AND_WAIT_SERVER)
# start_server("UDP", 65000, STREAM_SERVER)
# start_server("UDP", 65000, STOP_AND_WAIT_SERVER)