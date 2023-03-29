from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic.base import TemplateResponseMixin


class TemplateViewMixin(TemplateResponseMixin, View):
    response_class = TemplateResponse
    template_name = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        return self.response_class(
            request=self.request,
            template=self.template_name,
            context=context,
            **response_kwargs,
        )

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
        else:
            raise ImproperlyConfigured(
                f"Не определен template_name для  {self.__class__.__name__}"
            )


class ListViewMixin:
    model = None
    object_list = None
    context_object_name = None

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_object_name = self.get_context_object_name()
        context = {context_object_name: self.object_list, **kwargs}
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


class DetailViewMixin:
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset().select_related("category", "brand")

        slug = self.kwargs.get("slug")
        queryset = queryset.filter(slug=slug)
        try:
            return queryset.get()
        except queryset.model.DoesNotExist:
            return []

    def get_queryset(self):
        return self.model.objects.all()


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
        return redirect(self.get_success_url())

    def get_success_url(self):
        raise ImproperlyConfigured(
            "Не определен метод get_success_url "
            f"в представлении {self.__class__.__name__}"
        )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)
