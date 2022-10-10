import socket
import pickle
import struct


class ClientTundraDrone:
    """Klasa klienta do łaczenia się z serwerem do ustawiania ostrości kamer dla produktu tundra drone"""
    def __init__(self, _host, _number_port):
        """
        Konstruktor klasy
        :param _host: adres lub nazwa serwera do ustawiania ostrości kamer dla produktu tundra drone
        :type _host: str
        :param _number_port: numer portu serwera
        :type _number_port: int
        """
        self.port = _number_port
        self.host = self._prepare_host_address(_host)

    def send_command_to_camera_server(self, _command):
        """
        Metoda wysyła komende do serwera
        :param _command: komenda w postaci np. Video#A#480#480#640#640
        :type _command: str
        :return: obiekt połączenia z serwerem
        :rtype: socket.socket
        """
        _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _result = None
        while _result is None:  # reconnects if connection refused
            try:
                _client_socket.connect((self.host, self.port))  # a tuple
                _client_socket.sendall(_command.encode('utf-8'))
            except OSError as e:
                print(e)
            else:
                break
        return _client_socket

    @classmethod
    def _prepare_host_address(cls, _address_ip_or_name_host):
        """
        Metoda zamienia nazwe hosta a adres ip
        :param _address_ip_or_name_host: Nazwa lub adres IP hosta
        :type _address_ip_or_name_host: str
        :return: Zwraca adres IP hosta
        :rtype: str
        """

        if _address_ip_or_name_host.split('.')[0].isdigit():  # sprawdz czy jest to adres ip
            return socket.gethostbyname(_address_ip_or_name_host)
        else:
            return socket.gethostbyname(_address_ip_or_name_host + '.local')

    @classmethod
    def download_data(cls, _client_socket, _data, _payload_size):
        """
        Metoda do pobierania danych z serwera
        :param _client_socket: Obiekt nawiazanego połaczenia z serwerem
        :type _client_socket: socket.socket
        :param _data: Dane do pobrania
        :type _data: bytearray
        :param _payload_size: Rozmiar pobranych danych
        :type _payload_size: int
        :return: Zwraca dane z serwera wraz z rozmiarem
        :rtype: tuple
        """

        while len(_data) < _payload_size:
            _packet = _client_socket.recv(4 * 1024)  # 4K
            if not _packet: break
            _data += _packet
        _packed_msg_size = _data[:_payload_size]
        _data = _data[_payload_size:]
        _msg_size = struct.unpack("Q", _packed_msg_size)[0]
        while len(_data) < _msg_size:
            _data += _client_socket.recv(4 * 1024)
        return _data, _msg_size

    def download_frame_from_server(self, _client_socket, _data, _payload_size):
        """
        Pobiera ramke obrazu z serwera
        :param _client_socket: Obiekt nawiazanego połaczenia z serwerem
        :type _client_socket: socket.socket
        :param _data: Dane do pobrania
        :type _data: bytearray
        :param _payload_size: Rozmiar pobranych danych
        :type _payload_size: int
        :return: Zwraca ramkę obrazu
        :rtype: numpy.ndarray
        """
        _data, msg_size = self.download_data(_client_socket, _data, _payload_size)
        return self.convert_data_to_frame(_data, msg_size)

    @classmethod
    def convert_data_to_frame(cls, _data, _msg_size):
        """
        Metoda konwertuje pobrane dane na ramke obrazu
        :param _data: Pobrane dane
        :type _data: bytearray
        :param _msg_size: Rozmiar pobranych danych
        :type _msg_size: int
        :return: Zwraca przekonwertowaną ramkę obrazu
        :rtype: tuple
        """
        frame_data = _data[:_msg_size]
        _data = _data[_msg_size:]
        frame = pickle.loads(frame_data)
        return _data, frame


if __name__ == '__main__':
    port = 5000
    server_address = '10.100.255.215'
    client = ClientTundraDrone(server_address, port)

