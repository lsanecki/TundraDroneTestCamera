from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from gui_interface import GuiWidget
from PyQt5.QtWidgets import QApplication, QWidget
import sys
import cv2
import struct
from product_code import ProductCode
from db_tundra_drone import DbAmlM2Tester
from client import ClientTundraDrone
from focus_measure import FocusMeasure


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    stop_stream = False
    testStatus = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        try:
            port = 5000
            server_address = '10.100.255.215'
            client = ClientTundraDrone(server_address, port)
            client_socket = client.send_command_to_camera_server('Video#A#480#480#640#640')
            data = b""
            payload_size = struct.calcsize("Q")

            threshold = 300
            focus = FocusMeasure(threshold)
            while True:
                data, frame = client.download_frame_from_server(client_socket, data, payload_size)

                frame2, status = focus.detect_blur(frame)

                h, w, ch = frame2.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(frame2.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if self.stop_stream == True:
                    self.testStatus.emit(str(status))
                    # cv2.imwrite('out.jpg', frame)
                    break
        except Exception as e:
            self.error.emit(str(e))
            print(str(e))

    def stop(self):
        self.terminate()


class ControlGui(QWidget, GuiWidget):
    def __init__(self, parent=None, ):
        super(ControlGui, self).__init__(parent, )
        self.status = None
        self.th_stream_video = None
        self.setup_ui(self)
        self.config_gui_widget()
        self.set_start_widget_parameters()
        self.set_name_project()
        self.set_message("Zeskanuj numer SN testowanego produktu")

    @pyqtSlot(QImage)
    def set_image(self, image):

        self.p_box_preview_camera.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def set_status(self, status):
        self.status = status
        print(status)

    def set_start_widget_parameters(self):
        self.btn_start_test.setEnabled(False)
        self.btn_stop_test.setEnabled(False)
        self.btn_save_db.setEnabled(False)

    def set_name_project(self):
        self.lab_select_project.setText("AML_M2*")

    def config_gui_widget(self):
        self.connect_btn()
        self.set_t_box_sn()

    def set_message(self, msg):
        self.lab_message.setText(msg)

    def set_t_box_sn(self):
        self.t_box_sn.setEnabled(True)
        self.t_box_sn.textChanged[str].connect(self.check_t_box_sn)
        self.t_box_sn.setFocus()

    def check_t_box_sn(self):
        print(self.t_box_sn.text())
        if 9 <= len(self.t_box_sn.text()) <= 10:

            product_code = ProductCode(self.t_box_sn.text())
            if product_code.check_sn(9):
                self.t_box_sn.setEnabled(False)
                self.btn_start_test.setEnabled(True)
                print("kod ok")
                self.t_box_sn.setText(product_code.serial_number)
                self.set_message("Podlacz kamere i umieść w gniezdzie, a nastepnie kliknij na przycisk Rozpocznij")
            else:
                self.set_message("Bledny kod zeskanuj SN jeszcze raz")
                print("kod NOK")
                self.t_box_sn.clear()

    def connect_btn(self):
        self.btn_start_test.clicked.connect(self.clicked_btn_start)
        self.btn_stop_test.clicked.connect(self.clicked_btn_stop)
        self.btn_save_db.clicked.connect(self.clicked_btn_save_db)
        self.btn_close.clicked.connect(self.close)

    def clicked_btn_start(self):
        self.btn_start_test.setEnabled(False)
        self.btn_stop_test.setEnabled(True)

        self.th_stream_video = Thread(self)
        self.th_stream_video.changePixmap.connect(self.set_image)
        self.th_stream_video.testStatus.connect(self.set_status)
        self.th_stream_video.setTerminationEnabled(True)
        self.th_stream_video.start()
        self.set_message("Ustaw ostrość kamery")

    def clicked_btn_stop(self):
        try:
            self.set_message("Zatrzymano polaczenie z kamera")
            self.th_stream_video.stop_stream = True
            print('Running... ', self.th_stream_video.isRunning())
            self.th_stream_video.wait(1000)

            print('isFinished: ', self.th_stream_video.isFinished())
            # self.btn_stop_test.setEnabled(False)
            # self.btn_save_db.setEnabled(True)
        except Exception as e:
            print(str(e))

    def clicked_btn_save_db(self):
        try:
            self.set_message("Zapisuje wynik do bazy")
            self.btn_save_db.setEnabled(False)
            _pixmap = QPixmap('Image/empty.png')
            self.p_box_preview_camera.setPixmap(_pixmap)

            db = DbAmlM2Tester()
            db.save_to_db(self.t_box_sn.text(), self.status, "0")
            self.status = ""
            self.t_box_sn.clear()
            self.t_box_sn.setEnabled(True)
            self.t_box_sn.setFocus()
            self.set_message("Zeskanuj numer SN testowanego produktu")
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = ControlGui()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
