class ProductCode:
    """
    Klasa do obsługi numeru seryjnego produktu
    """

    def __init__(self, _serial_number):
        """
        Konstruktor klasy
        :param _serial_number: numer seryjny produktu
        :type _serial_number: str
        """
        self.serial_number = _serial_number

    def check_hash(self):
        """
        Metoda do usuwania znaku # na poczatku SN
        :return:
        """
        if self.serial_number[0] == "#":
            self.serial_number = self.serial_number[1:]

    def check_format(self):
        """
        Metoda do sprawdzania czy wszystkie znaki w SN sa cyframi
        :return: Zwraca informacje czy SN sklada sie z cyfr
        :rtype: bool
        """
        return self.serial_number.isdigit()

    def check_length_sn(self, len_code):
        """
        Metoda do sprawdzania ilosci znakow w SN
        :param len_code: Ilosc znakow ile powinien miec SN
        :type len_code: int
        :return: Zwraca informacje czy ilosc znakow sie zgadza
        :rtype: bool
        """
        if len(self.serial_number) == len_code:
            return self.check_format()
        return False

    def check_sn(self, len_code):
        """
        Metoda do spradzania SN
        :param len_code: Ilosc znakow ile powinien miec SN
        :type len_code: int
        :return: Zwraca informacje czy SN jest prawidlowy
        :rtype: bool
        """
        self.check_hash()
        return self.check_length_sn(len_code)


def main():
    code = ProductCode("123456789")
    print(code.check_sn(9))


if __name__ == '__main__':
    main()
