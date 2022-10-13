from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from gui_interface import GuiWidget
from PyQt5.QtWidgets import QApplication, QWidget
import sys
import cv2
import struct
from product_code import ProductCode
from db_tundra_drone import DbAmlM2Tester
from client import ClientTundraDrone
from focus_measure import FocusMeasure


class ThreadPreviewCamera(QThread):
    change_pixmap = pyqtSignal(QImage)
    stop_stream = False
    test_status = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        try:
            self.connect_server_camera()
        except Exception as e:
            print('Blad ThreadPreviewCamera: ', str(e))

    def connect_server_camera(self):
        pass
