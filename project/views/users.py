from project import app
from project.models.user_model import Users
from project.models.question_model import Questions
from flask import render_template,redirect,url_for


@app.route('/users')
def users():
    user_details = Users.get_current_user()
    if user_details:
        if user_details.admin:
            app.logger.debug('Current user %s is an admin',user_details.name)
            user = Users.get_all_nonadmin_users()
            return render_template('users.html',user=user_details,users=user)
        else:
            app.logger.debug('Current user %s is not an admin', user_details.name)
            return redirect(url_for('index'))
    else:
        app.logger.debug('User not signed in !')
        return redirect(url_for('login'))

@app.route('/promote/<user_id>')
def promote(user_id):
    app.logger.debug("Attempting to promote/demote user with id : %s",str(user_id))
    user_details = Users.get_current_user()
    if user_details:
        if user_details.admin:
            app.logger.debug('Current user %s is an admin', user_details.name)
            user_details = Users.get_by_id(user_id)
            if user_details.expert:
                app.logger.debug('%s is an expert user',user_details.name)
                user_details.expert = False
            else:
                app.logger.debug('%s is not an expert user', user_details.name)
                user_details.expert = True
            user_details.save_to_db()
            return redirect(url_for('users'))
        else:
            app.logger.debug('Current user %s is not an admin', user_details.name)
            return redirect(url_for('index'))
    else:
        app.logger.debug('User not signed in !')
        return redirect(url_for('login'))
