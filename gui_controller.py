from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from gui_interface import GuiWidget
from PyQt5.QtWidgets import QApplication, QWidget
import sys
from thread_preview_server_camera import ThreadPreviewCamera
from product_code import ProductCode
from db_tundra_drone import DbAmlM2Tester


class GuiController(QWidget, GuiWidget):
    def __init__(self, parent=None, ):
        super(GuiController, self).__init__(parent, )
        self.status_stream = None
        self.th_stream_video = None
        self.status = None
        self.setup_ui(self)
        self.set_slot_and_connect()
        self.set_thread_preview_camera()

    @pyqtSlot(QImage)
    def set_image(self, image):
        if self.status_stream:
            self.p_box_preview_camera.setPixmap(QPixmap.fromImage(image))
        else:
            self.set_default_preview_image()

    @pyqtSlot(str)
    def set_status(self, status):
        self.status = status

    def set_slot_and_connect(self):
        self.btn_start_test.clicked.connect(self.clicked_btn_start)
        self.btn_stop_test.clicked.connect(self.clicked_btn_stop)
        self.btn_save_db.clicked.connect(self.clicked_btn_save_db)
        self.btn_close.clicked.connect(self.close)
        self.t_box_sn.textChanged[str].connect(self.check_t_box_sn)

    def clicked_btn_start(self):
        self.status_stream = True
        self.th_stream_video.stop_stream = False
        self.th_stream_video.start()

    def set_thread_preview_camera(self):
        self.th_stream_video = ThreadPreviewCamera(self)
        self.th_stream_video.change_pixmap.connect(self.set_image)
        self.th_stream_video.setTerminationEnabled(True)

    def clicked_btn_stop(self):
        self.th_stream_video.stop_stream = True
        self.status_stream = False

    def clicked_btn_save_db(self):
        pass

    def set_default_preview_image(self):
        _pixmap = QPixmap('Image/empty.png')
        self.p_box_preview_camera.setPixmap(_pixmap)

    def set_t_box_sn(self):
        pass

    def check_t_box_sn(self):
        if 9 <= len(self.t_box_sn.text()) <= 10:
            product_code = ProductCode(self.t_box_sn.text())
            if product_code.check_sn(9):
                print("kod ok")
                self.t_box_sn.setEnabled(False)
                self.t_box_sn.setText(product_code.serial_number)
            else:
                print("kod NOK")
                self.t_box_sn.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GuiController()
    window.show()
    sys.exit(app.exec_())
