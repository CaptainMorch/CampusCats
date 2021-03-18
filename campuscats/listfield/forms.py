from django.forms import CharField
from django.contrib.admin.widgets import AdminTextInputWidget
from .widgets import DefaultListFieldWidget


class ListFieldFormField(CharField):
    widget = DefaultListFieldWidget

    def __init__(self, *, sep=None, **kwargs):
        self.sep = sep

        # Modelfield ListField inherits from CharField, so even if we
        # had set a default widget, ModelAdmin simply ignores it and
        # try using this guy. So here we throw it away.
        # See: django.contrib.admin.options.BaseModelAdmin.formfield_for_dbfield
        if kwargs['widget'] == AdminTextInputWidget:
            kwargs.pop('widget')
        super().__init__(**kwargs)
        self.widget.sep = self.sep

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['data-sep'] = self.sep
        return attrs