#coding: utf8
from django.db import models


class Organization(models.Model):
    """ Названия мед. организаций """
    code = models.CharField(u'Код МО', max_length=7, unique=True)
    name = models.CharField(u'Название', max_length=50)
    full_name = models.TextField(verbose_name=u'Полное название')

    def __unicode__(self):
        return u"%s (%s)" % (self.full_name, self.code,)

    class Meta:
        verbose_name = u'Название организации'
        verbose_name_plural = u'Названия организаций'

    def save(self, *args, **kwargs):
        from patient.models import Patient, Visit

        if self.pk is not None:
            Patient.objects.filter(allocate_lpu=self) \
                           .update(code_allocate_lpu=self.code,
                                   name_allocate_lpu=self.full_name)
            Visit.objects.filter(lpu=self) \
                         .update(code=self.code, name=self.full_name)
        super(Organization, self).save(*args, **kwargs)
