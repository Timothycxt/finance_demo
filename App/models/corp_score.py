from App.extensions import db

class Corp_score(db.Model):
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