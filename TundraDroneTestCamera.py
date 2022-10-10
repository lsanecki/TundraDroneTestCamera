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

                frame2 = focus.detect_blur(frame)

                h, w, ch = frame2.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(frame2.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if self.stop_stream == True:
                    cv2.imwrite('out.jpg', frame)
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

    def config_gui_widget(self):
        self.connect_btn()
        self.set_t_box_sn()

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
            else:
                print("kod NOK")
                self.t_box_sn.clear()

    def connect_btn(self):
        self.btn_start_test.clicked.connect(self.clicked_btn_start)
        self.btn_stop_test.clicked.connect(self.clicked_btn_stop)
        self.btn_save_db.clicked.connect(self.clicked_btn_save_db)

    def clicked_btn_start(self):
        self.btn_start_test.setEnabled(False)
        self.btn_stop_test.setEnabled(True)

        self.th_stream_video = Thread(self)
        self.th_stream_video.changePixmap.connect(self.set_image)
        self.th_stream_video.setTerminationEnabled(True)
        self.th_stream_video.start()

    def clicked_btn_stop(self):
        self.th_stream_video.stop_stream = True
        self.btn_stop_test.setEnabled(False)
        self.btn_save_db.setEnabled(True)

    def clicked_btn_save_db(self):
        self.btn_save_db.setEnabled(False)

        frame = cv2.imread('out.jpg')
        status, frame = self.detect_blur(frame, 300)

        db = DbAmlM2Tester()
        db.save_to_db(self.t_box_sn.text(), status, "0")
        self.status = ""
        self.t_box_sn.clear()
        self.t_box_sn.setEnabled(True)
        # czyszczenie tBoxSN
        # wlaczenie edtycji t_box_sn

    def variance_of_laplacian(self, img2):
        # compute the Laplacian of the image and then return the focus
        # measure, which is simply the variance of the Laplacian
        gray = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def BGR2RGB(self, BGR_img):
        # turning BGR pixel color to RGB
        rgb_image = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2RGB)
        return rgb_image

    def detect_blur(self, img, threshold):
        text = "OK"
        fm = self.variance_of_laplacian(img)
        if fm < threshold:
            text = "NOK"
        return text, img


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ControlGui()
    window.show()
    sys.exit(app.exec_())
