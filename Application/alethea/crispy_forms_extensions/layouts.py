from crispy_forms.layout import Field


# Bit of a bodge - Crispy forms doesn't support Bootstrap 4's horizontal forms so this rectifies that, hopefully can
# remove this one crispy forms is updated to support them
class HorizontalField(Field):
    def __init__(self, field_name, *args, **kwargs):
        super(HorizontalField, self).__init__(Field(field_name,
                                                    template="fields/horizontalfield.html", *args, **kwargs))
