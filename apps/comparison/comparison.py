class Comparison:
    def __init__(self, request, comparison_model):
        if request.user.is_authenticated:
            comparison, created = comparison_model.objects.get_or_create(
                user=request.user
            )
        else:
            session = request.session
            if not session.session_key:
                session.create()
            comparison, created = comparison_model.objects.get_or_create(
                temp_user=session.session_key
            )
        self.comparison = comparison

    def add(self, product):
        self.comparison.products.add(product)
