from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QFrame, QLabel, QProgressBar, QLCDNumber, QLineEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt


class GuiWidget(object):
    """Interefejs gui"""

    def __init__(self):
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

    def setup_ui(self, widget):
        """Tworzy główne okno"""
        widget.setObjectName("Widget")
        self.layout_win = QVBoxLayout(self)
        self.insert_header()
        self.insert_test_frame()
        self.insert_footer()

    def insert_header(self):
        """ Wstawia nagłówek wraz z elementami do głównego okna"""
        self.frame_header = QFrame()
        self.layout_header = QVBoxLayout(self.frame_header)
        self.layout_project_information = QHBoxLayout()
        self.init_project_information()

        self.layout_win.addWidget(self.frame_header, 2)

    def init_project_information(self):
        """Wstawia elementy do pierwszego wiersza w nagłówku"""
        self.init_widget_lab_project()
        self.init_widget_lab_select_project()
        self.layout_header.addLayout(self.layout_project_information, 3)
        self.init_widget_lab_message()

    def init_widget_lab_project(self):
        """Wstawia etykiete statyczna 'Projekt:'"""
        _labProject = QLabel("Projekt: ")
        _labProject.adjustSize()
        self.layout_project_information.addWidget(_labProject, 1)

    def init_widget_lab_select_project(self):
        """ Wstawia etykiete z nazwa wybranego projektu"""
        self.lab_select_project = QLabel("Wybrany project")
        self.lab_select_project.adjustSize()
        self.lab_select_project.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout_project_information.addWidget(self.lab_select_project, 5)

    def init_widget_lab_message(self):
        self.lab_message = QLabel("Komunikat")
        self.lab_message.adjustSize()
        self.lab_message.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout_header.addWidget(self.lab_message)

    def insert_test_frame(self):
        """Wstawia ramke obslugi testu"""
        self.frame_test = QFrame()
        self.layout_test = QVBoxLayout(self.frame_test)
        self.init_frame_sn_test_product()
        # self.init_progress_bar()
        self.layout_win.addWidget(self.frame_test, 6)

    def init_frame_sn_test_product(self):
        self.frame_sn_test_product = QFrame()
        self.layout_sn = QHBoxLayout(self.frame_sn_test_product)

        self.lab_sn_product = QLabel("SN:")
        self.lab_sn_product.adjustSize()
        self.lab_sn_product.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout_sn.addWidget(self.lab_sn_product)

        self.t_box_sn = QLineEdit()
        # self.t_box_project_code.setEchoMode(QLineEdit.Password)
        # self.t_box_project_code.setEnabled(False)
        # self.t_box_project_code.textChanged[str].connect(self.check_t_box_project_code)
        self.layout_sn.addWidget(self.t_box_sn)
        self.layout_test.addWidget(self.frame_sn_test_product)

        self.init_preview_camera_menu()

    def init_preview_camera_menu(self):
        self.layout_preview_camera = QVBoxLayout()

        self.layout_menu_camera = QHBoxLayout()
        self.btn_start_test = QPushButton("Rozpocznij")
        self.layout_menu_camera.addWidget(self.btn_start_test)
        self.btn_stop_test = QPushButton("Zatrzymaj")
        self.layout_menu_camera.addWidget(self.btn_stop_test)

        self.layout_preview_camera.addLayout(self.layout_menu_camera)

        self.p_box_preview_camera = QLabel()
        self.p_box_preview_camera.resize(640, 480)
        _pixmap = QPixmap('Image/empty.png')
        self.p_box_preview_camera.setPixmap(_pixmap)

        self.layout_preview_camera.addWidget(self.p_box_preview_camera)

        self.layout_test.addLayout(self.layout_preview_camera)

    def insert_footer(self):
        self.frame_footer = QFrame()
        self.layout_footer = QHBoxLayout(self.frame_footer)

        self.btn_save_db = QPushButton("Zapisz wynik")
        self.btn_close = QPushButton("Zamknij program")

        self.layout_footer.addWidget(self.btn_save_db)
        self.layout_footer.addWidget(self.btn_close)

        self.layout_win.addWidget(self.frame_footer, 3)
