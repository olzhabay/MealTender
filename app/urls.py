from django.conf.urls import url, include
from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^add/$', views.add_to_cart, name='shopping-cart-add'),
    url(r'^remove/$', views.remove_from_cart, name='shopping-cart-remove'),
    url(r'^show_cart/$', views.show_cart, name='shopping-cart-show'),
    url(r'^food_list/(\d+)/$', views.food_list, name='food_list'),
    url(r'^restaurant_list/$', views.restaurant_list, name='restaurant_list'),
]
