<<<<<<< HEAD
import pymysql
pymysql.install_as_MySQLdb()

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Test%4012345%23@localhost/contact_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
=======
import pymysql 
pymysql.install_as_MySQLdb()

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Test%4012345%23@localhost/student_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
>>>>>>> 1c25ee110bd490b7b2298d3eb60cce8fef0bbeb2
