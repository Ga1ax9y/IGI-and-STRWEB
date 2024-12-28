from .models import Service,Customer,ServiceType,Order,EmployeeSpecialization,Review,FAQ,Vacancy,PromoCode,News,Employee,SliderSettings
from django.forms import ModelForm, TextInput, NumberInput,ModelChoiceField,Select,CheckboxSelectMultiple,DateInput,DateField,CharField
from datetime import date
from django.core.exceptions import ValidationError
import re
from django import forms
from .models import Company
def validate_birth_date(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('Пользователь должен быть старше 18 лет.')

def validate_phone_number(value):
    pattern = re.compile(r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$')
    if not pattern.match(value):
        raise ValidationError('Номер телефона должен быть в формате +375 (29) XXX-XX-XX')

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ["title","description","price","service_type"]
        widgets = {
            "title" : TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Введите название услуги'

        }),
            "description" : TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Введите описание услуги'
        }),
            "price" : NumberInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Введите стоимость услуги'
        })
            }
    service_type = ModelChoiceField(queryset=ServiceType.objects.all(), widget=Select(attrs={'class': 'form-control'}))

class CustomerRegistrationForm(ModelForm):
    birth_date = DateField(
        validators=[validate_birth_date],
        input_formats=['%d/%m/%Y'],
        widget=DateInput(attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'})
    )
    contact_phone = CharField(
        validators=[validate_phone_number],
        widget=TextInput(attrs={'placeholder': '+375 (29) XXX-XX-XX'})
    )
    class Meta:
        model = Customer
        fields = ['full_name','birth_date', 'company_name', 'contact_phone', 'customer_type']

class EmployeeForm(ModelForm):
    birth_date = DateField(
        validators=[validate_birth_date],
        input_formats=['%d/%m/%Y'],
        widget=DateInput(attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'})
    )
    work_phone = CharField(
        validators=[validate_phone_number],
        widget=TextInput(attrs={'placeholder': '+375 (29) XXX-XX-XX'})
    )
    class Meta:
        model = Employee
        fields = ['full_name','birth_date', 'specializations', 'photo','work_email','description','work_phone']

class EmployeeFullForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'birth_date', 'specializations', 'photo', 'work_phone', 'work_email', 'description']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['services', 'address', 'date_of_work','promo_code']
        widgets = {
            'services': CheckboxSelectMultiple(),
        }
class OrderUpdateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_code']


class EmployeeSpecializationForm(ModelForm):
    class Meta:
        model = EmployeeSpecialization
        fields = ['name']

class ServiceTypeForm(ModelForm):
    class Meta:
        model = ServiceType
        fields = ['name']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']


class FAQForm(ModelForm):
    class Meta:
        model = FAQ
        fields = ['question']

class AnswerForm(ModelForm):
    class Meta:
        model = FAQ
        fields = ['answer']

class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description']


class PromoCodeForm(ModelForm):
    class Meta:
        model = PromoCode
        fields = ['code', 'description', 'valid_until','discount_coefficient']

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'summary', 'image']


class FullOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_code', 'services', 'address', 'date_of_work', 'customer', 'employee']



class SliderSettingsForm(forms.ModelForm):
    class Meta:
        model = SliderSettings
        fields = ['loop', 'navs', 'pags', 'auto', 'stopMouseHover', 'auto_slide_delay']
        widgets = {
            'auto_slide_delay': forms.NumberInput(attrs={'min': 1}),
        }
