import cv2


class RpiCamera:
    """Klasa do obslugi kamery"""

    def __init__(self):
        """Konstruktor klasy RpiCamera"""
        pass

    @classmethod
    def make_photo(cls, _width, _height):
        """
        Metoda wykonuje wykonuje zdjęcie z podłaczonej kamery
        :param _width: Szerokość zdjecia w pixelach
        :type _width: int
        :param _height: Wysokość zdjęcia w pixelach
        :type _height: int
        :return: Zwraca wykonane zdjęcie
        :rtype: numpy.ndarray
        """
        _cap = cv2.VideoCapture(0)
        _cap.set(3, int(_width))
        _cap.set(4, int(_height))
        ret, _img = _cap.read()
        _cap.release()

        if ret:
            return _img
        else:
            return

    @classmethod
    def crop_image(cls, _img, _x, _y):
        """
        Metoda kadruje zdjecie wedlug podanych rozmiarów
        :param _img: Obraz do kadrowania
        :type _img: numpy.ndarray
        :param _x: Współrzedne na osi x do kadrowania [poczatek, koniec]
        :type _x: list
        :param _y: Współrzedne na osi y do kadrowania [poczatek, koniec]
        :type _y: list
        :return: Zwraca przerobiony obraz
        :rtype: numpy.ndarray
        """

        _crop = _img[int(_y[0]):int(_y[1]), int(_x[0]):int(_x[1])]
        return _crop

    @classmethod
    def open_stream(cls, _width, _height):
        """
        Metoda otwiera strumien kamery
        :param _width: szerokosc w pixelach
        :type _width: int
        :param _height: wysokosc w pixelach
        :type _height: int
        :return: Zwraca otwarty strumien kamery
        :rtype: cv2.VideoCapture
        """
        _cap = cv2.VideoCapture(0)
        _cap.set(3, int(_width))
        _cap.set(4, int(_height))
        return _cap


if __name__ == '__main__':
    camera = RpiCamera()
    cap = camera.open_stream(480, 640)
    print(type(cap))
    cap.release()
