#coding: utf8
from django import forms
from django.forms.models import formset_factory, modelformset_factory

from organization.models import Organization

from models import Patient, Visit, Diagnosis
from widgets import CalendarWidget


class SearchForm(forms.Form):
    """ Форма поиска пациентов """
    _LPU_QS = Visit.objects.filter(is_add=True).values_list('lpu')
    _LPU_ADDED_QS = Organization.objects.filter(pk__in=_LPU_QS)
    full_name = forms.CharField(required=False, label=u'ФИО')
    birthday = forms.DateField(required=False, label=u'Дата рождения')
    death = forms.DateField(required=False, label=u'Дата смерти')
    diagnosis = forms.CharField(required=False, label=u'Диагноз по МКБ')
    lpu_added = forms.ModelChoiceField(required=False,
                                       label=u'МО внесения в регистр',
                                       queryset=_LPU_ADDED_QS)
    special_cure = forms.ChoiceField(required=False,
                                     label=u'Спец. лечение',
                                     choices=Patient.SPECIAL_CURES)


class PatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.iteritems():
            if isinstance(field, forms.DateField):
                self.fields[name].widget = CalendarWidget()
                print name

    # если одно поле заполенно, то нужно проверять заполнены ли другие поля
    double_required = (('allocate_lpu', 'code_allocate_lpu',),)
    def clear(self):
        cd = self.cleaned_data
        for params in self.double_required:
            avalible = None
            for name in params:
                curr_avalible = bool(cd.get(name))
                if avalible is None:
                    avalible = curr_avalible
                if curr_avalible != avalible:
                    label = self.fields[name].label
                    text = u'%s обязательно для заполнения' % label
                    raise forms.ValidationError(text)
        return cd

    class Meta:
        model = Patient
        exclude = ('is_active', 'user_changed', 'date_changed',)


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        exclude = ('is_active', 'patient', 'user_created', 'date_created',
                   'name', 'code',)


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        exclude = ('is_active', 'patient', 'user_changed', 'date_changed',)


DiagnosisFormset = formset_factory(DiagnosisForm, extra=1, max_num=100)


DiagnosisModelFormset = modelformset_factory(Diagnosis,
                                             form=DiagnosisForm,
                                             extra=1,
                                             max_num=100,
                                             can_delete=True)
