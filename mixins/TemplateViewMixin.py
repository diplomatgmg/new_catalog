from django.core.exceptions import ImproperlyConfigured
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
