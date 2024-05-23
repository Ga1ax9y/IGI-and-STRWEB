from django.test import TestCase
from django.contrib.auth.models import User
from .models import Customer, Service, ServiceType, Employee, Order, PromoCode,EmployeeSpecialization
from datetime import date
from .forms import ServiceForm, CustomerRegistrationForm
from django.core.exceptions import ValidationError
class ServiceModelTest(TestCase):

    def setUp(self):
        self.service_type = ServiceType.objects.create(name="Consulting")

    def test_service_creation(self):
        service = Service.objects.create(
            title="Test Service",
            description="This is a test service description.",
            price=200,
            service_type=self.service_type
        )
        self.assertIsInstance(service, Service)
        self.assertEqual(service.title, "Test Service")
        self.assertEqual(service.description, "This is a test service description.")
        self.assertEqual(service.price, 200)
        self.assertEqual(service.service_type, self.service_type)

    def test_service_str_representation(self):
        service = Service.objects.create(
            title="Test Service",
            description="This is a test service description.",
            price=200,
            service_type=self.service_type
        )
        self.assertEqual(str(service), "Test Service")

    def test_service_default_price(self):
        service = Service.objects.create(
            title="Test Service",
            description="This is a test service description.",
            service_type=self.service_type
        )
        self.assertEqual(service.price, 100)

    def test_service_type_relationship(self):
        service = Service.objects.create(
            title="Test Service",
            description="This is a test service description.",
            price=200,
            service_type=self.service_type
        )
        self.assertEqual(service.service_type.name, "Consulting")


class CustomerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.service_type = ServiceType.objects.create(name="Consulting")
        self.service = Service.objects.create(
            title="Test Service",
            description="This is a test service description.",
            price=200,
            service_type=self.service_type
        )

    def test_customer_creation(self):
        customer = Customer.objects.create(
            user=self.user,
            full_name="Test Customer",
            birth_date=date(2000, 1, 1),
            company_name="Test Company",
            contact_phone="1234567890",
            customer_type="individual"
        )
        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.full_name, "Test Customer")
        self.assertEqual(customer.birth_date, date(2000, 1, 1))
        self.assertEqual(customer.company_name, "Test Company")
        self.assertEqual(customer.contact_phone, "1234567890")
        self.assertEqual(customer.customer_type, "individual")

    def test_customer_str_representation(self):
        customer = Customer.objects.create(
            user=self.user,
            full_name="Test Customer",
            birth_date=date(2000, 1, 1),
            company_name="Test Company",
            contact_phone="1234567890",
            customer_type="individual"
        )
        self.assertEqual(str(customer), "Test Customer")


class EmployeeModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='employeeuser', password='12345')
        self.specialization = EmployeeSpecialization.objects.create(name="Specialization")

    def test_employee_creation(self):
        employee = Employee.objects.create(
            user=self.user,
            full_name="Test Employee",
            birth_date=date(2000, 1, 1),
            work_phone="0987654321",
            work_email="test@example.com",
            description="This is a test employee description."
        )
        employee.specializations.add(self.specialization)
        self.assertIsInstance(employee, Employee)
        self.assertEqual(employee.full_name, "Test Employee")
        self.assertEqual(employee.birth_date, date(2000, 1, 1))
        self.assertEqual(employee.work_phone, "0987654321")
        self.assertEqual(employee.work_email, "test@example.com")
        self.assertEqual(employee.description, "This is a test employee description.")
        self.assertIn(self.specialization, employee.specializations.all())

    def test_employee_str_representation(self):
        employee = Employee.objects.create(
            user=self.user,
            full_name="Test Employee",
            birth_date=date(2000, 1, 1),
            work_phone="0987654321",
            work_email="test@example.com",
            description="This is a test employee description."
        )
        self.assertEqual(str(employee), "Test Employee")

