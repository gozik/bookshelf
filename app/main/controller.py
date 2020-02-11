from app import db
from app.models.history import History


class UserInterface:
    # todo Add second side approval for transfer.
    # One should be able to decline command that did not happen in real life
    def __init__(self, user):
        self.user = user

    def add_book(self, book, add_hardcopy=False):
        """ Add book (as description) to database """
        pass

    def new_item(self, item):
        """ Add hardcopy to your collection """
        item.owner = self.user
        item.controller = self.user
        history = History(command='add_hardcopy', user_to=self.user, item=item)
        db.session.add(item)
        db.session.add(history)
        db.session.commit()

    def take_item(self, item):
        """ Borrow hardcopy """
        user_from = item.controller
        item.controller = self.user
        history = History(command='take_hardcopy', item=item,
                          user_from=user_from, user_to=self.user)
        db.session.add(item)
        db.session.add(history)
        db.session.commit()

    def return_item(self, item):
        """ Return hardcopy to previous controller """
        # Возврат обычно производится на полку (откуда книга была взята),
        # таким образом некорректно говорить, что возврат будет обязательно владельцу
        # Дополнительно необходимо учесть вложенные передачи (неограниченной глубины):
        # A -> B -> C -> B (тут интерфейс должен знать, кому необходимо вернуть книгу) -> A
        last_user_from = (History.query
                            .filter_by(item=item, user_to=self.user,
                                       command='take_hardcopy')
                            .order_by(History.id.desc())
                            .first()
                     ).user_from
        # add give hardcopy as option for command
        item.controller = last_user_from
        history = History(command='return_hardcopy', item=item,
                          user_from=self.user, user_to=last_user_from)
        db.session.add(item)
        db.session.add(history)
        db.session.commit()

    def give_item(self, item, user_to):
        if item.controller != self.user:
            # you have to controll hardcopy to be able to give it
            return 1

        user_from = self.user
        item.controller = user_to
        history = History(command='give_hardcopy', item=item,
                          user_from=user_from, user_to=self.user)
        db.session.add(item)
        db.session.add(history)
        db.session.commit()
