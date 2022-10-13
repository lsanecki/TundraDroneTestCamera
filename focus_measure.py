import cv2
import numpy as np

class FocusMeasure:
    """Klasa do pomiaru ostrosci zdjecia"""
    def __init__(self, _threshold):
        """
        Konstruktor klasy
        :param _threshold: Próg wyzwalania
        :type _threshold: int
        """

        self.threshold = _threshold

    @classmethod
    def variance_of_laplacian(cls, _frame):
        """
        Metoda oblicza wariancje Laplasa obrazu
        :param _frame: Ramka obrazu
        :type _frame: numpy.ndarray
        :return: Zwraca wartość ostrości obrazu
        :rtype: int
        """

        _gray_frame = cv2.cvtColor(_frame, cv2.COLOR_RGB2BGR)
        return cv2.Laplacian(_gray_frame, cv2.CV_64F).var()

    @classmethod
    def convert_bgr_to_rgb(cls, _bgr_img):
        """
        Metoda konwertuje obraz z palety barw BGR na palete barw RGB
        :param _bgr_img: Ramka obrazu w palecie barw BGR
        :type _bgr_img: numpy.ndarray
        :return: Zwraca ramkę obrazu w palecie barw RGB
        :rtype: numpy.ndarray
        """

        _rgb_image = cv2.cvtColor(_bgr_img, cv2.COLOR_BGR2RGB)
        return _rgb_image

    def detect_blur(self, _img):
        """
        Metoda wykrywa czy obraz jest rozmazany i zapisuje status jak i wartość ostrości na ramce obrazu
        :param _img: Ramka obrazu do pomiaru ostrości
        :type _img: numpy.ndarray
        :return: Zwraca ramkę obrazu z informacją na temat ostrości wraz ze statusem
        :rtype: tuple
        """
        _fm, _text_focus_status = self.measure_focus(_img)
        _rgb_img = self.convert_bgr_to_rgb(_img)
        cv2.putText(_rgb_img, "{}: {:.2f}".format(_text_focus_status, _fm), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return _rgb_img, _text_focus_status

    def measure_focus(self, _img):
        """
        Metoda do pomiaru ostrści ramki obrazu
        :param _img: Ramka obrazu do pomiaru
        :type _img: numpy.ndarray
        :return: Zwraca wartość zmierzonej ostrości obrazu wraz ze statusem
        :rtype: tuple
        """
        _focus_status = "OK"
        _fm = self.variance_of_laplacian(_img)
        if _fm < self.threshold:
            _focus_status = "NOK"
        return _fm, _focus_status

    @classmethod
    def generate_black_image(cls):
        """
        Metoda generuje czarny obraz
        :return: Zwaraca czarny obraz
        :rtype: numpy.ndarray
        """
        return np.zeros((640, 480, 1), dtype="uint8")


if __name__ == '__main__':
    pass
