from django.db.models import IntegerChoices


def create_choices_class(name, *choices, null=False, null_label='未知'):
    """Create a Choices class using list.
    
    Positional arguments:
        name: str, name of the created Choices class
        *choices: turple[name: str, lable: str], ...
    Keyword arguments:
        null: bool, determine whether to add a choic for null.
              default to False;
        null_lable: str, the lable of null choice. Only work
                    work when null=True. Default to '未知'
    Return an IntergerChoices named 'name'.
    eg:
        >>> Gender = create_choices_class(
        ...    'Gender', ('FEMALE', '女'),
        ...    ('MALE', '男'), null=True,
        ...    )
        >>> Gender.choices
        [(None, '未知'), (0, '女'), (1, '男')]
    """
    use_bool = len(choices) == 2
    start = int(not use_bool)

    members = []
    for choice in choices:
        key, label = choice
        members.append((key, (start, label)))
        start += 1
    
    klass = IntegerChoices(name, members)

    if null:
        klass.__empty__ = null_label

    return klass