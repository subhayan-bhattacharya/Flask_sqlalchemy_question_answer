from project import app
from project.models.user_model import Users
from project.models.question_model import Questions
from flask import render_template,redirect,url_for,session,request
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import TextAreaField,SelectField
from werkzeug.security import generate_password_hash, check_password_hash

def get_experts():
    app.logger.debug("Inside get_experts function")
    experts = Users.get_experts()
    expertlist = []
    for expert in experts:
        t = (str(expert['id']), expert['name'])
        expertlist.append(t)
    return expertlist


@app.route('/ask',methods=["GET","POST"])
def ask():
    app.logger.info("Inside ask route")
    user_details = Users.get_current_user()

    class AskForm(FlaskForm):
        question = TextAreaField("Question",validators=[InputRequired()])
        expert = SelectField("Experts", choices=get_experts())

    askform = AskForm()

    if request.method == "POST":
        if askform.validate_on_submit():
            app.logger.debug("validation succeeded!")
            question = askform.question.data
            expert_id = askform.expert.data
            ask_by_id = user_details.id
            new_question = Questions(question_text=question,asked_by_id=ask_by_id,expert_id=expert_id)
            new_question.save_to_db()
            return redirect(url_for('index'))
        else:
            app.logger.error("Errors in validation %s",askform.errors)

    if user_details:
        app.logger.debug("User is logged in !")
        return render_template('ask.html',user=user_details,form=askform)
    else:
        app.logger.debug("User is not logged in !")
        return redirect(url_for('login'))



