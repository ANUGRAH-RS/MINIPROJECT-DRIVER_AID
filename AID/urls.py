
from django.urls import path, include

from AID import views

urlpatterns = [
    path('',views.home),
    path('log',views.log),
    path('login_code',views.login_code),
    path('admin', views.admin),
    path('driver', views.driver),
    path('driver_reg', views.driver_reg),
    path('user', views.user),
    path('admin_view_user', views.admin_view_user),
    path('user_reg', views.user_reg),
    path('verify_driver', views.verify_driver),
    path('admin_verify_accept/<id>', views.admin_verify_accept),
    path('reject_verify_accept/<id>', views.reject_verify_accept),

    path('user_home', views.user_home),
    path('viewmore_driver/<int:id>', views.viewmore_driver),
    path('viewmore_user/<int:id>', views.viewmore_user),

    path('driver_profile', views.driver_profile),
    path('driver_edit_profile', views.driver_edit_profile),
    path('driver_edit_post', views.driver_edit_post),
    path('block_driver', views.block_driver),
    path('unblock_driver', views.unblock_driver),

]
