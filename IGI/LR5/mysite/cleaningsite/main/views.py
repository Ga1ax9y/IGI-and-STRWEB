from django.shortcuts import render,redirect,get_object_or_404
import matplotlib.pyplot
from .models import Service,Customer,ServiceType,Employee,EmployeeSpecialization,Order,News,Review,AboutUs,FAQ,Vacancy,PromoCode
from .forms import ServiceForm,CustomerRegistrationForm,OrderForm,OrderUpdateForm,ServiceTypeForm,EmployeeSpecializationForm,ReviewForm,FAQForm,AnswerForm,VacancyForm,PromoCodeForm
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
import pytz
# Create your views here.


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
                                                                'service_types': service_types})
            except Service.DoesNotExist:
                pass
        elif 'action' in request.POST and request.POST['action'] == 'update':
            service_title = request.POST.get('service_title')
            try:
                service = Service.objects.get(title=service_title)
                service.description = request.POST.get('description')
                service.price = request.POST.get('price')
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
    user_is_superuser = request.user.is_superuser
    is_employee = request.user.groups.filter(name='Employee').exists()
    inforamation = AboutUs.objects.all()
    return render(request,"main/about.html",{'informations':inforamation})

@user_passes_test(lambda u: u.is_superuser)
def create(request):
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
                pass
            user.groups.add(customer_group)
        return redirect('management')
    else:
        employees = Employee.objects.all()
        customers = Customer.objects.all()
        return render(request, 'main/management.html', {'employees': employees, 'customers': customers})


def employee_detail(request, employee_id):
    user_is_superuser = request.user.is_superuser
    employee = get_object_or_404(Employee, id=employee_id)
    orders = Order.objects.filter(employee_id=employee_id)
    return render(request, 'main/employee_detail.html', {'employee': employee,'orders':orders,'user_is_superuser':user_is_superuser})

def customer_detail(request, customer_id):
    user_is_superuser = request.user.is_superuser
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer_id=customer_id)
    return render(request, 'main/customer_detail.html', {'customer': customer,'orders':orders,'user_is_superuser':user_is_superuser})


def user_edit(request):
    user = request.user
    is_employee = user.groups.filter(name='Employee').exists()
    is_customer = user.groups.filter(name='Customer').exists()
    if is_employee:
        employee = Employee.objects.get(user=user)
        specializations = EmployeeSpecialization.objects.all()
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            specializations_ids = request.POST.getlist('specializations')
            photo = request.FILES.get('photo')
            work_phone = request.POST.get('work_phone')
            work_email = request.POST.get('work_email')
            description = request.POST.get('description')
            selected_specializations = request.POST.getlist('specializations')
            birth_date = request.POST.get('birth_date')

            employee.full_name = full_name
            employee.work_phone = work_phone
            employee.work_email = work_email
            employee.description = description
            employee.specializations.set(selected_specializations)
            employee.birth_date = birth_date

            employee.specializations.clear()
            for specialization_id in specializations_ids:
                specialization = EmployeeSpecialization.objects.get(id=specialization_id)
                employee.specializations.add(specialization)

            if photo:
                employee.photo = photo

            employee.save()
            return redirect('profile')
        return render(request,"main/edit_profile.html",{'user': employee,
                                                        'is_customer':is_customer,
                                                        'is_employee':is_employee,
                                                        'specializations': specializations})
    elif is_customer:
        customer = Customer.objects.get(user=user)
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            company_name = request.POST.get('company_name')
            contact_phone = request.POST.get('contact_phone')
            customer_type = request.POST.get('customer_type')

            customer.full_name = full_name
            customer.company_name = company_name
            customer.contact_phone = contact_phone
            customer.customer_type = customer_type
            customer.save()
            return redirect('profile')

        return render(request,"main/edit_profile.html",{'user': customer,
                                                        'is_customer':is_customer,
                                                        'is_employee':is_employee})

def cart_view(request):
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
    return render(request, 'main/myorders.html',
                  {'orders': orders_data,
                   'user_is_superuser': user_is_superuser,
                   'is_employee':is_employee,
                   "is_customer":is_customer,
                   'employees': employees,
                   'selected_employee_id': employee_id,
                   'sort_direction': sort_direction})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Employee').exists(), login_url='login')
def unassigned_orders(request):

    orders = Order.objects.filter(employee__isnull=True)
    return render(request, 'main/unassigned_orders.html', {'orders': orders})


def edit_order(request, order_id):
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
    spezializations = EmployeeSpecialization.objects.all()
    if request.method == 'POST':
        form = EmployeeSpecializationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')
    else:
        form = EmployeeSpecializationForm()
    return render(request, 'main/add_employee_specialization.html', {'form': form,
                                                                     'spezializations':spezializations})

@user_passes_test(lambda u: u.is_superuser)
def add_service_type(request):
    servicetypes = ServiceType.objects.all()
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminpanel')
    else:
        form = ServiceTypeForm()
    return render(request, 'main/add_service_type.html', {'form': form,
                                                          'servicetypes':servicetypes})

@user_passes_test(lambda u: u.is_superuser)
def adminpanel(request):
    return render(request, 'main/AdminPanel.html')


def news_view(request):
    news_list = News.objects.all()
    return render(request, 'main/news.html', {'news_list': news_list})


def reviews_list(request):
    is_customer = request.user.groups.filter(name='Customer').exists()
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

    return render(request, 'main/reviews_list.html', {'reviews': reviews, 'form': form,'is_customer':is_customer})


@login_required
def faq_list(request):
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
    return render(request, 'main/faq_list.html', {'faqs': faqs, 'form': form, 'is_employee': is_employee,'user_is_superuser':user_is_superuser})

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

@login_required
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

@login_required
def promo_codes(request):
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
        'user_is_superuser': request.user.is_superuser
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
