# user
from exts import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


class User(BaseModel):
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(200), default='upload/mine.png')

    books = db.relationship('Book', backref='users', secondary='cart')

    def __str__(self):
        return self.username


# book
class Book(BaseModel):
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(15), nullable=False)
    desc = db.Column(db.String(256), nullable=False)

    def __str__(self):
        return self.title


# cart
class Cart(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    bookid = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    numbers = db.Column(db.Integer, default=1)
