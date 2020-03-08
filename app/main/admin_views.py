from flask import redirect, url_for, flash
from flask_admin.base import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import db, admin
from app.models.auth import User
from app.models.books import Book, Author, Category, Identifier, Link
from app.models.history import History
from app.models.item import Item


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated \
               and current_user.role and current_user.role.name == "Admin"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("You need to be an admin to view this page.")
        return redirect(url_for('main.index'))

    can_export = True
    export_types = ['csv']
    static_folder = 'static'


class UserAdmin(AdminModelView):
    column_list = ['username', 'email', 'role']
    form_columns = ['username', 'email', 'role']
    column_editable_list = ['email', 'role', ]
    column_searchable_list = ['username', 'email', 'role.name', ]


admin.add_view(UserAdmin(User, db.session))
admin.add_view(AdminModelView(Book, db.session, category='Books'))
admin.add_view(AdminModelView(Author, db.session, category='Books'))
admin.add_view(AdminModelView(Category, db.session, category='Books'))
admin.add_view(AdminModelView(Identifier, db.session, category='Books'))
admin.add_view(AdminModelView(Link, db.session, category='Books'))
admin.add_view(AdminModelView(Item, db.session, category='BookItems'))
admin.add_view(AdminModelView(History, db.session, category='BookItems'))
admin.add_link(MenuLink(name='Exit Admin', url='/'))
