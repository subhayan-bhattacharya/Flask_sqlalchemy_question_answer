from project import app
from project.models.user_model import Users
from project.models.question_model import Questions
from flask import render_template,redirect,url_for


@app.route('/unanswered')
def unanswered():
    user_details = Users.get_current_user()
    if user_details:
        if user_details.expert:
            app.logger.debug("Current user %s is an expert",user_details.name)
            unanswered_questions = Questions.get_unanswered_questions(user_details.id)
            return render_template('unanswered.html',user=user_details,questions=unanswered_questions)
        else:
            app.logger.debug("Current user %s is not an expert", user_details.name)
            return redirect(url_for('index'))
    else:
        app.logger.debug("User not logged in !")
        return redirect(url_for('login'))