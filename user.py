from database import CursorFromConnectionFromPool
import datetime

class User:
    def __init__(self, email, firstname, lastname, oauth_token, oauth_token_secret, id):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.id = id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def __repr__(self):
        return "User: {}".format(self.email)

    def save_to_db(self):
        # 1st way
        # connection = psycopg2.connect(dbname="learning", user="postgres", password="P@ssw0rd",host="localhost")
        # with connection.cursor() as cursor:
        #     cursor.execute(" INSERT INTO USERS (email, firstname, lastname) values (%s, %s, %s)",
        #                    (self.email, self.firstname, self.lastname));
        # connection.commit()
        # connection.close()
        # - 2nd way without explicitly denote connection.commit and connection.close
        # >> with connection_pool.getconn() as connection:
        # - 3rd way if there's connection pool setting makes sure the connection doesn't hold, make sure it gets released back.
        # >> Hence, must use command to put back the pool
        # >> connection = connection_pool.getconn()
        # - 4th way create a class and access the method via default "enter" hence the enter method must return
        # >> the connection pool object. this way there's no need to explicit declare conn.commit, conn.close
        # >> but this causes a lot of overhead
        # with ConnectionFromPool() as connection:
        #     with connection.cursor() as cursor:
        #         cursor.execute(" INSERT INTO USERS (email, firstname, lastname) "
        #                        " values (%s, %s, %s)",
        #                    (self.email, self.firstname, self.lastname))
            # connection_pool.putconn(connection) no longer needed if it's connection pool
        with CursorFromConnectionFromPool() as cursor: # this bundled w cursor and connection
            cursor.execute(" INSERT INTO USERS "
                           " (email, firstname, lastname, oauth_token, oauth_toket_secret) "
                            " values (%s, %s, %s, %s, %s)",
                            (self.email, self.firstname, self.lastname, self.oauth_token, self.oauth_token_secret))


    @classmethod
    def load_email_from_db(cls, email):
        # with connection_pool.getconn() as connection:
        # connection = connection_pool.getconn()
        # with ConnectionFromPool() as connection:
          #  with connection.cursor() as cursor:
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(" select * from users where email=%s", (email,))
            user_data = cursor.fetchone()
            return cls(email=user_data[1], firstname=user_data[2], lastname=user_data[3], oauth_token=user_data[4], oauth_token_secret=[5], id=user_data[0])
