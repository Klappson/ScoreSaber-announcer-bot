import psycopg2
import config as cfg


global db_connection


def init_connection() -> bool:
    try:
        global db_connection
        conn_str = (
                "host=" + cfg.db_connection["ip"] + " " +
                "port=" + cfg.db_connection["port"] + " " +
                "user=" + cfg.db_connection["username"] + " " +
                "password=" + cfg.db_connection["passwort"] + " " +
                "dbname=" + cfg.db_connection["dbname"]
            )
        db_connection = DbConnection(psycopg2.connect(conn_str))
        return True
    except Exception as r:
        raise r


class DbConnection:
    """
    Some SQL-Methods that would be the same everytime, so it makes sense
    to put them in a seperate class
    """
    def __init__(self, db_conn):
        self.dbcon = db_conn

    # Checks if a primary-key exists.
    def does_pkey_exist(self, table_name, pkey_name, pkey_val):
        c = self.dbcon.cursor()
        c.execute(
            " SELECT "+str(pkey_name) +
            " FROM "+str(table_name) +
            " WHERE "+str(pkey_name)+" = '"+str(pkey_val)+"'"
        )
        try:
            if c.fetchone() is not None:
                return True
            else:
                return False
        except psycopg2.ProgrammingError:
            return False

    # Send a Statement to Database
    def send_statm(self, statms):
        c = self.dbcon.cursor()
        print("Executing SQL-Statemend \n" + statms + "\n")
        c.execute(statms)
        c.close()
        self.dbcon.commit()

    # Send a querrie to Database
    def get_data(self, querry) -> list:
        try:
            c = self.dbcon.cursor()
            c.execute(querry)
            retu = c.fetchall()
            c.close()
            print("Executing SQL-Querie \n"+querry+"\n")
            self.dbcon.commit()
            return retu
        except psycopg2.ProgrammingError:
            return []


def get() -> DbConnection:
    global db_connection
    return db_connection
