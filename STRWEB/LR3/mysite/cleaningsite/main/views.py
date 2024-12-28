from django.shortcuts import render,redirect,get_object_or_404
import matplotlib.pyplot
from .models import Service,Customer,ServiceType,Employee,EmployeeSpecialization,\
    Order,News,Review,AboutUs,FAQ,Vacancy,PromoCode,Company,Partner,SliderSettings
from .forms import ServiceForm,CustomerRegistrationForm,OrderForm,OrderUpdateForm,\
                    ServiceTypeForm,EmployeeSpecializationForm,ReviewForm,FAQForm,AnswerForm,\
                    VacancyForm,PromoCodeForm,NewsForm,FullOrderForm,EmployeeForm,SliderSettingsForm,EmployeeFullForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User,Group
from django.db.models import Sum, Avg, Count
from django.core.exceptions import ObjectDoesNotExist
import re
from PIL import Image
from io import BytesIO
import requests
from datetime import datetime, timedelta
import statistics
from django.utils import timezone
from datetime import date
from django.db.models.functions import ExtractYear
import calendar,tzlocal
import matplotlib
matplotlib.use('Agg')
import os
from django.conf import settings
import logging
from django.http import JsonResponse,HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import base64
from django.contrib import messages
import math

def powerSeries(x, eps):
    """
    Приближенное вычисление log((x+1)/(x-1)) с помощью разложения в ряд.
    Возвращает результат и количество итераций для одного значения x.
    """
    # Исключаем x = 0 и другие недопустимые значения
    if x == 0:
        raise ValueError("Значение x не может быть равно нулю для данной функции.")

    n = 0
    result = 0.0
    sum_term = 1 / ((2 * n + 1) * pow(x, 2 * n + 1))

    while abs(sum_term) >= eps:
        result += 2 * sum_term
        n += 1
        sum_term = 1 / ((2 * n + 1) * pow(x, 2 * n + 1))

        if n > 500:
            break

    return result



def graph_view(request):
    if request.method == "POST":
        try:
            x_start = float(request.POST.get("x_start", -5))
            x_end = float(request.POST.get("x_end", 5))
            eps = float(request.POST.get("eps", 0.001))
            chart_image = request.POST.get('chart_image')

        except (ValueError, TypeError):
            x_start, x_end, eps = -5, 5, 0.001

        x_values = [x for x in [x_start + i * 0.1 for i in range(int((x_end - x_start) / 0.1) + 1)]]
        print(x_values)
        if x_start < -1.05:
            x_values.insert(0,-1.05)
        if x_start < -1.02:
            x_values.insert(0,-1.02)
        if x_end > 1.05:
            x_values.append(1.05)
        if x_end > 1.02:
            x_values.append(1.02)

        x_values.sort()
        series_segments = []
        math_segments = []
        temp_series = []
        temp_math = []

        for x in x_values:
            if abs(x) > 1.01:
                try:
                    series_y = powerSeries(x, eps)
                    math_y = math.log((x + 1) / (x - 1))
                    temp_series.append((x, series_y))
                    temp_math.append((x, math_y))
                except ValueError:
                    if temp_series:
                        series_segments.append(temp_series)
                        temp_series = []
                    if temp_math:
                        math_segments.append(temp_math)
                        temp_math = []
            else:
                if temp_series:
                    series_segments.append(temp_series)
                    temp_series = []
                if temp_math:
                    math_segments.append(temp_math)
                    temp_math = []

        if temp_series:
            series_segments.append(temp_series)
        if temp_math:
            math_segments.append(temp_math)
        print(series_segments)
        context = {
            'series_segments': json.dumps(series_segments),
            'math_segments': json.dumps(math_segments),
        }
    else:
        context = {
            'series_segments': json.dumps([]),
            'math_segments': json.dumps([]),
        }

    return render(request, 'main/graph.html', context)
###################
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger(__name__)

def index(request):
    sort_services(request)
    return index_btn(request)

def news_detail(request, id):
    news = get_object_or_404(News,
                             id=id)

    return render(request, 'main/news_detail.html', {'news': news})

def task7(request):
    return render(request, 'main/task7.html')


