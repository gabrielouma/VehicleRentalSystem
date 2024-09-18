from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.aboutpage),
    path('contactus/', views.contactus),
    path("user_register/", views.user_register, name="user_register"),
    path("password_recovery/", views.password_recovery, name="password_recovery"),
    path("customer_login/", views.customer_login, name="customer_login"),
    path("dealer_login/", views.dealer_login, name="dealer_login"),
    path("logout/", views.signout, name="logout"),
    path("select_vehicle/", views.customer_home, name="select_vehicle"),
    path("dealer_home/", views.dealer_home, name="dealer_home"),
    path("add_vehicle/", views.add_vehicle, name="add_vehicle"),
    path("vehicle_rent/", views.vehicle_rent, name="vehicle_rent"),
    path("order_details/", views.order_details, name="order_details"),
    path("request_vehicle/", views.request_vehicle, name="request_vehicle"),
    path("customer_orders/", views.customer_orders, name="customer_orders"),
    path("delete_order/<int:ord_id>/", views.delete_order_history, name="delete_order"),
    path("user_profile/", views.edit_profile, name="user_profile"),
    path("delete_vehicle/<int:v_id>/", views.delete_vehicle, name="delete_vehicle"),
    path("edit_vehicle/<int:v_id>/", views.edit_vehicle, name="edit_vehicle"),
    path("rented_vehicle/", views.rented_vehicle, name="rented_vehicle"),
    path("dealer_orders/", views.dealer_orders, name="dealer_orders"),
    path("complete_rent_request/", views.complete_rent_request, name="complete_rent_request"),
    path("cancel_rent_request/", views.cancel_rent_request, name="cancel_rent_request"),
    path("accept_rent_request/", views.accept_rent_request, name="accept_rent_request"),
]