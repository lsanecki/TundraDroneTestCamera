import cv2


class RpiCamera:
    """Klasa do obslugi kamery"""

    def __init__(self):
        """Konstruktor klasy RpiCamera"""
        pass

    @classmethod
    def make_photo(cls, _width, _height):
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
        _crop = _img[int(_y[0]):int(_y[1]), int(_x[0]):int(_x[1])]
        return _crop

    @classmethod
    def open_stream(cls, _width, _height):
        _cap = cv2.VideoCapture(0)
        _cap.set(3, int(_width))
        _cap.set(4, int(_height))
        return _cap