def contact_table(request):
    if request.method == 'POST':
        # Получаем формы
        user_form = UserCreationForm(request.POST)
        employee_form = EmployeeFullForm(request.POST, request.FILES)

        # Проверяем валидность обеих форм
        if user_form.is_valid() and employee_form.is_valid():
            # Сохраняем пользователя
            user = user_form.save()

            # Создаем сотрудника и связываем его с пользователем
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            # Перенаправляем на страницу таблицы после успешного сохранения
            return redirect('contact_table')

    else:
        # Для GET запроса создаем пустые формы
        user_form = UserCreationForm()
        employee_form = EmployeeFullForm()

    # Получаем все данные сотрудников для отображения на странице
    employees = Employee.objects.all()

    return render(request, 'main/contact_table.html', {
        'employees': employees,
        'user_form': user_form,
        'employee_form': employee_form
    })
# Обработка подробностей сервиса
def service_detail(request, year, month, day, id):
    # Получаем сервис по ID и дате публикации (year, month, day)
    service = get_object_or_404(Service, id=id, publish__year=year, publish__month=month, publish__day=day)

    user_is_superuser = request.user.is_superuser
    is_employee = request.user.groups.filter(name='Employee').exists()
    is_customer = request.user.groups.filter(name='Customer').exists()
    # Обработка POST-запросов
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete' and user_is_superuser:
            # Удаление сервиса - доступно только суперпользователю
            service.delete()
            return redirect('home')  # Перенаправляем на главную страницу

        elif action == 'edit' and (user_is_superuser or is_employee):
            # Редактирование сервиса - доступно суперпользователю и сотруднику
            service_types = ServiceType.objects.all()
            return render(request, "main/administrator/edit_service.html", {
                'service': service,
                'service_types': service_types,
                'user_is_superuser': user_is_superuser
            })

        elif action == 'update' and user_is_superuser:
            # Обновление сервиса - доступно только суперпользователю
            if 'title' in request.POST and request.POST['title'].strip():
                service.title = request.POST['title']
            if 'description' in request.POST and request.POST['description'].strip():
                service.description = request.POST['description']
            if 'price' in request.POST and request.POST['price'].strip():
                service.price = request.POST['price']

            service_type_title = request.POST.get('service_type')
            if service_type_title:
                service_type = ServiceType.objects.get(id=service_type_title)
                service.service_type = service_type

            service.save()  # Сохраняем изменения
            return redirect('home')  # Перенаправляем на главную страницу после сохранения изменений

        elif action == 'buy' and request.user.is_authenticated:
            # Добавление в корзину - доступно авторизованным пользователям
            customer = Customer.objects.get(user=request.user)
            customer.cart.add(service)
            return redirect('home')  # Можно перенаправить на корзину или отобразить сообщение

    # Возвращаем страницу с подробностями о сервисе
    return render(request, "main/service_detail.html", {
        'service': service,
        'user_is_superuser': user_is_superuser,
        'is_employee': is_employee,
        'is_customer':is_customer,
        'service_types': ServiceType.objects.all(),
        'is_authenticated': request.user.is_authenticated
    })

# Функция для получения данных о компании, пользователе и услугах
def get_common_data(request):
    company = Company.objects.first()
    is_auth = request.user.is_authenticated
    user_is_superuser = request.user.is_superuser
    is_employee = request.user.groups.filter(name='Employee').exists()
    is_customer = request.user.groups.filter(name='Customer').exists()

    services = sort_services(request)

    return company, is_auth, user_is_superuser, is_employee, is_customer, services


def get_slider_settings(request):
    slider_settings, created = SliderSettings.objects.get_or_create(id=1)

    if request.method == 'POST' and 'action' in request.POST and request.POST['action'] == 'update_slider_settings' and request.user.is_superuser:
        
        form = SliderSettingsForm(request.POST, instance=slider_settings)
        if form.is_valid():
            form.save()
        else:
            pass

    return slider_settings


# Функция для обработки поиска по сервисам
def search_services(request, services):
    search_service_title = request.GET.get('service_title', None)
    if search_service_title is not None and search_service_title.strip() != "":
        regex = re.escape(search_service_title)
        services = services.filter(title__iregex=regex)
    return services




