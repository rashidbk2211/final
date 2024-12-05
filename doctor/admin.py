from django.contrib import admin
from .models import Doctor
#Prescription

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'specialization', 'license_number')
    list_filter = ('specialization',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization', 'license_number')
    readonly_fields = ('user',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

#@admin.register(Prescription)
#class PrescriptionAdmin(admin.ModelAdmin):
 #   list_display = ('patient', 'doctor', 'date', 'medications')
  #  list_filter = ('date', 'doctor')
   # search_fields = ('patient__user__username', 'doctor__user__username', 'medications')
    #date_hierarchy = 'date'

