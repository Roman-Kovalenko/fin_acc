from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string


# TODO: Переделать в универсальный Mixin
class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                'name': self.object.name
            }
            return JsonResponse(data)
        else:
            return response

    def get(self, request, *args, **kwargs):
        """
        Для ajax-запроса возвращаем форму с минимальным шаблоном
        """
        response = super().get(request, *args, **kwargs)
        if self.request.is_ajax():
            html = render_to_string(
                self.ajax_template_name,
                context={'form': self.get_form()},
                request=self.request
            )
            return HttpResponse(html)
        return response
