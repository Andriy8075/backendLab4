from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    default_currency = db.Column(db.String(3), nullable=False)

    categories = db.relationship('Category', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def create(data: dict):
        password_hash = generate_password_hash(data['password'])
        user = User(name=data['name'], password=password_hash, default_currency=data['default_currency'])
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        user = User.query.get(id)
        if user is None:
            return None
        return user.to_dict()

    @staticmethod
    def delete(id):
        user = User.query.get(id)
        if user is None:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'default_currency': self.default_currency,
        }

    def check_password(self, password: str) -> bool:
        print(password)
        print(self.password)
        print(check_password_hash(self.password, password))
        return check_password_hash(self.password, password)
