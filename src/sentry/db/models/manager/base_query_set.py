from django.db.models import QuerySet


class BaseQuerySet(QuerySet):
    # XXX(dcramer): we prefer values_list, but we can't disable values as Django uses it
    # internally
    # def values(self, *args, **kwargs):
    #     raise NotImplementedError('Use ``values_list`` instead [performance].')

    def defer(self, *args, **kwargs):
        raise NotImplementedError("Use ``values_list`` instead [performance].")

    def only(self, *args, **kwargs):
        # In rare cases Django can use this if a field is unexpectedly deferred. This
        # mostly can happen if a field is added to a model, and then an old pickle is
        # passed to a process running the new code. So if you see this error after a
        # deploy of a model with a new field, it'll likely fix itself post-deploy.
        raise NotImplementedError("Use ``values_list`` instead [performance].")
