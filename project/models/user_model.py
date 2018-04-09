from project import db
from flask import session

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(20),nullable=False)
    expert = db.Column(db.Boolean,nullable=False)
    admin = db.Column(db.Boolean,nullable=False)


    @classmethod
    def get_by_name(cls,name):
        user = None
        user = cls.query.filter_by(name=name).first()
        return user

    @classmethod
    def get_by_id(cls,id):
        user = None
        user = cls.query.filter_by(id=id).first()
        return user

    @classmethod
    def get_experts(cls):
        experts = []
        for expert in cls.query.filter(cls.expert == True).all():
            temp = {}
            temp['id'] = expert.id
            temp['name'] = expert.name
            experts.append(temp)
        return experts

    @classmethod
    def get_all_nonadmin_users(cls):
        users = []
        users = cls.query.filter_by(admin=False).all()
        return users

    @classmethod
    def get_current_user(cls):
        user_result = None
        if 'username' in session:
            user = session['username']
            user_result = cls.get_by_name(name=user)
        return user_result

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
