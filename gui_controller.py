from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from gui_interface import GuiWidget
from PyQt5.QtWidgets import QApplication, QWidget
import sys
from thread_preview_server_camera import ThreadPreviewCamera
from product_code import ProductCode
from states import ListStates
from db_tundra_drone import DbAmlM2Tester
from gui_model import GuiModel


class GuiController(QWidget, GuiWidget):
    """
    Kontroler GUI
    """

    def __init__(self, parent=None, ):
        """
        Konstruktor klasy
        """
        super(GuiController, self).__init__(parent, )
        self.product_code = None
        self.serial_number = None
        self.status_stream = None
        self.th_stream_video = None
        self.status = None
        self.model_gui = GuiModel()
        self.state_test = ListStates.INIT_TEST
        self.setup_ui(self)
        self.setWindowTitle("AML_M2_FOCUS_CAMERA")
        self.set_slot_and_connect()
        self.set_thread_preview_camera()
        self.set_name_project()
        self.set_font()
        self.timer()

    @pyqtSlot(QImage)
    def set_image(self, _image):
        """
        Metoda ustawia obraz w kontrolce p_box_preview_camera
        :param _image: Obraz z kamery do wyświetlania
        :type  _image: QImage
        :return:
        """
        if self.status_stream:
            self.p_box_preview_camera.setPixmap(QPixmap.fromImage(_image))
        else:
            self.set_default_preview_image()

    @pyqtSlot(str)
    def set_status(self, _status):
        """
        Metoda wyświetla status testu
        :param _status: status testu (czy ostrość kamery została poprawnie ustawiona)
        :type _status: str
        :return:
        """
        self.status = _status
        self.set_message("Zatrzymano polaczenie z kamera, Status: {}".format(self.status))
        self.set_status_test_preview_image(self.status)

    def set_font(self):
        """
        Metoda ustawia wielkosc czcionki w kontrolkach GUI
        :return:
        """

        self.set_font_btn_close()
        self.set_font_btn_save_db()
        self.set_font_btn_stop_test()
        self.set_btn_start_test()

        self.set_font_lab_sn_product()
        self.set_font_t_box_sn()
        self.set_font_lab_select_project()
        self.set_font_lab_message()

    def set_font_lab_message(self):
        """
        Metoda ustawia czcionke dla etykiety lab_message
        :return:
        """

        _font_lab_message = self.lab_message.font()
        _font_lab_message.setPointSize(self.model_gui.lab_font_size_small)
        self.lab_message.setFont(_font_lab_message)

    def set_font_lab_select_project(self):
        """
        Metoda ustawia czcionke dla etykiety lab_select_project
        :return:
        """
        _font_lab_select_project = self.lab_select_project.font()
        _font_lab_select_project.setPointSize(self.model_gui.lab_font_size_medium)
        self.lab_select_project.setFont(_font_lab_select_project)

    def set_font_t_box_sn(self):
        """
        Metoda ustawia czcionke dla TextBox t_box_sn
        :return:
        """
        _font_t_box_sn = self.t_box_sn.font()
        _font_t_box_sn.setPointSize(self.model_gui.t_box_font_size)
        self.t_box_sn.setFont(_font_t_box_sn)

    def set_font_lab_sn_product(self):
        """
        Metoda ustawia czcionke dla etykiety lab_sn_product
        :return:
        """
        _font_lab_sn = self.lab_sn_product.font()
        _font_lab_sn.setPointSize(self.model_gui.lab_font_size_small)
        self.lab_sn_product.setFont(_font_lab_sn)

    def set_btn_start_test(self):
        """
        Metoda ustawia czcionke dla button btn_start_test
        :return:
        """
        _font_btn_start_test = self.btn_start_test.font()
        _font_btn_start_test.setPointSize(self.model_gui.btn_font_size)
        self.btn_start_test.setFont(_font_btn_start_test)

    def set_font_btn_stop_test(self):
        """
        Metoda ustawia czcionke dla button btn_stop_test
        :return:
        """
        _font_btn_stop_test = self.btn_stop_test.font()
        _font_btn_stop_test.setPointSize(self.model_gui.btn_font_size)
        self.btn_stop_test.setFont(_font_btn_stop_test)

    def set_font_btn_save_db(self):
        """
        Metoda ustawia czcionke dla button btn_save_db
        :return:
        """
        _font_btn_save_db = self.btn_save_db.font()
        _font_btn_save_db.setPointSize(self.model_gui.btn_font_size)
        self.btn_save_db.setFont(_font_btn_save_db)

    def set_font_btn_close(self):
        """
        Metoda ustawia czcionke dla button btn_close
        :return:
        """
        _font_btn_close = self.btn_close.font()
        _font_btn_close.setPointSize(self.model_gui.btn_font_size)
        self.btn_close.setFont(_font_btn_close)

    def set_slot_and_connect(self):
        """
        Ustawia powiązania kontrolek GUI z metodami
        :return:
        """
        self.btn_start_test.clicked.connect(self.clicked_btn_start)
        self.btn_stop_test.clicked.connect(self.clicked_btn_stop)
        self.btn_save_db.clicked.connect(self.clicked_btn_save_db)
        self.btn_close.clicked.connect(self.close)
        self.t_box_sn.textChanged[str].connect(self.check_t_box_sn)

    def clicked_btn_start(self):
        """
        Metoda wywoluje się po naciśnieciu przycisku 'Rozpocznij', uruchamia stremowanie obrazu z serwera
        :return:
        """
        self.state_test = ListStates.START_STREAM_CAMERA
        self.timer()

    def set_thread_preview_camera(self):
        """
        Metoda ustawia paramatry wątku do połaczenia ze serwerem
        :return:
        """
        self.th_stream_video = ThreadPreviewCamera(self)
        self.th_stream_video.change_pixmap.connect(self.set_image)
        self.th_stream_video.test_status.connect(self.set_status)
        self.th_stream_video.setTerminationEnabled(True)

    def clicked_btn_stop(self):
        """
        Metoda wywołuje sie po naciśnieciu przycisku 'Zatrzymaj'
        zatrzymuje stremowanie obrazu z kamery
        :return:
        """
        self.state_test = ListStates.STOP_STREAM_CAMERA
        self.timer()

    def clicked_btn_save_db(self):
        """
        Metoda wywołuje sie po naciśnieciu przycisku 'Zapisz do bazy danych'
        uruchamia zapis wyniku testu do bazy
        :return:
        """
        self.state_test = ListStates.SAVE_TO_DB
        self.timer()

    def set_default_preview_image(self):
        """
        Ustawia domyślny obraz w kontrolce p_box_preview_camera
        :return:
        """
        _pixmap = QPixmap('Image/empty.png')
        self.p_box_preview_camera.setPixmap(_pixmap)

    def set_status_test_preview_image(self, _status):
        """
        Wyswietla na p_box status testy
        :param _status: Status testu
        :type _status: str
        :return:
        """
        if _status == "OK":
            _pixmap = QPixmap('Image/status_ok.png')
        else:
            _pixmap = QPixmap('Image/status_nok.png')

        self.p_box_preview_camera.setPixmap(_pixmap)

    def check_t_box_sn(self):
        """
        Metoda sprawdza serial number wpisany do t_box_sn
        :return:
        """
        if 9 <= len(self.t_box_sn.text()) <= 10:
            self.product_code = ProductCode(self.t_box_sn.text())
            if self.product_code.check_sn(9):
                self.state_test = ListStates.SN_OK
                self.timer()
            else:
                self.state_test = ListStates.SN_NOK
                self.timer()

    def set_message(self, _msg):
        """
        Metoda ustawia wyswietlany komunikat na ekranie
        :param _msg: Wiadomość do wyswietlenia na ekranie
        :type _msg: str
        :return:
        """

        self.lab_message.setText(_msg)

    def set_name_project(self):
        """
        Metoda ustawia nazwe testowanego produktu
        :return:
        """
        self.lab_select_project.setText("AML_M2*")

    def timer(self):
        """
        Metoda do wywałania odpowiedniego stanu urzadzenia
        :return:
        """
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
        """
        Stan urzadzenia zapisu wyniku testu do bazy danych
        :return:
        """
        db = DbAmlM2Tester()
        db.save_to_db(self.t_box_sn.text(), self.status, "0")
        self.state_test = ListStates.INIT_TEST
        self.timer()

    def state_stop_stream_camera(self):
        """
        stan urzadzenia do zatrzymania stremowania obrazu z kamery
        :return:
        """
        self.btn_stop_test.setEnabled(False)
        self.th_stream_video.stop_stream = True
        self.status_stream = False
        self.btn_save_db.setEnabled(True)
        self.state_test = ListStates.SAVE_TO_DB

    def state_start_stream_camera(self):
        """
        Stan do rozpoczenia stremowania obrazu z kamery
        :return:
        """
        self.btn_start_test.setEnabled(False)
        self.btn_stop_test.setEnabled(True)
        self.status_stream = True
        self.set_message("Ustaw ostrość kamery")
        self.th_stream_video.stop_stream = False
        self.th_stream_video.start()

    def state_sn_nok(self):
        """
        Stan odczytu blednego kodu sn
        :return:
        """
        self.t_box_sn.clear()
        self.set_message("Bledny kod zeskanuj SN jeszcze raz")
        self.state_test = ListStates.WAIT_FOR_SN
        self.timer()

    def state_sn_ok(self):
        """
        Stan odczytu poprawnego kodu sn
        :return:
        """
        self.t_box_sn.setEnabled(False)
        self.t_box_sn.setText(self.product_code.serial_number)
        self.set_message("Podlacz kamere i umieść w gniezdzie,\n a nastepnie kliknij na przycisk Rozpocznij")
        self.btn_start_test.setEnabled(True)

    def state_wait_for_sn(self):
        """stan oczekiwania na kod sn"""
        self.t_box_sn.setEnabled(True)
        self.t_box_sn.setFocus()

    def state_init_test(self):
        """Stan inicjalizacji testu"""
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