# Функция для обновления деталей сервиса
def update_service_details(request, service, service_type):
    if request.POST.get('title').strip():
        service.title = request.POST.get('title')
    if request.POST.get('description').strip():
        service.description = request.POST.get('description')
    if request.POST.get('price').strip():
        service.price = request.POST.get('price')
    service.service_type = service_type
    service.save()

def index_btn(request):
    # Получаем общие данные
    company, is_auth, user_is_superuser, is_employee, is_customer, services = get_common_data(request)

    # Получаем и обновляем настройки слайдера
    slider_settings = get_slider_settings(request)
    slider_form = SliderSettingsForm(instance=slider_settings)  # Форма для слайдера

    if request.method == 'POST':
        # Обрабатываем действия с сервисами (удаление, редактирование, добавление в корзину)
        service_title = request.POST.get('service_title')
        service = Service.objects.filter(title=service_title).first()

        if service:
            # Обработка действий с сервисом
            result = handle_service_actions(request, user_is_superuser, is_employee, service)
            if result:
                return result  # Возвращаем результат редиректа или ответа, если действие выполнено

    elif request.method == 'GET':
        # Обрабатываем поиск сервисов (если это GET-запрос)
        services = search_services(request, services)

    # Преобразуем сервисы в список словарей, чтобы передать их в шаблон
    services_data = [service.to_dict() for service in services]

    return render(request, "main/index.html", {
        'services_data': json.dumps(services_data, cls=DjangoJSONEncoder),
        'services': services,
        'user_is_superuser': user_is_superuser,
        'is_authenticated': is_auth,
        'is_employee': is_employee,
        'is_customer': is_customer,
        'company': company,
        'last_news': News.objects.last(),
        'slider_form': slider_form,  # Передаем форму слайдера
        'slider_settings': slider_settings,  # Передаем объект настроек слайдера для JavaScript
    })




def about(request):
    logger.info('In about us')

    user_is_superuser = request.user.is_superuser
    is_employee = request.user.groups.filter(name='Employee').exists()
    inforamation = Company.objects.first()
    print(inforamation)

    return render(request,"main/about.html",{'information':inforamation})

@user_passes_test(lambda u: u.is_superuser)
def create(request):
    logger.info('In create')
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = ServiceForm()
    context = {
        'form' : form
    }
    return render(request,"main/administrator/create.html",context)


def register_customer(request):
    logger.info('In register')
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        customer_form = CustomerRegistrationForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer_group = Group.objects.get(name='Customer')
            user.groups.add(customer_group)
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('login')
    else:
        user_form = UserCreationForm()
        customer_form = CustomerRegistrationForm()
    return render(request, 'main/authorization/register_customer.html', {'user_form': user_form, 'customer_form': customer_form})


def user_login(request):
    logger.info('In login')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/authorization/login.html', {'form': form})

def get_user_time():
    user_timezone = tzlocal.get_localzone()
    current_date = datetime.now(user_timezone).date()
    current_date_formatted = current_date.strftime("%d/%m/%Y")

    calendar_text = calendar.month(
        datetime.now(user_timezone).year,
        datetime.now(user_timezone).month,
    )

    return {
        "user_timezone": user_timezone,
        "current_date_formatted": current_date_formatted,
        "calendar_text": calendar_text,
    }

def user_profile(request):
    logger.info('In profile')
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'action' in request.POST and request.POST['action'] == 'logout':
                logout(request)
                return redirect('home')
        user_zone = get_user_time()
        is_superuser = request.user.is_superuser
        is_employee = request.user.groups.filter(name='Employee').exists()
        type_of_user = None
        if is_employee:
            type_of_user = Employee.objects.get(user=request.user)
        elif not is_superuser:
            type_of_user = Customer.objects.get(user=request.user)
        return render(request, 'main/profile/profile.html',
                              {'nickname': request.user,
                               'user': type_of_user,
                               'is_superuser': is_superuser,
                               'is_employee':is_employee,
                               'user_zone':user_zone})
    else:
        return redirect('login')


def sort_services(request):
    sort_direction = request.GET.get('sort_direction')

    if sort_direction == 'asc':
        services = Service.objects.all().order_by('price')
    elif sort_direction == 'desc':
        services = Service.objects.all().order_by('-price')
    else:
        services = Service.objects.all()

    return services

