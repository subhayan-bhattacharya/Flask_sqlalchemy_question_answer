from project import app
from project.models.user_model import Users
from project.models.question_model import Questions
from flask import render_template,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import TextAreaField
from werkzeug.security import generate_password_hash, check_password_hash


class AnswerForm(FlaskForm):
    answer = TextAreaField("Answer",validators=[InputRequired()])

@app.route('/answer/<question_id>',methods=["GET","POST"])
def answer(question_id):
    app.logger.info("Inside answer route with question id : %s \n",str(question_id))
    user_details = Users.get_current_user()
    answerform = AnswerForm()

    if answerform.validate_on_submit():
        app.logger.debug("Answer form validated \n")
        answer = answerform.answer.data
        question = Questions.get_question_details(question_id=question_id)
        question.answer_text = answer
        question.save_to_db()
        return redirect(url_for('unanswered'))

    if user_details:
        app.logger.debug("User %s logged in !",user_details.name)
        if user_details.expert:
            app.logger.debug("user %s is an expert",user_details.name)
            question = Questions.get_question_details(question_id=question_id)
            return render_template('answer.html',user=user_details,question=question,form=answerform)
        else:
            app.logger.debug("user %s is not an expert", user_details.name)
            return redirect(url_for('index'))
    else:
        app.logger.debug("User not logged in!")
        return redirect(url_for('login'))