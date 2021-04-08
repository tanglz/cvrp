import mysql.connector
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqlconnector://lisa:123456@localhost:3306/cvrp')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    #import yourapplication.models
    Base.metadata.create_all(bind=engine)

# if __name__ == '__main__':
#     mydb = mysql.connector.connect(
#         host="localhost",
#         port=3306,
#         user="lisa",
#         password="123456",
#         database="cvrp"
#     )
#     mycursor = mydb.cursor()

    # mycursor.execute("CREATE DATABASE cvrp")

    # mycursor.execute("CREATE TABLE task (id INT AUTO_INCREMENT PRIMARY KEY, dataset VARCHAR(255), MAX_NFC INT, "
    #                  "ants INT, status TINYINT(1))")
