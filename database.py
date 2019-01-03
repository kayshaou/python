from psycopg2 import pool
import psycopg2

class Database:

    ___connection_pool = None

    # **kwargs - any number of name parameters
    @staticmethod
    def initialise(**kwargs):
        Database.___connection_pool = pool.SimpleConnectionPool(
                                            1,  # minConnection if no conn avail we gonna connect one.
                                            10,  # maxConnection
                                            **kwargs)
    @classmethod
    def get_connection(cls):
        return cls.___connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        cls.___connection_pool.putconn(connection)

    @classmethod
    def close_all_connection(cls):
        cls.___connection_pool.closeall()

# format code use alt+ctrl L

# 1st way
# def connect():
#     # establish connection to postgres
#     return psycopg2.connect(dbname="learning", user="postgres", password="P@ssw0rd",host="localhost")
# 2nd way
# connection pool
# connection_pool = pool.SimpleConnectionPool(1,  # minConnection if no conn avail we gonna connect one.
#                                             10,  # maxConnection
#                                             dbname="learning",
#                                             user="postgres",
#                                             password="P@ssw0rd",
#                                             host="localhost")


# 3rd way
# class ConnectionPool:
#     # sequence of invocation - init > enter > exit (get called at the end of with clause)
#     def __init__(self):
#         self.connection_pool = pool.SimpleConnectionPool(1,  # minConnection if no conn avail we gonna connect one.
#                                                          1,  # maxConnection
#                                                          dbname="learning",
#                                                          user="postgres",
#                                                          password="P@ssw0rd",
#                                                          host="localhost")
#     #enter the class
#     def __enter__(self):
#         return self.connection_pool.getconn();
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass
#

#4th way
# >> declare the pool properties globally. so we can obtain and release the connection from the pool via init>enter>exit
# class ConnectionFromPool:
#     # initially set connection var to none
#     def __init__(self):
#         self.connection = None;
#
#     #now assign connection
#     def __enter__(self):
#         self.connection = connection_pool.getconn()
#         return self.connection
#
#     #remember to release
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.connection.commit()
#         connection_pool.putconn(self.connection)


#5th way adding in cursor
class CursorFromConnectionFromPool:
    #initialize both connection and cursor
    def __init__(self):
        self.connection = None;
        self.cursor = None;

    #now assign connection & cursor
    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    #remember to release
    #def __exit__(self, exc_type, exc_val, exc_tb):
    def __exit__(self, exception_type, exception_value, exception_traceback):
        # if there's error rollback the connection
        if exception_value is not None:
            self.cursor.rollback()
        else: # else close cursor and commit!
            self.cursor.close()
            self.connection.commit()
            Database.return_connection(self.connection)
