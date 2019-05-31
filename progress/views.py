from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from progress.models import PassEntry, EntryType
from django.views.generic.list import ListView
from progress.forms import PassEntryAddForm
from django.urls import reverse_lazy
from django.utils import timezone


class EntryTypeListView(ListView):
    model = EntryType
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class EntryTypeDetailView(DetailView):
    model = EntryType


class PassEntryCreateView(CreateView):
    model = PassEntry
    form_class = PassEntryAddForm

    def get_success_url(self):
        return reverse_lazy('realty:house-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article = get_object_or_404(EntryTypeListView, id=self.kwargs.get('article_pk'))
        return super().form_valid(form)
