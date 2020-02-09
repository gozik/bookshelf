class UserInterface:
    def __init__(self):
        pass

    def add_book(self, book, add_hardcopy=False):
        """ Add book (as description) to database """
        pass

    def add_hardcopy(self):
        """ Add hardcopy to your collection """
        pass

    def take_hardcopy(self, hardcopy):
        """ Borrow hardcopy """
        pass

    def return_hardcopy(self, hardcopy):
        """ Return hardcopy to previous controller """
        # Возврат обычно производится на полку (откуда книга была взята),
        # таким образом некорректно говорить, что возврат будет обязательно владельцу
        pass
