from flask_admin.contrib.sqla import ModelView
from flask import flash
from safrs import ValidationError
from sqlalchemy.orm.base import instance_state

from admin.admin_model_converter_ext import AdminModelConverterExt


class AdminViewExt(ModelView):
    """
         Quick example on adding additional SQLAlchemy types via AdminModelConverterExt
    """
    model_form_converter = AdminModelConverterExt

    def __init_(self, **kwargs):
        super().__init__(self, **kwargs)

    ''' def on_model_change(self, form, model, is_created):
        if is_created:
            model.id = '''

    """
         Enable SAFRSBase support Flask-admin does not create regular Instances
    """
    def build_new_instance(self):
        model = self._manager.new_instance()
        model.__init__()  # <-- Call SAFRSBase.__init__()
        state = instance_state(model)
        self._manager.dispatch.init(state, [], {})
        return model

    def handle_view_exception(self, exc):
        if isinstance(exc, ValidationError):
            flash(message=exc.message, category='error')
            return True

        return super(self).handle_view_exception(exc)
