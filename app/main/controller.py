from app import db
from app.models.books import Book
from app.models.item import Item
from app.models.history import History


class UserInterface:
    # todo Add second side approval for transfer.
    # One should be able to decline command that did not happen in real life
    def __init__(self, user):
        self.user = user

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
            return 1 # no previous controller
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
