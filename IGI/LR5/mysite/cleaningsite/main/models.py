from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
# Create your models here.


class ServiceType(models.Model):
    name = models.CharField('Название типа', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'


class Service(models.Model):
    title = models.CharField('Название',max_length=50)
    description = models.TextField('Описание')
    price = models.IntegerField('Стоимость',default=100)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name='Тип услуги',default=1)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, verbose_name='ФИО заказчика')
    birth_date = models.DateField(verbose_name='Дата рождения',default=date(2000, 1, 1))
    company_name = models.CharField(max_length=100, verbose_name='Название компании', blank=True, null=True)
    contact_phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    CUSTOMER_TYPE_CHOICES = (
        ('individual', 'Частное лицо'),
        ('legal_entity', 'Юридическое лицо'),
    )
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, verbose_name='Тип заказчика')
    cart = models.ManyToManyField(Service, related_name='customers_cart', blank=True)
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class EmployeeSpecialization(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование специализации')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специализация сотрудника'
        verbose_name_plural = 'Специализации сотрудников'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    full_name = models.CharField(max_length=100, verbose_name='ФИО сотрудника')
    birth_date = models.DateField(verbose_name='Дата рождения',default=date(2000, 1, 1))
    specializations = models.ManyToManyField(EmployeeSpecialization, related_name='employees', verbose_name='Специализации')
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True, verbose_name='Фото')
    work_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Рабочий телефон')
    work_email = models.EmailField(max_length=254, blank=True, null=True, verbose_name='Рабочая почта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание работ')
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Order(models.Model):
    order_code = models.CharField(max_length=100, unique=True,blank=True, null=True, verbose_name='Код заказа')
    services = models.ManyToManyField('Service', related_name='orders', verbose_name='Услуги')
    address = models.CharField(max_length=255, verbose_name='Адрес проведения работ')
    date_of_work = models.DateTimeField(default=timezone.now, verbose_name='Дата проведения работ')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='orders', verbose_name='Сотрудник', blank=True, null=True)
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='Промокод')

    def total_cost(self):
        total = sum(service.price for service in self.services.all())
        if self.promo_code and self.promo_code.is_active:
            total *= self.promo_code.discount_coefficient
        return total

    def __str__(self):
        return self.order_code if self.order_code else f"Непринятый заказ {self.id}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    summary = models.TextField(verbose_name='Краткое содержание')
    image = models.ImageField(upload_to='news_images/', verbose_name='Картинка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(verbose_name='Оценка', choices=[(i, i) for i in range(1, 6)])
    text = models.TextField(verbose_name='Текст отзыва')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f"{self.customer.full_name} - {self.rating}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class AboutUs(models.Model):
    summary = models.TextField(verbose_name='Информация')

    def __str__(self):
        return "Информация"

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'


class FAQ(models.Model):
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ', blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now, verbose_name='Дата добавления')
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name='Клиент')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'


class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Описание вакансии')
    posted_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Промокод')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Действующий')
    valid_until = models.DateField(verbose_name='Годен до', null=True, blank=True)
    discount_coefficient = models.FloatField(default=1.0, verbose_name='Коэффициент скидки')


    def is_valid(self):
        if self.valid_until and self.valid_until < timezone.now().date():
            self.is_active = False
            self.save() 
        return self.is_active

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
