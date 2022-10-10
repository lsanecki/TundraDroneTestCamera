import mysql.connector


class Database:
    """Klasa do obslugi bazy danych MySql"""

    def __init__(self, _host: str, _user: str, _password: str, _database: str):
        """Konstruktor klasy
        :param _host: Adres serwera bazy danych
        :type _host: str
        :param _user: Nazwa użytkownika bazy danych
        :type _user: str
        :param _password: Hasło do bazy danych
        :type _password: str
        :param _database: Nazwa bazy danych
        :type _database"""

        self.mydb = None
        self.host = _host
        self.user = _user
        self.password = _password
        self.database = _database
        self.status_db = False

    def connect(self):
        """Tworzy połączenie z bazą danych"""

        try:
            self.mydb = mysql.connector.connect(user=self.user,
                                                password=self.password,
                                                host=self.host,
                                                database=self.database)
            print("Połączono... ")
            self.status_db = True
        except mysql.connector.errors.DatabaseError as err:
            print(str(err))
            self.status_db = False

    def disconnect(self):
        """Zamyka połącznie z bazą danych"""

        if self.status_db:
            self.mydb.disconnect()
            self.status_db = False
            print("Rozłączono... ")

    def check_connection(self):
        """Sprawdza połączenie z bazą danych
        :return: zwraca status połaczenia z baza danych
        :rtype: bool"""

        self.connect()
        _status = self.status_db
        self.disconnect()
        return _status

    def insert(self, _sql):
        """Wstawia nowy wiersz do bazy danych
        :param _sql: zapytanie sql
        :type _sql: str
        :return: Zwraca status zapisu do bazy
        :rtype: bool"""

        _status, _my_result = self.exec_query(_sql, 'w')
        print("Status zapisu do bazy: {}".format(_status))
        return _status, _my_result

    def insert_multi(self, _sql):
        """Wstawia dane do bazy danych dla kilku tabel
        :param _sql: zapytanie sql
        :type _sql: str
        :return: Zwraca status zapisu do bazy
        :rtype: bool"""

        _my_cursor = self.mydb.cursor()
        for result in _my_cursor.execute(_sql, multi=True):
            if result.with_rows:
                print("Rows produced by statement '{}':".format(
                    result.statement))
                print(result.fetchall())
            else:
                print("Zapis rekordu '{}': {}".format(
                    result.statement, result.rowcount))

    def select(self, _sql):
        """Odczytuje rekordy z bazy danych
        :param _sql: zapytanie sql
        :type _sql: str
        :return: status i wynik zapytania
        :rtype: list"""

        _status, _my_result = self.exec_query(_sql, 'r')

        return _status, _my_result

    def exec_query(self, _sql, _mode='r'):
        """Wywołuje zapytanie sql dla bazy danych
        :param _sql: zapytanie sql
        :type _sql: str
        :param _mode: tryb wywołania zapytania 'r' - odczyt, 'w' - zapis
        :type _mode: str
        :return _status: status wywołania zapytania
        :rtype _status: bool
        :return _my_result: wynik zapytania
        :rtype _my_result: list"""

        _status = False
        _my_result = []
        if self.status_db:
            try:
                _my_cursor = self.mydb.cursor()
                _my_cursor.execute(_sql)
                _my_result = self.select_mode_exec_query(_mode, _my_cursor, _my_result)
                _status = True
            except mysql.connector.errors.ProgrammingError as er:
                print("Blad zapytania sql do bazy: ", str(er))
                _status = False
        return _status, _my_result

    def select_mode_exec_query(self, _mode, _my_cursor, _my_result):
        """Wybor trybu zapytania do bazy
        :param _mode: tryb wywołania zapytania 'r' - odczyt, 'w' - zapis
        :type _mode: str
        :param _my_cursor: kursor zapytania do bazy
        :type _my_cursor: CMySQLCursor
        :param _my_result: wynik zapytania
        :type _my_result: list
        :return: zwraca wynik zapytania
        :rtype: list"""

        if _mode == 'r':
            _my_result = _my_cursor.fetchall()
        elif _mode == 'w':
            self.mydb.commit()
        return _my_result


if __name__ == '__main__':
    db = Database("10.10.100.99", "Oasis", "6CNkdnpCI3YxO30s", "iir")
    # db.connect()
    # db.disconnect()
    print(db.check_connection())

    sql = "INSERT INTO `Oasis_refresh` (`ID`, `Test`, `Cycle`, `Type_cycle`, `FLR`, `REG`, `FLT`, `FILL`, " \
          "`Data_start`, `Data_stop`, `Movie`, `Bottle`, `Water_spilled`, `Filter_wear`, `Buzzer`, `Flow_meter`, " \
          "`Pouring_time`, `Disturbance_bottle`, `Eva_error`, `error_info`) VALUES (NULL, '1', '1', 'aaa', '1.5', " \
          "'reg', '3.2', '11', '2022-07-27 00:00:00', CURRENT_TIMESTAMP, 'film.avi', '22', '4.2', '1.4', '1', '1', " \
          "'32', '0', '0', '-'); "
    db.connect()
    db.insert(sql)
    db.disconnect()
