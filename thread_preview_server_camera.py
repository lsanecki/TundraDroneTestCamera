from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from thread_server_camera_model import ServerCameraModel
import struct
from client import ClientTundraDrone
from focus_measure import FocusMeasure


class ThreadPreviewCamera(QThread):
    change_pixmap = pyqtSignal(QImage)
    stop_stream = False
    test_status = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        try:
            self.stream_video_from_server()
        except Exception as e:
            print('Blad ThreadPreviewCamera: ', str(e))

    def stream_video_from_server(self):

        _camera_model = ServerCameraModel()
        _client, _client_socket, _data, _payload_size = self.connect_to_server(_camera_model)
        _focus = FocusMeasure(_camera_model.camera_threshold)
        while True:
            _data, _frame_from_server = _client.download_frame_from_server(_client_socket, _data, _payload_size)

            _frame_with_focus_status, _focus_status = _focus.detect_blur(_frame_from_server)

            _p = self.convert_frame_to_qt_image(_frame_with_focus_status)
            self.change_pixmap.emit(_p)
            if self.stop_stream:
                self.test_status.emit(str(_focus_status))
                break

    @classmethod
    def convert_frame_to_qt_image(cls, _frame_with_focus_status):
        _h, _w, _ch = _frame_with_focus_status.shape
        _bytes_per_line = _ch * _w
        _convert_to_qt_format = QImage(_frame_with_focus_status.data, _w, _h, _bytes_per_line, QImage.Format_RGB888)
        p = _convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return p

    @classmethod
    def connect_to_server(cls, camera_model):
        client = ClientTundraDrone(camera_model.server_address, camera_model.port)
        client_socket = client.send_command_to_camera_server(camera_model.command_to_send)
        data = b""
        payload_size = struct.calcsize("Q")
        return client, client_socket, data, payload_size

    def stop(self):
        self.stop_stream = True
        self.wait(1000)
        self.terminate()
