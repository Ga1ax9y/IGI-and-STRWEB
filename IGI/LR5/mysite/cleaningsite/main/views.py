from django.shortcuts import render,redirect,get_object_or_404
import matplotlib.pyplot
from .models import Service,Customer,ServiceType,Employee,EmployeeSpecialization,Order,News,Review,AboutUs,FAQ,Vacancy,PromoCode
from .forms import ServiceForm,CustomerRegistrationForm,OrderForm,OrderUpdateForm,ServiceTypeForm,EmployeeSpecializationForm,ReviewForm,FAQForm,AnswerForm,VacancyForm,PromoCodeForm,NewsForm,FullOrderForm,EmployeeForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User,Group
from django.db.models import Sum, Avg, Count
from django.core.exceptions import ObjectDoesNotExist
import re
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
###################
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Получение логера для текущего модуля
logger = logging.getLogger(__name__)

def index(request):
    sort_services(request)
    return index_btn(request)



def index_btn(request):
    is_auth = request.user.is_authenticated
    services = sort_services(request)
    user_is_superuser = request.user.is_superuser
    is_employee = request.user.groups.filter(name='Employee').exists()
    is_customer = request.user.groups.filter(name='Customer').exists()
    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'delete' and request.user.is_superuser:
            service_title = request.POST.get('service_title')
            try:
                service = Service.objects.get(title=service_title)
                service.delete()
            except Service.DoesNotExist:
                pass
        elif 'action' in request.POST and request.POST['action'] == 'edit':
            service_title = request.POST.get('service_title')
            try:
                service = Service.objects.get(title=service_title)
                service_types = ServiceType.objects.all()
                return render(request,"main/edit_service.html",{'service': service,
                                                                'service_types': service_types,
                                                                'user_is_superuser': user_is_superuser})
            except Service.DoesNotExist:
                pass
        elif 'action' in request.POST and request.POST['action'] == 'update':
            service_title = request.POST.get('service_title')
            try:
                service = Service.objects.get(title=service_title)
                if user_is_superuser and request.POST.get('title').strip():
                    service.title = request.POST.get('title')
                if request.POST.get('description').strip():
                    service.description = request.POST.get('description')
                if request.POST.get('price').strip():
                    service.price = request.POST.get('price')
                logger.debug(f"{service.title},{service.description},{service.price}")
                service_type_title = request.POST.get('service_type')
                service_type = ServiceType.objects.get(id=service_type_title)
                service.service_type = service_type
                service.save()
                return redirect('home')
            except Service.DoesNotExist:
                pass
        elif 'action' in request.POST and request.POST['action'] == 'buy':
            service_title = request.POST.get('service_title')
            service = Service.objects.get(title=service_title)
            customer = Customer.objects.get(user=request.user)
            customer.cart.add(service)
    elif request.method == 'GET':
        search_service_title = request.GET.get('service_title',None)
        print(search_service_title)
        if search_service_title is not None and search_service_title.strip()!= "":
            regex = re.escape(search_service_title)
            services = services.filter(title__iregex=regex)
            print(services.values("title"))
    return render(request,"main/index.html",
                  {'services' : services,
                   'user_is_superuser': user_is_superuser,
                   'is_authenticated':is_auth,
                   'is_employee':is_employee,
                   "is_customer":is_customer})




def about(request):
    logger.info('In about us')

    user_is_superuser = request.user.is_superuser
    is_employee = request.user.groups.filter(name='Employee').exists()
    inforamation = AboutUs.objects.all()
    return render(request,"main/about.html",{'informations':inforamation})

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
    return render(request,"main/create.html",context)


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
    return render(request, 'main/register_customer.html', {'user_form': user_form, 'customer_form': customer_form})


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
    return render(request, 'main/login.html', {'form': form})

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
        if is_superuser:
            return render(request, 'main/profile.html',{'user': request.user, 'is_superuser': is_superuser,'is_employee':is_employee,'user_zone':user_zone})
        elif is_employee:
            employee = Employee.objects.get(user=request.user)
            return render(request, 'main/profile.html', {'nickname': request.user, 'user': employee,'is_superuser': is_superuser,'is_employee':is_employee,'user_zone':user_zone})
        else:
            try:
                customer = Customer.objects.get(user=request.user)
                return render(request, 'main/profile.html', {'nickname': request.user, 'user': customer, 'is_superuser': is_superuser,'is_employee':is_employee,'user_zone':user_zone})
            except Customer.DoesNotExist:
                logger.error('Error: Customer.DoesNotExist')
                return render(request, 'main/profile.html', {'user': request.user, 'is_superuser': is_superuser,'is_employee':is_employee,'user_zone':user_zone})
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
                employee = Employee(user=user, full_name=customer.full_name, work_phone=customer.contact_phone)
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
                customer = Customer(user=user, full_name=employee.full_name, contact_phone=employee.work_phone,customer_type='individual')
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
        return render(request, 'main/management.html', {'employees': employees, 'customers': customers})


def employee_detail(request, employee_id):
    logger.info('In employee profile')
    user_is_superuser = request.user.is_superuser
    employee = get_object_or_404(Employee, id=employee_id)
    orders = Order.objects.filter(employee_id=employee_id)
    return render(request, 'main/employee_detail.html', {
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
    return render(request, 'main/update_employee.html', {'form': form, 'employee': employee})

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

    return render(request, 'main/customer_detail.html', {
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
        return render(request, "main/edit_profile.html", {'form': form, 'is_employee': is_employee})

    elif is_customer:
        customer = get_object_or_404(Customer, user=user)
        if request.method == 'POST':
            form = CustomerRegistrationForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = CustomerRegistrationForm(instance=customer)
        return render(request, "main/edit_profile.html", {'form': form, 'is_customer': is_customer})

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
    return render(request, 'main/order.html', {'form': form})

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

    return render(request, 'main/myorders.html', {
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
    return render(request, 'main/update_order.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Employee').exists(), login_url='login')
def unassigned_orders(request):
    logger.info('employee is looking for orders')
    orders = Order.objects.filter(employee__isnull=True)
    return render(request, 'main/unassigned_orders.html', {'orders': orders})

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
    return render(request, 'main/edit_order.html', {'form': form})

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

    return render(request, 'main/add_employee_specialization.html', {
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

    return render(request, 'main/add_service_type.html', {
        'form': form,
        'servicetypes': servicetypes,
        'editing': editing,
        'servicetype': servicetype,
    })

@user_passes_test(lambda u: u.is_superuser)
def adminpanel(request):
    return render(request, 'main/AdminPanel.html')


def news_view(request):
    if request.method == 'POST' and (request.user.groups.filter(name='Employee').exists() or request.user.is_superuser):
        form = NewsForm(request.POST, request.FILES)  # Добавляем request.FILES
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm()
    news_list = News.objects.all()
    return render(request, 'main/news.html', {
        'news_list': news_list,
        'form': form,
        'is_employee': request.user.groups.filter(name='Employee').exists(),
        'user_is_superuser': request.user.is_superuser
    })


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
    return render(request, 'main/statistics.html', context)


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
