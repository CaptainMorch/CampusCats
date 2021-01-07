from django.db.models.lookups import PatternLookup, Contains, IContains
from django.db.models import Value
from django.db.models.functions import Concat


# Define custom lookups. Registered in ./apps.py

# Builtin lookups rely on their 'lookup_name' to work, which must
# be changed if we subclass them. So wrap these lookups instead.
#
# Subclass PatternLookup to pretend we are a real lookup
class LookupWrapper(PatternLookup):
    wrapped_lookup_class = None

    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)
        # make modifications to the rhs
        sep = self.lhs.output_field.sep
        if hasattr(self.rhs, 'resolve_expression'):
            sep = Value(sep)
            self.rhs = Concat(sep, self.rhs, sep)
        else:
            self.rhs = f'{sep}{self.rhs!s}{sep}'
        # use modified args to initialize wrapped lookup
        # pylint: disable=not-callable
        self.wrapped_lookup = self.wrapped_lookup_class(self.lhs, self.rhs)

    def as_sql(self, compiler, connection):
        return self.wrapped_lookup.as_sql(compiler, connection)


class Has(LookupWrapper):
    lookup_name = 'lf_has'
    wrapped_lookup_class = Contains


class IHas(LookupWrapper):
    lookup_name = 'lf_ihas'
    wrapped_lookup_class = IContains