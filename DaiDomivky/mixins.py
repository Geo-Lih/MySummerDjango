from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.utils.text import slugify


class SlugifyMixin:
    def form_valid(self, form):
        post_obj = form.save(commit=False)  # returns post instance without sending it to db
        post_obj.author = self.request.user
        post_obj.slug = slugify(post_obj.title)  # creating slug for post
        # post_obj.save()
        # return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)  # saving and redirection by FormMixin


class SuccessUrlMixin:
    success_url_name = ''

    def get_success_url(self):
        return reverse_lazy(self.success_url_name)


class PermissionHandlerMixin:
    def handle_no_permission(self):
        return HttpResponseNotFound()
