from App.extensions import db
from App.utils.config_helper import get_config_map

config_map = get_config_map()

class CorpNews(db.Model):
    __table_args__ = {
        'schema': config_map['postgresql']['schema']
    }
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(256))
    content=db.Column(db.Text)
    link=db.Column(db.String(2048))
    publish_date=db.Column(db.DateTime)
    type=db.Column(db.String(256))
    corporation=db.Column(db.String(2048))
    person=db.Column(db.String(2048))
    keywords=db.Column(db.String(2048))
    create_date=db.Column(db.DateTime)
    create_by=db.Column(db.Integer)
    update_date = db.Column(db.DateTime)
    update_by = db.Column(db.DateTime)
    emotion_trend=db.Column(db.String(1024))  # 新闻情感倾向

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
             del dict["_sa_instance_state"]
        return dict