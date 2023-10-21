from flask import Flask , render_template , request , redirect , url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect  # para que formulario de login tenga codigo token para csrf
from flask_login import LoginManager , login_user, logout_user, login_required
from flask_mail import Mail , Message


from config import config

from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)
db = MySQL(app) 
login_manager_app = LoginManager(app)
csrf = CSRFProtect()  # para que formulario de login tenga codigo token para csrf
mail = Mail()

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db , id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':      
        if request.form['password'] == request.form['password-confirm']:            
            user = User( 0 , request.form['email'] , request.form['password'] )
            registerUser = ModelUser.register(db, user)
            if registerUser:                 
                login_user(user)
                flash("Usuario registrado y logueado")

                msg = Message('Nuevo registro',
                               sender = app.config['MAIL_USERNAME'],
                               recipients= [user.email])
                
                msg.html = render_template('email.html' , userEmail = user.email)

                mail.send(msg)

                return redirect(url_for('home'))
            else:                
                flash("Email ya existe, intenta logueandote")
                return render_template('auth/login.html')
        else:            
            flash("Passwords no coinciden!")
            return render_template('auth/register.html')
    else:
        return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        user = User( 0 , request.form['email'], request.form['password'])
        loguedUser = ModelUser.login(db, user)

        if loguedUser != None:
            if loguedUser.password:
                login_user(loguedUser)
                return redirect(url_for('home'))
            else:
                flash("Credenciales erroneas")
                return render_template('auth/login.html')
        else:
            flash("Credenciales erroneas")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
        return render_template('home.html')

@app.route('/protected')
@login_required
def protected():
        return "<h1>SOY UN CONTENIDO SOLO PARA AUTHENTICADOS <h1/>"

def status_401(error):
     return redirect(url_for('login'))

def status_404(error):
     return "<h1> Pagina no encontrada! <h1/>",404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app) # para que formulario de login tenga codigo token para csrf
    mail.init_app(app)
    app.register_error_handler(401 , status_401)
    app.register_error_handler(404 , status_404)
    app.run()