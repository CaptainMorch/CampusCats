from django.forms import TextInput

class DefaultListFieldWidget(TextInput):
    template_name = 'listfield/widgets/default_listfield.html'

    class Media:
        js = [
            'listfield/js/default_listfield.js',
        ]
        css = {
            'all': ('listfield/css/default_listfield.css',),
        }

    def __init__(self, sep=None, **kwargs):
        # 'sep' should be explictly set when init, except being
        # initialized by formfield 'ListField' (automatically set latter)
        self.sep = sep
        super().__init__(**kwargs)

    def format_value(self, value):
        """format python list object back into string"""
        if not value:
            return ""
        else:
            return '{sep}{strings}{sep}'.format(
                    sep=self.sep,
                    strings=self.sep.join(value)
                    )