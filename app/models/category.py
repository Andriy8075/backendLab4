from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='categories')
    records = db.relationship('Record', back_populates='category', lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def create(name, user_id):
        category = Category(name=name, user_id=user_id)
        db.session.add(category)
        db.session.commit()
        return category
    
    @staticmethod
    def get_by_user_id(user_id):
        return Category.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_id(id):
        return Category.query.get(id)

    @staticmethod
    def delete(id):
        category = Category.query.get(id)
        if category is None:
            return False
        db.session.delete(category)
        db.session.commit()
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
        }
