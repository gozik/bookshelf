from app import db
from app.models.books import Book, Author, Identifier, Category, Link
from app.models.item import Item
from app.models.history import History


class UserInterface:
    # todo Add second side approval for transfer.
    # One should be able to decline command that did not happen in real life
    def __init__(self, user):
        self.user = user

    def add_volume_to_db(self, volume):
        if 'id' not in volume or 'volumeInfo' not in volume:
            raise KeyError

        if Book.query.filter_by(google_id=volume['id']).first():
            return 1  # google_id is in db already

        google_id = volume['id']
        book = Book(google_id=google_id)

        copy_list = ['title', 'subtitle', 'publisher', 'publishedDate', 'description']

        for field in copy_list:
            if field in volume['volumeInfo']:
                setattr(book, field, volume['volumeInfo'][field])

        if 'pageCount' in volume['volumeInfo']:
            book.page_count = volume['volumeInfo']['pageCount']

        if 'mainCategory' in volume['volumeInfo']:
            category = Category.query.filter_by(name=volume['volumeInfo']['mainCategory']).first()
            if not category:
                category = Category(name=volume['volumeInfo']['mainCategory'])
            book.main_category = category
        book.language = volume['volumeInfo']['language']

        if 'authors' in volume['volumeInfo']:
            for author_name in volume['volumeInfo']['authors']:
                author = Author.query.filter_by(fullname=author_name).first()
                if not author:
                    author = Author(fullname=author_name)
                book.authors.append(author)

        if 'industryIdentifiers' in volume['volumeInfo']:
            for ii in volume['volumeInfo']['industryIdentifiers']:
                book.industry_identifiers.append(Identifier(kind=ii['type'], data=ii['identifier']))

        if 'categories' in volume['volumeInfo']:
            for category_name in volume['volumeInfo']['categories']:
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                book.categories.append(category)

        if 'imageLinks' in volume['volumeInfo']:
            if 'thumbnail' in volume['volumeInfo']['imageLinks']:
                link = Link(kind='thumbnail', body=volume['volumeInfo']['imageLinks']['thumbnail'])
                book.image_links.append(link)

        db.session.add(book)
        db.session.commit()

    def add_book(self, title, subtitle, add_item=False):
        """ Add book (as description) to database """
        b = Book(title=title, subtitle=subtitle)
        db.session.add(b)
        db.session.commit()

        if add_item:
            self.new_item(Item(book=b))

    def new_item(self, item):
        """ Add item to your collection """
        item.owner = self.user
        item.controller = self.user
        history = History(command='add_item', user_to=self.user, item=item)
        db.session.add(item)
        db.session.add(history)
        db.session.commit()

    def take_item(self, item):
        """ Borrow item """
        user_from = item.controller
        item.controller = self.user
        history = History(command='take_item', item=item,
                          user_from=user_from, user_to=self.user)
        db.session.add(item)
        db.session.add(history)
        db.session.commit()

    def return_item(self, item):
        """ Return item to previous controller """
        # Возврат обычно производится на полку (откуда книга была взята),
        # таким образом некорректно говорить, что возврат будет обязательно владельцу
        # Дополнительно необходимо учесть вложенные передачи (неограниченной глубины):
        # A -> B -> C -> B (тут интерфейс должен знать, кому необходимо вернуть книгу) -> A
        last = (History.query
                .filter_by(item=item, user_to=self.user)
                .filter(History.command.in_(['take_item', 'give_item']))
                .order_by(History.id.desc())
                .first()
                )

        if not last:
            return 1  # no previous controller
        last_user_from = last.user_from
        item.controller = last_user_from
        history = History(command='return_item', item=item,
                          user_from=self.user, user_to=last_user_from)
        db.session.add(item)
        db.session.add(history)
        db.session.commit()

    def give_item(self, item, user_to):
        if item.controller != self.user:
            # you have to control item to be able to give it
            return 1

        user_from = self.user
        item.controller = user_to
        history = History(command='give_item', item=item,
                          user_from=user_from, user_to=self.user)
        db.session.add(item)
        db.session.add(history)
        db.session.commit()
