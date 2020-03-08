from app import db

writen_by = db.Table('writen_by',
                     db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                     db.Column('author_id', db.Integer, db.ForeignKey('authors.id'))
                     )

book_category = db.Table('book_category',
                         db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                         db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
                         )

book_image_link = db.Table('book_image_link',
                           db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                           db.Column('link_id', db.Integer, db.ForeignKey('links.id'))
                           )


class Book(db.Model):
    """
        A Book represents information about a book or a magazine.
        It contains metadata, such as title and author.
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(240))
    subtitle = db.Column(db.String(240))

    authors = db.relationship('Author', secondary='writen_by')

    publisher = db.Column(db.String(64))

    publishedDate = db.Column(db.String(64))

    description = db.Column(db.Text)

    industry_identifiers = db.relationship('Identifier',
                                           backref='book')
    page_count = db.Column(db.Integer)

    main_category_id = db.Column(db.Integer,
                                 db.ForeignKey('categories.id'))
    main_category = db.relationship('Category')
    categories = db.relationship('Category',
                                 secondary='book_category')
    image_links = db.relationship('Link',
                                  secondary='book_image_link')
    language = db.Column(db.String(32))

    def __str__(self):
        return self.title

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(240))

    def __str__(self):
        return self.fullname


class Identifier(db.Model):
    __tablename__ = 'identifiers'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    kind = db.Column(db.String(32))
    data = db.Column(db.String(240))

    def __str__(self):
        return self.data


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)

    kind = db.Column(db.String(32))
    body = db.Column(db.Text)
