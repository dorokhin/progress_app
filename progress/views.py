from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from progress.models import PassEntry, EntryType
from django.views.generic.list import ListView
from progress.forms import PassEntryAddForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count, DateField
from django.db.models.functions import Trunc


class EntryTypeListView(ListView):
    model = EntryType
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class EntryTypeDetailView(DetailView):
    model = EntryType

    def get_object(self, queryset=None):
        pass

    def get_context_data(self, **kwargs):
        context = super(EntryTypeDetailView, self).get_context_data(**kwargs)
        context['entries'] = PassEntry.objects.order_by()\
            .annotate(day=Trunc('creation_date', 'day', output_field=DateField()))\
            .values('day',).annotate(all_that_day=Count('id'))

        return context


class PassEntryCreateView(CreateView):
    model = PassEntry
    form_class = PassEntryAddForm

    def get_success_url(self):
        return reverse_lazy('progress:entry-detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.entry_type, _ = EntryType.objects.get_or_create(pk=self.kwargs.get(self.pk_url_kwarg))
        obj.save()

        return super().form_valid(form)
