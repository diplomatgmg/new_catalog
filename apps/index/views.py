from mixins.TemplateViewMixin import TemplateViewMixin


class IndexView(TemplateViewMixin):
    template_name = "index/index.html"
