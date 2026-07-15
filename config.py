import pymysql 
pymysql.install_as_MySQLdb()

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Test%4012345%23@localhost/student_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
