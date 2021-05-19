class AssertSerializerValidationMixin:
    """Provides an asserting method for validation errors raised by serializers"""
    def assertValidationErrorCodes(self, errors, codes):
        """Assert errors (raised by Serializer) are exactly your \
        expected ones in code form.

        Providing codes in both ways are identical:
            {'single-error-field': 'code'}
            {'single-error-field': ['code']}
        """
        for field, field_errors in errors.items():
            self.assertIn(
                field, codes, 
                '\nUnexpected errors in field "{0}": {1}'.format(
                    field, ', '.join(field_errors)
                ))

            field_error_codes = [err.code for err in field_errors]
            field_expected_codes = codes.pop(field)
            if not isinstance(field_expected_codes, (list, tuple)):
                field_expected_codes = [field_expected_codes]

            self.assertCountEqual(
                field_expected_codes, field_error_codes,
                "\nField '{0}' didn't run as expected.\n"\
                "Expected error codes: {1}\n"\
                "Raised error codes: {2}".format(
                    field,
                    ', '.join(field_expected_codes),
                    ', '.join(field_error_codes),
                    )
                )
        # check for remaining codes
        self.assertFalse(
            codes,
            "\nThe following fields didn't report any errors: {}".format(
                ', '.join(codes.keys())
            ))