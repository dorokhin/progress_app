from django.urls import path
from progress.views import EntryTypeListView, PassEntryCreateView, EntryTypeDetailView

app_name = 'progress'

urlpatterns = [
    path('', EntryTypeListView.as_view(), name='entry-list'),
    path('<int:pk>/detail', EntryTypeDetailView.as_view(), name='entry-detail'),
    path('<int:pk>/create/', PassEntryCreateView.as_view(), name='entry-create'),

]
