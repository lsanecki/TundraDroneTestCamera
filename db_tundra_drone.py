from database import Database


class DbAmlM2Tester(Database):
    def __init__(self):
        _host = "10.10.100.99"
        _user = "riot_test"
        _password = "NO0abCFC6o63PXrb"
        _database = "iir"
        super().__init__(_host, _user, _password, _database)
        self.client = "TundraDrone"
        self.product = "AML_M2*"
        self.name_device = "Tester_Focus_Camera"

    def generate_sql_query(self):
        pass

    def read_id_main(self, _serial_number):
        """
        Metoda do odczytu ID z tabeli Main na podstawie SN
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :return: Zwraca numer ID z tabeli Main
        :rtype: str
        """
        _sql = "SELECT ID  FROM `Main` " \
               "WHERE `Serial` LIKE '{}' AND `Klient` LIKE '{}' AND `Wyrób` LIKE '{}' ORDER BY `ID`  DESC" \
            .format(_serial_number, self.client, self.product)
        _status, _my_result = self.select(_sql)
        if _status and len(_my_result) > 0:
            return _my_result[0][0]
        return

    def insert_record_to_main(self, _serial_number):
        """
        Metoda ktora zapisuje rekord do tabeli main
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :return: Zwrana nr ID w tabeli Main
        :rtype: int
        """
        _id_main = self.read_id_main(_serial_number)
        if _id_main is None:
            _sql = "INSERT INTO `Main` (`Serial`, `Klient`, `Wyrób`) VALUES ('{}', '{}', '{}');" \
                .format(_serial_number, self.client, self.product)
            _status, _my_result = self.insert(_sql)
            if _status:
                _id_main = self.read_id_main(_serial_number)
        return _id_main

    def count_test(self, _serial_number):
        """
        Metoda która sprawdza ile dany wyrob byl testowany
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :return: Zwraca ilosc ile dany wyrob zostal przetestowany
        :rtype: int
        """
        _sql = "SELECT COUNT(*)  FROM `Testowanie` WHERE `Serial` LIKE '{}' ORDER BY `ID_test`  DESC" \
            .format(_serial_number)
        _status, _my_result = self.select(_sql)
        if _status and len(_my_result) > 0:
            return _my_result[0][0]
        return

    def insert_record_to_test_table(self, _id_main, _serial, _name_device, _status, _error_code):
        """
        Metoda do zapisu rekordu w tabeli Testowanie
        :param _id_main: Nr id w tabeli Main
        :type _id_main: int
        :param _serial: Numer SN testowanego wyrobu
        :type _serial: str
        :param _name_device: Nazwa testera
        :type _name_device: str
        :param _status: Status czy wyrob przeszedl test
        :type _status:str
        :param _error_code: Kod bledu
        :type _error_code: str
        :return:
        """
        _count_test = self.count_test(_serial) + 1
        _sql = "INSERT INTO `Testowanie` " \
               "(`ID_test`, `ID`, `Status`, `KodBledu`, `Ilosc_prob`, `Nazwa_urzadzenia`, `FirmwareTester`," \
               " `Gniazdo`," \
               " `Serial`, `Data`, `CzasTestu`, `Serwis`, `dodatkowe_informacje`)" \
               " VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '0.1', '1', '{}', CURRENT_TIMESTAMP, NULL, NULL, NULL);" \
            .format(_id_main, _status, _error_code, _count_test, _name_device, _serial)

        print(_sql)
        _status, _my_result = self.insert(_sql)

    def check_prog_status(self, _serial_number):
        """
        Metoda do sprawdzania czy wyrob został zaprogramowany
        :param _serial_number: Numer SN testowanego wyrobu
        :return: Zwraca status programowania
        :rtype: bool
        """
        _sql = "SELECT *  FROM `Programowanie` WHERE `Serial` LIKE '{}' ORDER BY `ID_prog`  DESC" \
            .format(_serial_number)
        self.connect()
        _status, _my_result = self.select(_sql)
        self.disconnect()
        if len(_my_result) == 0:
            return False
        if _my_result[0][3] == 'OK':
            return True
        return False

    def save_to_db(self, _serial_number, _status, _error_code):
        """
        Metoda do zapisu wyniku testowania do bazy danych
        :param _serial_number: Numer SN produktu
        :type _serial_number: str
        :param _status: Status czy produkt został poprawnie przetestowany
        :type _status: str
        :param _error_code: Kod bledu
        :type _error_code: str
        :return:
        """
        self.connect()
        _id_main = self.insert_record_to_main(_serial_number)
        self.insert_record_to_test_table(_id_main, _serial_number, self.name_device, _status, _error_code)
        self.disconnect()


def main():
    db = DbAmlM2Tester()
    sn = "123456789"

    print(db.check_prog_status(sn))

    db.save_to_db(sn, "OK", "0")


if __name__ == '__main__':
    main()
