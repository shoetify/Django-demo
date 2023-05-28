"""student URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from studentManagement.views import depart, user, pretty, admin, account, task, order

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 部门管理
    path('depart/list', depart.depart_list),
    path('depart/add', depart.depart_add),
    path('depart/delete', depart.depart_delete),
    path('depart/<int:nid>/edit', depart.depart_edit),

    # 用户管理
    path('user/list', user.user_list),
    path('user/add', user.user_add),
    path('user/model/form/add', user.user_model_form_add),
    path('user/<int:nid>/model/form/edit', user.user_model_form_edit),
    path('user/<int:nid>/delete', user.user_delete),

    # 靓号管理
    path('pretty/list', pretty.pretty_list),
    path('pretty/add', pretty.pretty_add),
    path('pretty/<int:nid>/edit', pretty.pretty_edit),

    # 管理员管理
    path('admin/list', admin.admin_list),
    path('admin/add', admin.admin_add),
    path('admin/<int:nid>/edit', admin.admin_edit),
    path('admin/<int:nid>/delete', admin.admin_delete),
    path('admin/<int:nid>/reset', admin.admin_reset),

    #用户登录
    path('login', account.login),
    path('logout', account.logout),
    path('image/code', account.image_code),

    #任务管理
    path('task/list', task.task_list),
    path('task/ajax', task.task_ajax),

    #订单管理
    path('order/list', order.order_list),
    path('order/add', order.order_add),
    path('order/delete', order.order_delete),
]
