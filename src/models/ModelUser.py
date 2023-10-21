from models.entities.User import User
from flask_mysqldb import MySQL


class ModelUser():

    @classmethod
    def register(self , db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO user (`email`, `password` , `role`)
                        VALUES (%s, %s, %s)"""
            if user.email == "admin@admin.com" :
                user.role = "admin"
            cursor.execute(sql, (user.email, User.hash_password(user.password), user.role))
            db.connection.commit()            
            return True
        except Exception as ex:
            if ex.args[0] == 1062:
                return False
            return str(ex)


    @classmethod
    def login(self , db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, email, password , role FROM user 
                        WHERE email = '{}'""".format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                validPassword = User.check_password(row[2] , user.password)
                return User(row[0], row[1] , validPassword, row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self , db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, email, role FROM user 
                        WHERE id = '{}'""".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                return User(row[0], row[1] , None, row[2])
            else:
                return None

        except Exception as ex:
            raise Exception(ex)