def user_management(request):
    logger.info('In managment')
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        employee_group = Group.objects.get(name='Employee')
        customer_group = Group.objects.get(name='Customer')
        if action == 'add':
            user.groups.remove(customer_group)
            try:
                customer = Customer.objects.get(user=user)
                employee = Employee(user=user, full_name=customer.full_name, work_phone=customer.contact_phone,birth_date=customer.birth_date)
                employee.save()
                customer.delete()
            except Customer.DoesNotExist:
                logger.error('Error: Customer.DoesNotExist')
                pass
            user.groups.add(employee_group)
        elif action == 'remove':
            user.groups.remove(employee_group)
            try:
                employee = Employee.objects.get(user=user)
                customer = Customer(user=user, full_name=employee.full_name, contact_phone=employee.work_phone,customer_type='individual',birth_date=employee.birth_date)
                customer.save()
                employee.delete()
            except Employee.DoesNotExist:
                logger.error('Employee: Customer.DoesNotExist')
                pass
            user.groups.add(customer_group)
        return redirect('management')
    else:
        employees = Employee.objects.all()
        customers = Customer.objects.all()
        return render(request, 'main/administrator/management.html', {'employees': employees, 'customers': customers})


def employee_detail(request, employee_id):
    logger.info('In employee profile')
    user_is_superuser = request.user.is_superuser
    employee = get_object_or_404(Employee, id=employee_id)
    orders = Order.objects.filter(employee_id=employee_id)
    return render(request, 'main/profile/employee_detail.html', {
        'employee': employee,
        'orders': orders,
        'user_is_superuser': user_is_superuser
    })

@user_passes_test(lambda u: u.is_superuser)
def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', employee_id=employee.id)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'main/profile/update_employee.html', {'form': form, 'employee': employee})

def customer_detail(request, customer_id):
    user_is_superuser = request.user.is_superuser
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer_id=customer_id)
    total_cost = 0

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            orders = orders.filter(date_of_work__range=(start_date, end_date))

            for order in orders:
                total_cost += order.total_cost()
        except ValueError:
            logger.error("Invalid date format. Expected 'YYYY-MM-DD'.")

    return render(request, 'main/profile/customer_detail.html', {
        'customer': customer,
        'orders': orders,
        'user_is_superuser': user_is_superuser,
        'total_cost': total_cost,
        'start_date': start_date,
        'end_date': end_date
    })


