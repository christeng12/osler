from django.utils.timezone import now
from django.contrib import admin

from osler.utils import admin as admin_utils
from osler.core import models
from osler.workup.models import Workup
import datetime


for model in [models.Language, models.Patient,
              models.Gender, models.ActionInstruction, models.Ethnicity,
              models.ReferralType, models.ReferralLocation,
              models.ContactMethod, models.DocumentType, models.Outcome]:
    admin_utils.simplehistory_aware_register(model)

admin.site.register(models.Document, admin_utils.NoteAdmin)
admin.site.register(models.ActionItem, admin_utils.ActionItemAdmin)


@admin.register(models.PatientDataSummary)
class PatientDataDashboardAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/sale_summary_change_list.html'
    change_list_template = "admin/patient_data_dashboard_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super(PatientDataDashboardAdmin, self).changelist_view(
            request, extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        patients = models.Patient.objects.all()

        frankie = patients.filter(pk=1)
        # gets workups based on patient pk (aka get frankie's workups)
        workups = Workup.objects.filter(patient__in=list(patients.values_list('pk', flat=True)))

        hypertensive_workups = Workup.objects.filter(bp_sys__gte=140)

        # hypertensive_pks = list(set(hypertensive_workups.values_list('patient', flat=True))) #gets unique list of hypertensive pks
        hypertensive_pks = list(hypertensive_workups.values_list('patient', flat=True))
        hypertensive_bps = list(hypertensive_workups.values_list('bp_sys', flat=True)) #gets list of all hypertensive bp values from workups
        hypertensive_ethnicities = list(models.Patient.objects.filter(pk__in=hypertensive_pks)
                .values_list('ethnicities', flat=True))
        hypertensive_age = list()
        for patient in models.Patient.objects.filter(pk__in=hypertensive_pks):
            age = patient.age()
            hypertensive_age.append(age)
            
        # print(str(hypertensive_pks) + " " + str(hypertensive_age) + " " +
        #       str(hypertensive_bps) + " " + str(hypertensive_ethnicities) + " ")

        dict_list = list()
        for pk in range(1,len(hypertensive_workups)+1):
            dob = models.Patient.objects.filter(pk=pk)
            for patient in dob:
                age = patient.age()
            dictitem = {
                'workup': list(Workup.objects.filter(pk=pk)),
                'bp': list(Workup.objects.filter(pk=pk).values_list('bp_sys', flat=True)),
                'ethnicities': list(models.Patient.objects.filter(pk=pk).values_list('ethnicities', flat=True)),
                'age': age
            }
            dict_list.append(dictitem)

        print(dict_list)

        
        response.context_data['data'] = dict_list

        return response
