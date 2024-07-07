from rest_framework.serializers import ValidationError
class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        result = value.get(self.field)
        if result and not result.startswith('http://www.youtube.com/'):
            raise ValidationError('Website is not ok')
