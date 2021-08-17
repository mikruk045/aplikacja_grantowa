#podawanie danych pobieranych z kursora jako słowników
def rows_as_dicts(cursor):
    col_names = [i[0] for i in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor]
