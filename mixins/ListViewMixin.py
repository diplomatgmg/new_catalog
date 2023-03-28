from django.core.exceptions import ImproperlyConfigured


class ListViewMixin:
    model = None
    object_list = None
    context_object_name = None

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def get_context_data(self):
        context_object_name = self.get_context_object_name()
        context = {context_object_name: self.object_list}
        return super().get_context_data(**context)

    def get_queryset(self):
        raise ImproperlyConfigured(
            "Не определен метод get_queryset "
            f"в представлении {self.__class__.__name__}"
        )

    def get_context_object_name(self):
        if self.context_object_name:
            return self.context_object_name
        raise NotImplementedError(
            "Не определен атрибут context_object_name "
            f"в представлении {self.__class__.__name__}"
        )
