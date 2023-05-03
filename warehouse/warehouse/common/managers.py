from django.db.models import Manager


class SafeGetManager(Manager):
    def safe_get(self, pk, model):
        try:
            _object = self.get(id=pk)
        except model.DoesNotExist:
            _object = None

        return _object
