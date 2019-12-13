from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import CaptchaLoginForm
from django.http import HttpResponseRedirect
from progress.models import PassEntry, EntryType
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from progress.forms import PassEntryAddForm
from django.contrib.auth import logout
from django.views.generic import View
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count, DateField
from django.db.models.functions import Trunc
from django.urls import reverse
from django.http import Http404


class MainPageView(TemplateView):
    template_name = 'progress/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = EntryType.objects.all()
        return context


class EntryTypeListView(ListView):
    model = EntryType
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['entries'] = PassEntry.objects.order_by()\
            .annotate(day=Trunc('creation_date', 'day', output_field=DateField()))\
            .values('day',).annotate(all_that_day=Count('id'))
        return context


class EntryTypeDetailView(DetailView):
    model = EntryType

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if pk is None:
            raise AttributeError(
                "Custom detail view %s must be called with either an object "
                "pk in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super(EntryTypeDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['entries'] = PassEntry.objects.filter(author__passentry__entry_type_id=self.get_object())\
            .annotate(day=Trunc('creation_date', 'day', output_field=DateField()))\
            .values('day',).annotate(all_that_day=Count('id'))

        return context


class PassEntryCreateView(CreateView):
    model = PassEntry
    form_class = PassEntryAddForm

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('main'))

    def get_success_url(self):
        return reverse_lazy('progress:entry-detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

    def form_valid(self, form):

        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.entry_type, _ = EntryType.objects.get_or_create(pk=self.kwargs.get(self.pk_url_kwarg))
        obj.save()

        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('main'))


class CaptchaLoginView(LoginView):
    form_class = CaptchaLoginForm
    redirect_authenticated_user = True
