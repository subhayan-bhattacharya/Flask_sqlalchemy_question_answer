from project import app
from project.models.user_model import Users
from project.models.question_model import Questions
from flask import render_template,redirect,url_for


@app.route('/')
def index():
    app.logger.debug("Inside index route")
    user_details = Users.get_current_user()
    results = Questions.get_all_answered_questions_details()
    app.logger.debug("Exiting index route")
    return render_template('home.html',user=user_details,results=results)

