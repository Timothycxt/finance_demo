from App.extensions import db


class CorpNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    link = db.Column(db.String(1024))
    publish_date = db.Column(db.DateTime)
    type = db.Column(db.String(255))
    corporation = db.Column(db.String(2048))
    person = db.Column(db.String(2048))
    keywords = db.Column(db.String(2048))
    keywords_value = db.Column(db.String(255))
    emotion_trend = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    create_by = db.Column(db.Integer)
    update_date = db.Column(db.DateTime)
    update_by = db.Column(db.Integer)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