class OrderModelTest(TestCase):

    def setUp(self):
        self.user_customer = User.objects.create_user(username='customeruser', password='12345')
        self.user_employee = User.objects.create_user(username='employeeuser', password='12345')
        self.customer = Customer.objects.create(
            user=self.user_customer,
            full_name="Test Customer",
            birth_date=date(2000, 1, 1),
            contact_phone="1234567890",
            customer_type="individual"
        )
        self.employee = Employee.objects.create(
            user=self.user_employee,
            full_name="Test Employee",
            birth_date=date(2000, 1, 1)
        )
        self.service_type = ServiceType.objects.create(name="Consulting")
        self.service = Service.objects.create(
            title="Test Service",
            description="This is a test service description.",
            price=200,
            service_type=self.service_type
        )
        self.promo_code = PromoCode.objects.create(
            code="PROMO10",
            description="10% off",
            is_active=True,
            valid_until=date(2025, 1, 1),
            discount_coefficient=0.9
        )

    def test_order_creation(self):
        order = Order.objects.create(
            order_code="ORD123",
            address="123 Test St",
            customer=self.customer,
            employee=self.employee,
            promo_code=self.promo_code
        )
        order.services.add(self.service)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.order_code, "ORD123")
        self.assertEqual(order.address, "123 Test St")
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.employee, self.employee)
        self.assertEqual(order.promo_code, self.promo_code)
        self.assertIn(self.service, order.services.all())

    def test_order_str_representation(self):
        order = Order.objects.create(
            order_code="ORD123",
            address="123 Test St",
            customer=self.customer,
            employee=self.employee
        )
        self.assertEqual(str(order), "ORD123")

    def test_order_total_cost_with_promo_code(self):
        order = Order.objects.create(
            order_code="ORD123",
            address="123 Test St",
            customer=self.customer,
            employee=self.employee,
            promo_code=self.promo_code
        )
        order.services.add(self.service)
        self.assertEqual(order.total_cost(), 180.0)  # 200 * 0.9

    def test_order_total_cost_without_promo_code(self):
        order = Order.objects.create(
            order_code="ORD123",
            address="123 Test St",
            customer=self.customer,
            employee=self.employee
        )
        order.services.add(self.service)
        self.assertEqual(order.total_cost(), 200.0)


class PromoCodeModelTest(TestCase):

    def test_promo_code_creation(self):
        promo_code = PromoCode.objects.create(
            code="PROMO10",
            description="10% off",
            is_active=True,
            valid_until=date(2025, 1, 1),
            discount_coefficient=0.9
        )
        self.assertIsInstance(promo_code, PromoCode)
        self.assertEqual(promo_code.code, "PROMO10")
        self.assertEqual(promo_code.description, "10% off")
        self.assertTrue(promo_code.is_active)
        self.assertEqual(promo_code.valid_until, date(2025, 1, 1))
        self.assertEqual(promo_code.discount_coefficient, 0.9)

    def test_promo_code_str_representation(self):
        promo_code = PromoCode.objects.create(
            code="PROMO10",
            description="10% off",
            is_active=True,
            valid_until=date(2025, 1, 1),
            discount_coefficient=0.9
        )
        self.assertEqual(str(promo_code), "PROMO10")

    def test_promo_code_is_valid(self):
        promo_code = PromoCode.objects.create(
            code="PROMO10",
            description="10% off",
            is_active=True,
            valid_until=date(2023, 1, 1),
            discount_coefficient=0.9
        )
        promo_code.is_valid()
        self.assertFalse(promo_code.is_active)



class ServiceFormTest(TestCase):
    def setUp(self):
        self.service_type = ServiceType.objects.create(name="Test Service Type")

    def test_service_form_valid_data(self):
        form = ServiceForm(data={
            'title': 'Test Service',
            'description': 'This is a test service.',
            'price': 100,
            'service_type': self.service_type.id
        })
        self.assertTrue(form.is_valid())

    def test_service_form_invalid_data(self):
        form = ServiceForm(data={
            'title': '',
            'description': 'This is a test service.',
            'price': 100,
            'service_type': self.service_type.id
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

class CustomerRegistrationFormTest(TestCase):
    def test_customer_registration_form_valid_data(self):
        form = CustomerRegistrationForm(data={
            'full_name': 'Test User',
            'birth_date': '01/01/2000',
            'company_name': 'Test Company',
            'contact_phone': '+375 (29) 123-45-67',
            'customer_type': 'individual'
        })
        self.assertTrue(form.is_valid())

    def test_customer_registration_form_invalid_phone(self):
        form = CustomerRegistrationForm(data={
            'full_name': 'Test User',
            'birth_date': '01/01/2000',
            'company_name': 'Test Company',
            'contact_phone': '12345',
            'customer_type': 'individual'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('contact_phone', form.errors)


    def test_customer_registration_form_invalid_birth_date(self):
        form = CustomerRegistrationForm(data={
            'full_name': 'Test User',
            'birth_date': 'invalid-date',
            'company_name': 'Test Company',
            'contact_phone': '+375 (29) 123-45-67',
            'customer_type': 'individual'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)
