from django.core.exceptions import ImproperlyConfigured


class CreateViewMixin:
    form_class = None

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self):
        form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_class(self):
        if self.form_class:
            return self.form_class
        raise ImproperlyConfigured(
            "Не определен атрибут form_class "
            f"в представлении {self.__class__.__name__}"
        )

    def get_form_kwargs(self):
        kwargs = {}

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def form_valid(self, form):
        raise ImproperlyConfigured(
            "Не определен метод form_valid "
            f"в представлении {self.__class__.__name__}"
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)
