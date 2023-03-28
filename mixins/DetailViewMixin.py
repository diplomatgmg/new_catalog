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
