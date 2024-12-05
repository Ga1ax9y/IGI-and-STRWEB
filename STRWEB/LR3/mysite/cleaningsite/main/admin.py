from django.contrib import admin
from .models import Service, Customer,EmployeeSpecialization,Employee,ServiceType,\
            Order,News,Review,AboutUs,FAQ,PromoCode, Company, Partner,SliderSettings
# Register your models here.
admin.site.register(ServiceType)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'service_type')
    list_filter = ('title', 'price')
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'contact_phone')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'work_phone','work_email')

admin.site.register(EmployeeSpecialization)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'customer', 'employee', 'date_of_work')
    list_filter = ('order_code', 'date_of_work')


admin.site.register(News)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'rating', 'date')
    list_filter = ('rating', 'date')

admin.site.register(AboutUs)



@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'asked_by','date_added')
    list_filter = ('asked_by','date_added')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active','valid_until')
    list_filter = ('is_active','valid_until')

admin.site.register(Company)
admin.site.register(Partner)
@admin.register(SliderSettings)
class SliderSettingsAdmin(admin.ModelAdmin):
    list_display = ('auto_slide_delay',)
