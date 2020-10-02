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

        dashboard_data = {}

        for patient in patients:
            metrics = {}
            metrics['high_bp'] = False
            workup = patient.latest_workup()
            try:
                bp_reading = workup.bp_sys
                if(bp_reading>120):
                    metrics['high_bp'] = bp_reading
            except AttributeError:
                None
                
            metrics['gender'] = patient.gender.name
            metrics['age'] = (now().date() - patient.date_of_birth).days // 365
            metrics['ethnicity'] = patient.ethnicities.name
            dashboard_data[patient.name()] = metrics

        frankie = patients.filter(pk=1)
        # gets workups based on patient pk (aka get frankie's workups)
        workups = Workup.objects.filter(patient__in=list(frankie.values_list('pk', flat=True)))
        # models.PatientDataSummary.objects.create(bp_readings=[130,120,150])

        # metrics = {
        #     #'age': (now().date() - qs.values('date_of_birth')).days // 365,
        #     #'name': qs[0].name(),
        #     #'bp': q.values('bp_sys'),
        # }

        # for patient in patients:
        #     patient.
        # for patient in models.Patient.objects.raw('SELECT * FROM core_patient'):
        #     print(patient.gender)

        response.context_data['data'] = dict(
            dashboard_data
        )
        # response.context_data['bp'] = list(
        #     q.values('bp_sys')
        # )

        return response
