from App.extensions import db

class EconomicNews(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(256))
    content=db.Column(db.Text)
    link=db.Column(db.String(2048))
    publish_date=db.Column(db.DateTime)
    type=db.Column(db.String(256))
    keywords=db.Column(db.String(2048))
    create_date=db.Column(db.DateTime)
    create_by=db.Column(db.Integer)
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