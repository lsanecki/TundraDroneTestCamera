# plik działa tylko na raspberry pi

import pickle
import socket
import socketserver
import struct
import sys
from camera import RpiCamera


class ServerCamera:
    """
    Server do obsługi kamery przez siec ethernet
    """

    def __init__(self):
        """Konstruktor klasy"""

        self.camera_parameters_json = None
        self.name_selected_camera = None
        self.camera_parameters = None
        self.PORT = None
        self.HOST = None
        self.init_server_parameter()

    def init_server_parameter(self):
        """Ustawienie hostu i portu serwera"""
        self.HOST = ""
        self.PORT = 5000

    def recv_data(self):
        """Odbior danych wysłanych przez klienta"""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_camera_server:
            socketserver.TCPServer.allow_reuse_address = True
            self.bind_socket_param(socket_camera_server)
            socket_camera_server.listen()
            print('Rozpoczęto słuchanie')
            while True:
                client_connection, client_address = socket_camera_server.accept()
                self.recv_client_command(client_address, client_connection)

    def recv_client_command(self, client_address, client_connection):
        """Odbiór komendy od klienta
        :param client_address: Adres Ip klienta
        :type client_address: Tuple
        :param client_connection: Połączenie z klientem
        :type client_connection: socket.socket"""

        try:
            with client_connection:
                print('Połączono z', client_address)
                while True:
                    data = client_connection.recv(4096)
                    if not data:
                        break
                    # example: 13#B#7#off
                    data = data.decode('utf-8')
                    self.read_client_data(data, client_connection)

            client_connection.close()
        except socket.error as e:
            print("Connection error: %s" % e)

    def bind_socket_param(self, socket_camera_server):
        """Dodanie parametrow do klasy socket_camera_server
        :param socket_camera_server: Obiekt gniazda serwera
        :type socket_camera_server: socket.socket"""

        try:
            socket_camera_server.bind((self.HOST, self.PORT))
            print(self.HOST, self.PORT)
        except (OverflowError, TypeError, socket.gaierror):
            print('Nieprawidłowy HOST lub PORT.')
            exit(-1)

    def read_client_data(self, data, client_connection):
        """Dekodowanie komendy od klienta
        :param data: Komenda klienta
        :type data: str
        :param client_connection: Połączenie z klientem
        :type client_connection: socket.socket"""

        _recv_data = data.split('#')
        self.select_mode(_recv_data, client_connection)

    def select_mode(self, _recv_data, client_connection):
        """Wybor trybu pracy serwera
        :param _recv_data: Dane od klienta
        :type _recv_data: list
        :param client_connection: Połączenie z klientem
        :type client_connection: socket.socket
        """
        if _recv_data[0] == 'exit':
            self.close_server(0)

        if _recv_data[0] == 'Picture':
            self.send_photo(_recv_data, client_connection)
        elif _recv_data[0] == 'Video':
            self.stream_video(_recv_data, client_connection)
        else:
            pass
        pass

    @classmethod
    def close_server(cls, _code):
        """Zamyka serwer
        :param _code: kod z jakim ma być zamkniety serwer
        :type _code: int"""

        sys.exit(_code)

    @classmethod
    def stream_video(cls, _recv_data, client_connection):
        """metoda przesyła do kienta strumien wideo
        :param _recv_data: Dane od klienta
        :type _recv_data: list
        :param client_connection: Połączenie z klientem
        :type client_connection: socket.socket
        """

        _camera = RpiCamera()
        _height = int(_recv_data[2])
        _width = int(_recv_data[4])
        vid = _camera.open_stream(_width, _height)

        while vid.isOpened():
            img, frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_connection.sendall(message)

    def send_photo(self, _recv_data, client_connection):
        """metoda wysyla do kilenta wykonane zdjecie
        :param _recv_data: Dane od klienta
        :type _recv_data: list
        :param client_connection: Połączenie z klientem
        :type client_connection: socket.socket
        """
        _crop = self.make_photo(_recv_data)
        a = pickle.dumps(_crop)
        message = struct.pack("Q", len(a)) + a
        client_connection.sendall(message)

    def make_photo(self, _recv_data):
        """wykonuje zdjecie
        :param _recv_data: Dane od klienta
        :type _recv_data: list
        :return: zwraca wykonane zdjecie
        :rtype: numpy.array"""
        _x = (int(_recv_data[4]), int(_recv_data[5]))
        _y = (int(_recv_data[2]), int(_recv_data[3]))
        _img = self.prepare_image(_x, _y)
        return _img

    def prepare_image(self, _x, _y):
        """Przygotowanie zdjecia do odczytu kodu
        :param _x: Para wspolrzednych na osi x
        :type _x: tuple
        :param _y: Para wspolrzednych na osi y
        :type _y: tuple
        :return: Obrobione zdjęcie
        :rtype: numpy.array
        """

        _cam_resolution = self.camera_parameters[self.name_selected_camera]['camResolution']
        _camera = RpiCamera()
        _img = _camera.make_photo(_cam_resolution[0], _cam_resolution[1])
        _crop = _camera.crop_image(_img, _x, _y)
        return _crop


def main():
    server = ServerCamera()
    server.recv_data()


if __name__ == '__main__':
    main()
