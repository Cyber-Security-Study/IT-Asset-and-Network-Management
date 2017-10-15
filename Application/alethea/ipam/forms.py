from crispy_forms.bootstrap import InlineField, AppendedText, PrependedText
from crispy_forms.layout import Layout, Fieldset, Div, Field, MultiField, BaseInput, HTML, Button, Submit
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms_extensions.layouts import HorizontalField
from django.core.validators import validate_ipv4_address

# TODO: Needs more advanced validation to support IPv6 addresses, ideally mask_bits should have its limits adjusted
# depending if the address is v4 or v6
class SubnetForm(forms.Form):
    name = forms.CharField(label="Name", max_length=255)
    address = forms.CharField(label="IP Address", max_length=45, validators=[])
    mask_bits = forms.IntegerField(label="", min_value=0, max_value=128)

    def __init__(self, *args, **kwargs):
        super(SubnetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.is_horizontal = True
        self.helper.label_class = "col-md-2"
        self.helper.field_class = "col-md-8"
        self.helper.layout = Layout(
            HorizontalField("name"),
            Div(
                HTML(f"<label class=\"{self.helper.label_class} col-form-label\">IP Address*</label>"),
                Div(InlineField("address"), css_class="col-md-4"),
                Div(PrependedText("mask_bits", "/", label="", placeholder="Mask Bits"), css_class="col-md-4"),
                css_class="row"
            ),
            Submit("add", "Save Subnet")
        )

    # def is_valid(self):
    #     valid = super(SubnetForm, self).is_valid()
    #
    #     self.add_error("address", "Foobar")
    #     print(self._errors)
    #
    #     if not valid:
    #         return False
    #
    #     self.add_error("address", "Not a valid IP address")
    #     return False
    #
    #     return True
