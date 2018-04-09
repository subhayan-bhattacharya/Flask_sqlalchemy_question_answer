from project import app
from project.models.user_model import Users
from project.models.question_model import Questions
from flask import render_template,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Length
from wtforms import StringField,PasswordField
from werkzeug.security import generate_password_hash, check_password_hash

class RegisterForm(FlaskForm):
    username = StringField("Name",validators=[InputRequired(),Length(max=20)])
    password = PasswordField("Password",validators=[InputRequired(),Length(max=20)])

@app.route('/register',methods=["GET","POST"])
def register():
    user_details = Users.get_current_user()
    error_message = None
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        app.logger.debug("Register form validated successfully !")
        username = registerform.username.data
        password = registerform.password.data
        app.logger.debug("User %s is wanting to be registered",username)
        existing_user = Users.get_by_name(name=username)
        if not existing_user:
            hashed_password = generate_password_hash(password,method='sha256')
            new_user = Users(name=username,password=hashed_password,expert=False,admin=False)
            if username == 'admin':
                new_user.admin = True
            new_user.save_to_db()
            session['username'] = username
            app.logger.debug("Adding %s to session variable",username)
            return redirect(url_for('index'))
        else:
            error_message = "User already exists!"
            app.logger.debug("%s already exists in the database",username)

    return render_template('register.html',user=user_details,error=error_message,form=registerform)