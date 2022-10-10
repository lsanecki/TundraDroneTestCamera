import socket
import pickle
import struct


class ClientTundraDrone:
    """Klasa klienta do łaczenia się z serwerem do ustawiania ostrości kamer dla produktu tundra drone"""
    def __init__(self, host, number_port):
        """
        Konstruktor klasy
        :param host: adres lub nazwa serwera do ustawiania ostrości kamer dla produktu tundra drone
        :type host: str
        :param number_port: numer portu serwera
        :type number_port: int
        """
        self.port = number_port
        self.host = self._prepare_host_address(host)

    def send_command_to_camera_server(self, command):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = None
        while result is None:  # reconnects if connection refused
            try:
                client_socket.connect((self.host, self.port))  # a tuple
                client_socket.sendall(command.encode('utf-8'))
            except OSError as e:
                print(e)
            else:
                break
        return client_socket

    @classmethod
    def _prepare_host_address(cls, address_ip_or_name_host: str):
        """pobranie adresu ip serwera
        :param address_ip_or_name_host: Adres ip serwera lub nazwa serwera """

        if address_ip_or_name_host.split('.')[0].isdigit():  # sprawdz czy jest to adres ip
            address_ip_or_name_host = socket.gethostbyname(address_ip_or_name_host)
            return address_ip_or_name_host
        else:
            address_ip_or_name_host = socket.gethostbyname(address_ip_or_name_host + '.local')
            return address_ip_or_name_host

    @classmethod
    def download_data(cls, client_socket, data, payload_size):
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)
        return data, msg_size

    def download_frame_from_server(self, client_socket, data, payload_size):
        data, msg_size = self.download_data(client_socket, data, payload_size)
        return self.prepare_frame(data, msg_size)

    def prepare_frame(self, data, msg_size):
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        return data, frame

    @classmethod
    def download_data2(cls, client_socket):
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K
            if not packet: break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)
        return data, msg_size


if __name__ == '__main__':
    port = 5000
    server_address = '10.100.255.215'
    client = ClientTundraDrone(server_address, port)
