from django.urls import path
from progress.views import EntryTypeListView, PassEntryCreateView, EntryTypeDetailView

app_name = 'realty'

urlpatterns = [
    path('', EntryTypeListView.as_view(), name='entry-list'),
    path('entry/<int:pk>/detail', EntryTypeDetailView.as_view(), name='entry-detail'),
    path('entry/<int:pk>/create/', PassEntryCreateView.as_view(), name='entry-create'),

]
