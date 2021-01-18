from App.extensions import db
from App.utils.config_helper import get_config_map

config_map = get_config_map()

class Corp_score(db.Model):
    __table_args__ = {
        'schema': config_map['postgresql']['schema']
    }
    code = db.Column(db.String(255), primary_key=True)
    score = db.Column(db.String(2048))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
             del dict["_sa_instance_state"]
        return dict