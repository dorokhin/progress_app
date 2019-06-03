from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class EntryType(models.Model):

    name = models.CharField(max_length=200, default='', blank=True, verbose_name=_('Name'))

    def __str__(self):
        return '{name}'.format(name=self.name)


class PassEntry(models.Model):

    entry_type = models.ForeignKey(EntryType, related_name='entries', on_delete=models.CASCADE, verbose_name=_('Type'))
    author = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    approved = models.BooleanField(default=True, verbose_name=_('Approved'))
    creation_date = models.DateField(auto_now_add=True, verbose_name=_('Creation creation_date'))
    creation_time = models.TimeField(auto_now_add=True, verbose_name=_('Creation creation_time'))

    def __str__(self):
        return '{0}: {1}'.format(self.creation_date, self.creation_time)

    class Meta:
        verbose_name = _('PassEntry')
        verbose_name_plural = _('PassEntries')
        managed = True
        ordering = ['-creation_time']
