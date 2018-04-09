from project import app
from project.models.user_model import Users
from project.models.question_model import Questions
from flask import render_template,redirect,url_for


@app.route('/question/<question_id>')
def question(question_id):
    app.logger.debug("Retrieving information about question : %s",str(question_id))
    user_details = Users.get_current_user()
    details = Questions.view_question_details(question_id)
    return render_template('question.html',user=user_details,details=details)