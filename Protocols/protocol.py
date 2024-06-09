"""
Amit skarbin
"""

SIZE_TO_FILL = 15
MIN_SIZE = 0
CHUNK_SIZE = 4096  # Define a reasonable chunk size

class Protocol:
    @staticmethod
    def transmit_data(socket, data):
        encoded_msg = data.encode()
        length_str = str(len(encoded_msg)).zfill(SIZE_TO_FILL)
        length_bytes = length_str.encode()
        socket.send(length_bytes + encoded_msg)

    @staticmethod
    def receive_data(sock):
        total_size = b""
        size = SIZE_TO_FILL
        while size > MIN_SIZE:
            data = sock.recv(size)
            size -= len(data)
            total_size += data
        size = int(total_size.decode())
        total_data = b""
        while size > MIN_SIZE:
            data = sock.recv(size)
            size -= len(data)
            total_data += data
        return total_data.decode()

    @staticmethod
    def transmit_binary(sock, data):
        length_str = str(len(data)).zfill(SIZE_TO_FILL)
        sock.send(length_str.encode('utf-8'))
        sock.send(data)

    @staticmethod
    def receive_binary(sock):
        data_size_bytes = sock.recv(SIZE_TO_FILL)
        data_size_str = data_size_bytes.decode('utf-8')
        if not data_size_str.isdigit():
            raise ValueError(f"Invalid data size received: {data_size_bytes}")
        size = int(data_size_str)
        total_data = b''
        while size > 0:
            part = sock.recv(size)
            if not part:
                raise ConnectionError("Connection closed during data reception")
            total_data += part
            size -= len(part)
        return total_data