@login_required
def user_edit(request):
    logger.info('In user edit')
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    is_customer = user.groups.filter(name='Customer').exists()

    if is_employee:
        employee = get_object_or_404(Employee, user=user)
        if request.method == 'POST':
            form = EmployeeForm(request.POST, request.FILES, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = EmployeeForm(instance=employee)
        return render(request, "main/profile/edit_profile.html", {'form': form, 'is_employee': is_employee})

    elif is_customer:
        customer = get_object_or_404(Customer, user=user)
        if request.method == 'POST':
            form = CustomerRegistrationForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = CustomerRegistrationForm(instance=customer)
        return render(request, "main/profile/edit_profile.html", {'form': form, 'is_customer': is_customer})

    return redirect('profile')

def cart_view(request):
    logger.info('In cart')
    current_user = Customer.objects.get(user=request.user)
    context = {'customer': current_user}
    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'delete':
            service_title = request.POST.get('service_title')
            service = Service.objects.get(title=service_title)
            current_user.cart.remove(service)

    return render(request, 'main/cart.html', context)

def make_order(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.save()
            form.save_m2m()
            customer.cart.clear()
            return redirect('home')
    else:
        initial_data = {
            'services': customer.cart.all(),
        }
        form = OrderForm(initial=initial_data)
    return render(request, 'main/order/order.html', {'form': form})

@login_required
def view_orders(request):
    logger.info('In orders')
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    is_customer = user.groups.filter(name='Customer').exists()
    user_is_superuser = request.user.is_superuser
    orders_data = []
    employee_id = request.GET.get('employee_id')
    sort_direction = request.GET.get('sort_direction')

    if sort_direction == 'asc':
        if is_customer:
            orders = Order.objects.filter(customer__user=user).order_by('date_of_work')
        elif is_employee:
            orders = Order.objects.filter(employee__user=user).order_by('date_of_work')
        elif user_is_superuser:
            orders = Order.objects.all().order_by('date_of_work')
    elif sort_direction == 'desc':
        if is_customer:
            orders = Order.objects.filter(customer__user=user).order_by('-date_of_work')
        elif is_employee:
            orders = Order.objects.filter(employee__user=user).order_by('-date_of_work')
        elif user_is_superuser:
            orders = Order.objects.all().order_by('-date_of_work')
    else:
        if is_customer:
            orders = Order.objects.filter(customer__user=user)
        elif is_employee:
            orders = Order.objects.filter(employee__user=user)
        elif user_is_superuser:
            orders = Order.objects.all()

    if employee_id:
        orders = orders.filter(employee_id=employee_id)

    for order in orders:
        order.total_cost_value = order.total_cost()

        orders_data.append({
            'info': order,
            'total_order_price': order.total_cost() if order.total_cost() is not None else 0
        })

    employees = Employee.objects.all()

    if request.method == "POST":
        if 'delete_order' in request.POST:
            order_id = request.POST.get('order_id')
            order_to_delete = get_object_or_404(Order, id=order_id)
            order_to_delete.delete()
            return redirect('orders')
        elif 'update_order' in request.POST:
            order_id = request.POST.get('order_id')
            return redirect('update_order', order_id=order_id)

    return render(request, 'main/order/myorders.html', {
        'orders': orders_data,
        'user_is_superuser': user_is_superuser,
        'is_employee': is_employee,
        'is_customer': is_customer,
        'employees': employees,
        'selected_employee_id': employee_id,
        'sort_direction': sort_direction
    })

@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = FullOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders')
    else:
        form = FullOrderForm(instance=order)
    return render(request, 'main/order/update_order.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Employee').exists(), login_url='login')
def unassigned_orders(request):
    logger.info('employee is looking for orders')
    orders = Order.objects.filter(employee__isnull=True)
    return render(request, 'main/order/unassigned_orders.html', {'orders': orders})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Employee').exists())
def edit_order(request, order_id):
    logger.info('Someone edited order')
    user = request.user
    employee = Employee.objects.get(user=user)
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            order.employee = employee
            order.save()
            form.save()
            return redirect('home')
    else:
        form = OrderUpdateForm(instance=order)
    return render(request, 'main/order/edit_order.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def add_employee_specialization(request):
    specializations = EmployeeSpecialization.objects.all()
    form = EmployeeSpecializationForm()
    editing = False
    specialization = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            form = EmployeeSpecializationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('add_specialization')
        elif action == 'edit':
            specialization_id = request.POST.get('specialization_id')
            specialization = get_object_or_404(EmployeeSpecialization, id=specialization_id)
            form = EmployeeSpecializationForm(instance=specialization)
            editing = True
        elif action == 'update':
            specialization_id = request.POST.get('specialization_id')
            specialization = get_object_or_404(EmployeeSpecialization, id=specialization_id)
            form = EmployeeSpecializationForm(request.POST, instance=specialization)
            if form.is_valid():
                form.save()
                return redirect('add_specialization')
        elif action == 'delete':
            specialization_id = request.POST.get('specialization_id')
            specialization = get_object_or_404(EmployeeSpecialization, id=specialization_id)
            specialization.delete()
            return redirect('add_specialization')

    return render(request, 'main/administrator/add_employee_specialization.html', {
        'form': form,
        'specializations': specializations,
        'editing': editing,
        'specialization': specialization,
    })

@user_passes_test(lambda u: u.is_superuser)
def add_service_type(request):
    servicetypes = ServiceType.objects.all()
    form = ServiceTypeForm()
    editing = False
    servicetype = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            form = ServiceTypeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('add_service_type')
        elif action == 'edit':
            servicetype_id = request.POST.get('servicetype_id')
            servicetype = get_object_or_404(ServiceType, id=servicetype_id)
            form = ServiceTypeForm(instance=servicetype)
            editing = True
        elif action == 'update':
            servicetype_id = request.POST.get('servicetype_id')
            servicetype = get_object_or_404(ServiceType, id=servicetype_id)
            form = ServiceTypeForm(request.POST, instance=servicetype)
            if form.is_valid():
                form.save()
                return redirect('add_service_type')
        elif action == 'delete':
            servicetype_id = request.POST.get('servicetype_id')
            servicetype = get_object_or_404(ServiceType, id=servicetype_id)
            servicetype.delete()
            return redirect('add_service_type')

    return render(request, 'main/administrator/add_service_type.html', {
        'form': form,
        'servicetypes': servicetypes,
        'editing': editing,
        'servicetype': servicetype,
    })

@user_passes_test(lambda u: u.is_superuser)
def adminpanel(request):
    return render(request, 'main/administrator/AdminPanel.html')


def news_view(request):
    if request.method == 'POST' and (request.user.groups.filter(name='Employee').exists() or request.user.is_superuser):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm()
    news_list = News.objects.all()[::-1]
    for news in news_list:
        print(f"News: {news.title}, Image URL: {news.image.url if news.image else 'No image'}")
    return render(request, 'main/news.html', {
        'news_list': news_list,
        'form': form,
        'is_employee': request.user.groups.filter(name='Employee').exists(),
        'user_is_superuser': request.user.is_superuser
    })

def tags(request):
    return render(request, 'main/tag_page.html')


def reviews_list(request):
    is_customer = request.user.groups.filter(name='Customer').exists()
    is_auth = request.user.is_authenticated
    reviews = Review.objects.all().order_by('-date')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user.customer
            review.save()
            return redirect('reviews_list')
    else:
        form = ReviewForm()

    return render(request, 'main/reviews_list.html', {'reviews': reviews, 'form': form,'is_customer':is_customer,'is_auth':is_auth})


def faq_list(request):
    is_auth = request.user.is_authenticated
    faqs = FAQ.objects.all().order_by('-date_added')
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.asked_by = request.user
            faq.save()
            return redirect('faq_list')
    else:
        form = FAQForm()

    is_employee = request.user.groups.filter(name='Employee').exists()
    user_is_superuser = request.user.is_superuser
    return render(request, 'main/faq_list.html', {'faqs': faqs, 'form': form, 'is_employee': is_employee,'user_is_superuser':user_is_superuser,'is_auth':is_auth})

@login_required
def answer_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=faq)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.save()
            return redirect('faq_list')
    else:
        form = AnswerForm(instance=faq)
    return render(request, 'main/answer_faq.html', {'form': form, 'faq': faq})


def contacts(request):
    employees = Employee.objects.all()
    return render(request, 'main/contacts.html', {'employees': employees})

def politics(request):
    return render(request, 'main/confidantial_politic.html')

def vacancies(request):
    if request.method == 'POST' and (request.user.groups.filter(name='Employee').exists() or request.user.is_superuser):
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacancies')
    else:
        form = VacancyForm()

    all_vacancies = Vacancy.objects.all()
    return render(request, 'main/vacancies.html', {
        'vacancies': all_vacancies,
        'form': form,
        'is_employee': request.user.groups.filter(name='Employee').exists(),
        'user_is_superuser': request.user.is_superuser
    })

def promo_codes(request):
    is_auth = request.user.is_authenticated
    if request.method == 'POST' and (request.user.groups.filter(name='Employee').exists() or request.user.is_superuser):
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('promo_codes')
    else:
        form = PromoCodeForm()

    all_promocodes = PromoCode.objects.all()
    return render(request, 'main/promocodes.html', {
        'promocodes': all_promocodes,
        'form': form,
        'is_employee': request.user.groups.filter(name='Employee').exists(),
        'user_is_superuser': request.user.is_superuser,
        'is_auth':is_auth

    })


def api_combined_view(request):
    name = request.GET.get('name', 'John')
    nationality_data = None
    cat_fact_data = None

    if name:
        response = requests.get(f'https://api.nationalize.io/?name={name}')
        if response.status_code == 200:
            nationality_data = response.json()

    response = requests.get('https://catfact.ninja/fact')
    if response.status_code == 200:
        cat_fact_data = response.json()

    return render(request, 'main/combined.html', {
        'nationality_data': nationality_data,
        'cat_fact_data': cat_fact_data,
        'name': name
    })


def get_customers_alphabetical():
    return Customer.objects.all().order_by('full_name')

def get_total_sales():
    total_sales = Order.objects.annotate(total_cost=Sum('services__price'))
    return total_sales.aggregate(Sum('total_cost'))['total_cost__sum']

def get_sales_statistics():
    sales = Order.objects.annotate(total_cost=Sum('services__price')).values_list('total_cost', flat=True)
    sales_list = list(sales)
    return {
        'average': statistics.mean(sales_list),
        'median': statistics.median(sales_list),
        'mode': statistics.mode(sales_list) if len(sales_list) > 1 else None,
    }

def get_customer_age_statistics():
    ages = Customer.objects.annotate(age=(timezone.now().date().year - ExtractYear('birth_date'))).values_list('age', flat=True)
    age_list = list(ages)
    return {
        'average': statistics.mean(age_list),
        'median': statistics.median(age_list),
    }

def get_customer_age_categories():
    current_year = timezone.now().year
    ages = Customer.objects.annotate(age=(current_year - ExtractYear('birth_date'))).values_list('age', flat=True)
    age_list = list(ages)

    age_categories = {
        '18-25': 0,
        '26-35': 0,
        '36-50': 0,
        '50+': 0
    }

    for age in age_list:
        if 18 <= age <= 25:
            age_categories['18-25'] += 1
        elif 26 <= age <= 35:
            age_categories['26-35'] += 1
        elif 36 <= age <= 50:
            age_categories['36-50'] += 1
        elif age > 50:
            age_categories['50+'] += 1

    return age_categories

def plot_age_distribution():
    stats = get_customer_age_categories()
    labels = list(stats.keys())
    values = list(stats.values())

    fig, ax = matplotlib.pyplot.subplots()
    ax.bar(labels, values)
    ax.set_xlabel('Age Categories')
    ax.set_ylabel('Number of Customers')
    ax.set_title('Customer Age Distribution')

    image_path = os.path.join(settings.MEDIA_ROOT, 'graphs/age_distribution.png')
    matplotlib.pyplot.savefig(image_path)
    matplotlib.pyplot.close(fig)
    return os.path.join(settings.MEDIA_URL, 'graphs/age_distribution.png')


def get_most_popular_service_type():
    return ServiceType.objects.annotate(service_count=Count('service')).order_by('-service_count').first()

def get_most_profitable_service_type():
    return ServiceType.objects.annotate(total_revenue=Sum('service__orders__services__price')).order_by('-total_revenue').first()


def statistics_view(request):
    customers = get_customers_alphabetical()
    total_sales = get_total_sales()
    sales_stats = get_sales_statistics()
    age_stats = get_customer_age_statistics()
    age_distribution_image_path = plot_age_distribution()
    most_popular_service_type = get_most_popular_service_type()
    most_profitable_service_type = get_most_profitable_service_type()
    service_type_distribution_image_path = plot_service_type_distribution()
    context = {
        'customers': customers,
        'total_sales': total_sales,
        'sales_stats': sales_stats,
        'age_stats': age_stats,
        'most_popular_service_type': most_popular_service_type,
        'most_profitable_service_type': most_profitable_service_type,
        'age_distribution_image_path':age_distribution_image_path,
        'service_type_distribution_image_path':service_type_distribution_image_path
    }
    return render(request, 'main/administrator/statistics.html', context)


def plot_service_type_distribution():
    service_types = Service.objects.values_list('service_type__name', flat=True).distinct()
    service_type_counts = {service_type: 0 for service_type in service_types}

    for order in Order.objects.all():
        for service in order.services.all():
            service_type = service.service_type.name
            if service_type in service_type_counts:
                service_type_counts[service_type] += 1
    labels = list(service_type_counts.keys())
    sizes = list(service_type_counts.values())

    fig, ax = matplotlib.pyplot.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    image_path = os.path.join(settings.MEDIA_ROOT, 'graphs/service_type_distribution.png')
    matplotlib.pyplot.savefig(image_path)
    matplotlib.pyplot.close(fig)
    return os.path.join(settings.MEDIA_URL, 'graphs/service_type_distribution.png')

def slider_view(request):
    # Загружаем настройки слайдера из базы данных
    slider_settings = SliderSettings.objects.first()
    auto_slide_delay = slider_settings.auto_slide_delay if slider_settings else 5000  # 5 секунд по умолчанию

    return render(request, 'slider.html', {'auto_slide_delay': auto_slide_delay})
