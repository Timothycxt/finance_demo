from App.extensions import db
from App.utils.config_helper import get_config_map

config_map = get_config_map()

class CorpInfo(db.Model):
    __table_args__ = {
        'schema': config_map['postgresql']['schema']
    }
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256))
    name = db.Column(db.String(256))
    legal_person = db.Column(db.String(256))
    regist_capital = db.Column(db.String(256))
    industry = db.Column(db.String(256))
    type = db.Column(db.String(256))
    admin_div = db.Column(db.String(256))
    establish_date = db.Column(db.DateTime)
    business_scope = db.Column(db.Text)
    member = db.Column(db.Text)
    create_date = db.Column(db.DateTime)
    create_by = db.Column(db.Integer)
    update_date = db.Column(db.DateTime)
    update_by = db.Column(db.DateTime)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
             del dict["_sa_instance_state"]
        return dict