import re
from flask_restx.fields import StringMixin, Raw, MarshallingError


class Regex(StringMixin, Raw):
    def __init__(self, *args, pattern, **kwargs):
        self._pattern = pattern
        super().__init__(*args, **kwargs)

    def format(self, value):
        if re.match(self._pattern, value):
            return value
        else:
            raise MarshallingError(f"Value does not match pattern: '{self._pattern}'")

    def schema(self):
        schema = super().schema()
        schema["pattern"] = self._pattern
        return schema