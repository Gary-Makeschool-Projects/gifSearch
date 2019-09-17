# from gifSearch import db


# class Country(db.Model):
#     __tablename__ = 'countries'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(60), unique=True, nullable=False)
#     iso = db.Column(db.String(3), unique=True, nullable=False)

#     def __repr__(self):

#         return '{} - {}'.format(self.iso, self.name)

#     def as_dict(self):
#         return {'name': self.name}
