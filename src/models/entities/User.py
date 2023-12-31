from werkzeug.security import check_password_hash , generate_password_hash
from flask_login import UserMixin

class User(UserMixin):

# clase identica a la bd, es para mapear los objetos de la bd
    def __init__ (self , id, email, password, role="user") -> None:
        self.id = id
        self.email = email
        self.password = password
        self.role = role

    @classmethod # no hace falta instanciar clase para usar metodo
    def check_password (self , hashed_password, password):
        return check_password_hash(hashed_password,password)
    
    @classmethod # no hace falta instanciar clase para usar metodo
    def hash_password (self , inputPassword):
        return generate_password_hash(inputPassword)
    