# ListField Application
This application provides a field, and several tools for that field, 
including two lookups, a form-field, a widget, and some DJRF stuff.

## Field
`listfield.fields.ListField`

A single field to store a list of strings.

Inherits all args from `django.db.models.CharField` (So you
must provide 'max_length' to the field)

Additional kwargs:

`sep`: default to ','. A single non-alphabetic character to use as the
separator under the hood. Must not appear in the strings to store.

## FormField
`listfield.forms.ListFieldFormField`

A simple default formfield for ListField. 

## Widget
`listfield.widgets.DefaultListFieldWidget`

A widget mainly for django admin site, simple but works.

## Lookups
Lookup names are prefixed with `lf`(i.e. listfield) to avoid clashes.
### lf_has
Apply only to ListField. Look for those who has EXACTLY 
the righthand-side value as one of its elements.

e.g. `Model.objects.filter(listfield__lf_has='Element')` will search
for objects of Model, whose 'listfield' has an element 'Element'

NOTE: if you apply a bilateral transform on either side, make sure
that transform don't have effcts on the separater of your
ListField instance!

### lf_ihas
Case-insensitive version of `if_has`.

## DJRF Specific
For django-rest-framework. Consists of a serializer field and a mixin.

### Serializer Field
`listfield.serializers.ListField`

Corresponding field for rest_framework.serializers.

Must explictly pass 'sep' to it even when default is used.

Usage:
```python
class MySerializer(Serializer):
    lf = listfield.serialzers.ListField(sep=',', max_length=16)
    ... ...
```

### Serializer Mixin
`listfield.serializers.AllowListFieldMixin`

Mix this into rest_framework.serializers.ModelSerializer or 
it's subclass to enable them to automatically handle ListField,
then you could just include your ListField in Meta.fields like other
standard fields.