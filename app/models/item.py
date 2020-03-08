from app import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('Book')

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', foreign_keys=[owner_id], backref='own_items')

    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    controller = db.relationship('User', foreign_keys=[controller_id],
                                 backref='controlled_items')
    # При создании новой полки создавать нового пользователя.
    # (Добавить тип пользователя: полка)
    # Бот ассоциирует себя с данной полкой и отвечает о том какие книги у него сейчас есть
