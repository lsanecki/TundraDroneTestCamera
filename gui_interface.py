from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QFrame, QLabel, QProgressBar, QLCDNumber, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt


class GuiWidget(object):
    """Interefejs gui"""

    def __init__(self):
        """ Konstruktor klasy """
        self.btn_close = None
        self.btn_save_db = None
        self.layout_footer = None
        self.frame_footer = None
        self.p_box_preview_camera = None
        self.btn_stop_test = None
        self.btn_start_test = None
        self.layout_menu_camera = None
        self.layout_preview_camera = None
        self.t_box_sn = None
        self.layout_sn = None
        self.lab_sn_product = None
        self.frame_sn_test_product = None
        self.layout_test = None
        self.frame_test = None
        self.lab_message = None
        self.lab_select_project = None
        self.layout_project_information = None
        self.layout_header = None
        self.frame_header = None
        self.layout_win = None

    def setup_ui(self, _widget):
        """
        Tworzy główne okno programu
        :param _widget: Widget okna głównego
        :type _widget: __main__.ControlGui
        :return:
        """

        _widget.setObjectName("Widget")
        self.layout_win = QVBoxLayout(self)
        self.insert_header()
        self.insert_test_frame()
        self.insert_footer()

    def insert_header(self):
        """
        Wstawia nagłówek do głównego okna wraz z kontrolkami gui nagłówka
        :return:
        """

        self.frame_header = QFrame()
        self.insert_layout_project_information()
        self.init_project_information()

        self.layout_win.addWidget(self.frame_header, 2)

    def insert_layout_project_information(self):
        """
        Wstawia do nagłówka layout z informacjami o testowanym projekcie
        :return:
        """
        self.layout_header = QVBoxLayout(self.frame_header)
        self.layout_project_information = QHBoxLayout()

    def init_project_information(self):
        """
        Wstawia do layoutu nagłówka widgety (kontrolki gui)
        :return:
        """
        self.init_widget_lab_project()
        self.init_widget_lab_select_project()
        self.layout_header.addLayout(self.layout_project_information, 3)
        self.init_widget_lab_message()

    def init_widget_lab_project(self):
        """
        Wstawia widget QLabel (etykiete) 'Projekt:'
        :return:
        """

        _labProject = QLabel("Projekt: ")
        _labProject.adjustSize()
        self.layout_project_information.addWidget(_labProject, 1)

    def init_widget_lab_select_project(self):
        """
        Wstawia etykiete z nazwa wybranego projektu
        :return:
        """

        self.lab_select_project = QLabel("Wybrany project")
        self.lab_select_project.adjustSize()
        self.lab_select_project.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout_project_information.addWidget(self.lab_select_project, 5)

    def init_widget_lab_message(self):
        """
        Wstawia etykiete na ktorej beda pojawiac sie komuniakty dotyczace testu
        :return:
        """

        self.lab_message = QLabel("Komunikat")
        self.lab_message.adjustSize()
        self.lab_message.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout_header.addWidget(self.lab_message)

    def insert_test_frame(self):
        """
        Wstawia ramke obslugi testu
        :return:
        """

        self.frame_test = QFrame()
        self.layout_test = QVBoxLayout(self.frame_test)
        self.init_frame_sn_test_product()
        self.layout_win.addWidget(self.frame_test, 6)

    def init_frame_sn_test_product(self):
        """
        Wstawia ramke z kontrolkami do obslugi testu
        :return:
        """
        self.frame_sn_test_product = QFrame()
        self.layout_sn = QHBoxLayout(self.frame_sn_test_product)
        self.init_lab_serial_number()
        self.init_t_box_serial_number()
        self.layout_test.addWidget(self.frame_sn_test_product)
        self.init_preview_camera_menu()

    def init_lab_serial_number(self):
        """
        Wstawia etykiete statyczną 'SN:'
        :return:
        """

        self.lab_sn_product = QLabel("SN:")
        self.lab_sn_product.adjustSize()
        self.lab_sn_product.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout_sn.addWidget(self.lab_sn_product)

    def init_t_box_serial_number(self):
        """
        Wstawia textbox do wczytywania numerów seryjnych testowanych wyrobów
        :return:
        """

        self.t_box_sn = QLineEdit()
        self.layout_sn.addWidget(self.t_box_sn)

    def init_preview_camera_menu(self):
        """
        Wstawia kontrolki do obslugi testu
        :return:
        """
        self.layout_preview_camera = QVBoxLayout()
        self.layout_menu_camera = QHBoxLayout()
        self.init_btn_start_test()
        self.init_btn_stop_test()
        self.init_picture_box_preview_camera()
        self.layout_test.addLayout(self.layout_preview_camera)

    def init_picture_box_preview_camera(self):
        """
        Wstawia kontrolke picturebox do podgladu z kamery
        :return:
        """

        self.layout_preview_camera.addLayout(self.layout_menu_camera)
        self.p_box_preview_camera = QLabel()
        self.p_box_preview_camera.resize(640, 480)
        _pixmap = QPixmap('Image/empty.png')
        self.p_box_preview_camera.setPixmap(_pixmap)
        self.layout_preview_camera.addWidget(self.p_box_preview_camera)

    def init_btn_stop_test(self):
        """
        Wtawia button stop test
        :return:
        """

        self.btn_stop_test = QPushButton("Zatrzymaj")
        self.layout_menu_camera.addWidget(self.btn_stop_test)

    def init_btn_start_test(self):
        """
        Wstawia button start test
        :return:
        """
        self.btn_start_test = QPushButton("Rozpocznij")
        self.layout_menu_camera.addWidget(self.btn_start_test)

    def insert_footer(self):
        """
        Wstawia stopke wraz z kontrolkami
        :return:
        """

        self.frame_footer = QFrame()
        self.layout_footer = QHBoxLayout(self.frame_footer)
        self.init_btn_save_db()
        self.init_btn_close_program()
        self.layout_win.addWidget(self.frame_footer, 3)

    def init_btn_close_program(self):
        """
        Wstawia button do zamkniecia programu
        :return:
        """
        self.btn_close = QPushButton("Zamknij program")
        self.layout_footer.addWidget(self.btn_close)

    def init_btn_save_db(self):
        """
        Wstawia button do zapisu do bazy danych
        :return:
        """
        self.btn_save_db = QPushButton("Zapisz wynik")
        self.layout_footer.addWidget(self.btn_save_db)
