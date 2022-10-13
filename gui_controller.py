from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from gui_interface import GuiWidget
from PyQt5.QtWidgets import QApplication, QWidget
import sys
from thread_preview_server_camera import ThreadPreviewCamera
from product_code import ProductCode
from states import ListStates
from db_tundra_drone import DbAmlM2Tester


class GuiController(QWidget, GuiWidget):
    def __init__(self, parent=None, ):
        super(GuiController, self).__init__(parent, )
        self.product_code = None
        self.serial_number = None
        self.status_stream = None
        self.th_stream_video = None
        self.status = None
        self.state_test = ListStates.INIT_TEST
        self.setup_ui(self)
        self.set_slot_and_connect()
        self.set_thread_preview_camera()
        self.set_name_project()
        self.timer()

    @pyqtSlot(QImage)
    def set_image(self, image):
        if self.status_stream:
            self.p_box_preview_camera.setPixmap(QPixmap.fromImage(image))
        else:
            self.set_default_preview_image()

    @pyqtSlot(str)
    def set_status(self, status):

        self.status = status
        self.set_message("Zatrzymano polaczenie z kamera, Status: {}".format(self.status))

    def set_slot_and_connect(self):
        self.btn_start_test.clicked.connect(self.clicked_btn_start)
        self.btn_stop_test.clicked.connect(self.clicked_btn_stop)
        self.btn_save_db.clicked.connect(self.clicked_btn_save_db)
        self.btn_close.clicked.connect(self.close)
        self.t_box_sn.textChanged[str].connect(self.check_t_box_sn)

    def clicked_btn_start(self):
        self.state_test = ListStates.START_STREAM_CAMERA
        self.timer()

    def set_thread_preview_camera(self):
        self.th_stream_video = ThreadPreviewCamera(self)
        self.th_stream_video.change_pixmap.connect(self.set_image)
        self.th_stream_video.test_status.connect(self.set_status)
        self.th_stream_video.setTerminationEnabled(True)

    def clicked_btn_stop(self):
        self.state_test = ListStates.STOP_STREAM_CAMERA
        self.timer()

    def clicked_btn_save_db(self):
        self.timer()

    def set_default_preview_image(self):
        _pixmap = QPixmap('Image/empty.png')
        self.p_box_preview_camera.setPixmap(_pixmap)

    def check_t_box_sn(self):
        if 9 <= len(self.t_box_sn.text()) <= 10:
            self.product_code = ProductCode(self.t_box_sn.text())
            if self.product_code.check_sn(9):
                self.state_test = ListStates.SN_OK
                self.timer()
            else:
                self.state_test = ListStates.SN_NOK
                self.timer()

    def set_message(self, msg):
        self.lab_message.setText(msg)

    def set_name_project(self):
        self.lab_select_project.setText("AML_M2*")

    def timer(self):
        if self.state_test == ListStates.INIT_TEST:
            self.state_init_test()
        elif self.state_test == ListStates.WAIT_FOR_SN:
            self.state_wait_for_sn()
        elif self.state_test == ListStates.SN_OK:
            self.state_sn_ok()
        elif self.state_test == ListStates.SN_NOK:
            self.state_sn_nok()
        elif self.state_test == ListStates.START_STREAM_CAMERA:
            self.state_start_stream_camera()
        elif self.state_test == ListStates.STOP_STREAM_CAMERA:
            self.state_stop_stream_camera()
        elif self.state_test == ListStates.SAVE_TO_DB:
            self.state_save_to_db()
        else:
            pass

    def state_save_to_db(self):
        db = DbAmlM2Tester()
        db.save_to_db(self.t_box_sn.text(), self.status, "0")
        self.state_test = ListStates.INIT_TEST
        self.timer()

    def state_stop_stream_camera(self):
        self.btn_stop_test.setEnabled(False)
        self.th_stream_video.stop_stream = True
        self.status_stream = False
        self.btn_save_db.setEnabled(True)
        self.state_test = ListStates.SAVE_TO_DB

    def state_start_stream_camera(self):
        self.btn_start_test.setEnabled(False)
        self.btn_stop_test.setEnabled(True)
        self.status_stream = True
        self.set_message("Ustaw ostrość kamery")
        self.th_stream_video.stop_stream = False
        self.th_stream_video.start()

    def state_sn_nok(self):
        self.t_box_sn.clear()
        self.set_message("Bledny kod zeskanuj SN jeszcze raz")
        self.state_test = ListStates.WAIT_FOR_SN
        self.timer()

    def state_sn_ok(self):
        self.t_box_sn.setEnabled(False)
        self.t_box_sn.setText(self.product_code.serial_number)
        self.set_message("Podlacz kamere i umieść w gniezdzie, a nastepnie kliknij na przycisk Rozpocznij")
        self.btn_start_test.setEnabled(True)

    def state_wait_for_sn(self):
        self.t_box_sn.setEnabled(True)
        self.t_box_sn.setFocus()

    def state_init_test(self):
        self.t_box_sn.setEnabled(False)
        self.btn_save_db.setEnabled(False)
        self.btn_stop_test.setEnabled(False)
        self.btn_start_test.setEnabled(False)
        self.status = None
        self.status_stream = True
        self.th_stream_video.stop_stream = False
        self.serial_number = None
        self.set_default_preview_image()
        self.t_box_sn.clear()
        self.set_message("Zeskanuj numer SN testowanego produktu")
        self.state_test = ListStates.WAIT_FOR_SN
        self.timer()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GuiController()
    window.show()
    sys.exit(app.exec_())
