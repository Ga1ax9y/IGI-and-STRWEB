from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('tags', views.tags, name="tags"),
    path('about',views.about,name="about"),
    path('create',views.create,name="create"),
    path('register_customer', views.register_customer, name='register_customer'),
    path('login',views.user_login,name='login'),
    path('profile',views.user_profile,name='profile'),
    path('management',views.user_management,name='management'),
    path('edit_profile',views.user_edit,name='edit_profile'),
    path('cart', views.cart_view, name='cart'),
    path('order', views.make_order, name='order'),
    path('slider/', views.slider_view, name='slider_view'),
    path('myorders/', views.view_orders, name='orders'),
    path('unassigned-orders/', views.unassigned_orders, name='unassigned_orders'),
    path('add_specialization/', views.add_employee_specialization, name='add_specialization'),
    path('add_service_type/', views.add_service_type, name='add_service_type'),
    path('graph', views.graph_view, name='graph_view'),
    path('news', views.news_view, name='news'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('reviews/', views.reviews_list, name='reviews_list'),
    path('faq/', views.faq_list, name='faq_list'),
    path('faq/answer/<int:faq_id>/', views.answer_faq, name='answer_faq'),
    path('contacts/', views.contacts, name='contacts'),
    path('contact_table/', views.contact_table, name='contact_table'),
    re_path(r'^politics', views.politics, name='politics'),
    re_path(r'^vacancies', views.vacancies, name='vacancies'),
    re_path('^promo_codes', views.promo_codes, name='promo_codes'),
    path('api_combined/', views.api_combined_view, name='api_combined_view'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('adminpanel', views.adminpanel, name='adminpanel'),
    path('task7/', views.task7, name='task7'),
    path('employee/<int:employee_id>/update/', views.update_employee, name='update_employee'),
    path('update_order/<int:order_id>', views.update_order, name='update_order'),
    path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('<int:year>/<int:month>/<int:day>/<int:id>/', views.service_detail,
        name='service_detail'),

]
