from enum import EnumMeta
from typing import List, Any

from flask_admin.contrib.sqla.form import AdminModelConverter, choice_type_coerce_factory
from flask_admin.model.form import converts
from flask_admin import form
from wtforms import validators


class AdminModelConverterExt(AdminModelConverter):
    """
           Quick example on adding additional supported  types
    """
    def __init__(self, session, view):
        #  print("custom admin converter")
        super().__init__(session, view)

    def get_form(self, **kwargs):
        super().get_form(**kwargs)

    @converts('models.types.choice_ext.ChoiceType')
    def convert_choice_type_ext(self, column, field_args, **extra):
        available_choices: List[Any] = []
        # choices can either be specified as an enum, or as a list of tuples
        if isinstance(column.type.choices, EnumMeta):
            available_choices = [(f.value, f.name) for f in column.type.choices]
        else:
            available_choices = column.type.choices
        accepted_values = [key for key, val in available_choices]

        if column.nullable:
            field_args['allow_blank'] = column.nullable
            accepted_values.append(None)
            filters = field_args.get('filters', [])
            filters.append(lambda x: x or None)
            field_args['filters'] = filters

        field_args['choices'] = available_choices
        field_args['validators'].append(validators.AnyOf(accepted_values))
        field_args['coerce'] = choice_type_coerce_factory(column.type)
        return form.Select2Field(**field_args)

    @converts('models.types.email_type.EmailType')
    def conv_email_type(self, column, field_args, **extra):
        return super().conv_String(column, field_args, **extra)
