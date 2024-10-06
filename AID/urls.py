
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
    path('admin_view_user_search', views.admin_view_user_search),
    path('user_reg', views.user_reg),
    path('verify_driver', views.verify_driver),
    path('verify_driver_search', views.verify_driver_search),
    path('admin_verify_accept/<id>', views.admin_verify_accept),
    path('reject_verify_accept/<id>', views.reject_verify_accept),

    path('user_home', views.user_home),
    path('viewmore_driver/<int:id>', views.viewmore_driver),
    path('viewmore_user/<int:id>', views.viewmore_user),

    path('user_view_profile', views.user_view_profile),
    path('user_edit_profile', views.user_edit_profile),
    path('user_edit_profile_post', views.user_edit_profile_post),
    path('driver_profile', views.driver_profile),
    path('driver_edit_profile', views.driver_edit_profile),
    path('driver_edit_post', views.driver_edit_post),
    path('user_view_driver', views.user_view_driver),
    path('user_view_driver_search', views.user_view_driver_search),
    path('block_driver/<int:id>', views.block_driver),
    path('unblock_driver/<int:id>', views.unblock_driver),
    path('send_request/<int:id>', views.send_request),
    path('chatwithuser', views.chatwithuser, name='chatwithuser'),
    path('chatview', views.chatview, name='chatview'),
    path('coun_msg/<int:id>', views.coun_msg, name='coun_msg'),
    path('coun_insert_chat/<str:msg>/<int:id>', views.coun_insert_chat, name='coun_insert_chat'),
    path('chatwithuserdr', views.chatwithuserdr, name='chatwithuserdr'),
    path('chatviewdr', views.chatviewdr, name='chatviewdr'),
    path('coun_msgdr/<int:id>', views.coun_msgdr, name='coun_msgdr'),
    path('coun_insert_chatdr/<str:msg>/<int:id>', views.coun_insert_chatdr, name='coun_insert_chatdr'),

]
