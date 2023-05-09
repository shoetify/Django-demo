from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from studentManagement.utils.encrypt import md5

from studentManagement import models
from studentManagement.utils.pagination import Pagination


def admin_list(request):
    """管理员列表"""

    #检查用户是否已经登录，如果已登录，继续走下去，未登录，跳转为登录页面。
    #用户发来请求，获取cookie随机字符串，拿着随机字符串到session中查找
    # info = request.session.get("info")
    # if not info:
    #     return redirect('/login')

    queryset = models.Admin.objects.all()
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, 'admin_list.html', context)


from django import forms
from studentManagement.utils.bootstrap import BootStrapModelForm


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        # 针对“确认密码”的钩子函数

        # 首先获得“密码”和“确认密码”的数据
        pwd = self.cleaned_data.get("password")
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))

        if confirm_pwd != pwd:  # 两个数据不一致，抛出错误（记得导入ValidationError）
            raise ValidationError("密码不一致，请重新输入")

        # 此时记得把原来的值return回去
        return confirm_pwd


def admin_add(request):
    """添加管理员"""
    title = "新建管理员"

    if request.method == 'GET':
        form = AdminModelForm()
        context = {
            "title": title,
            "form": form
        }
        return render(request, 'admin_add.html', context)

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, 'admin_add.html', {'form': form, 'title': title})


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


def admin_edit(request, nid):
    """编辑管理员"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list')

    title = "编辑管理员"

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form': form, 'title': title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, 'admin_edit.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list')


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        # 针对“确认密码”的钩子函数

        # 首先获得“密码”和“确认密码”的数据
        pwd = self.cleaned_data.get("password")
        confirm_pwd = md5(self.cleaned_data.get("confirm_password"))

        if confirm_pwd != pwd:  # 两个数据不一致，抛出错误（记得导入ValidationError）
            raise ValidationError("密码不一致，请重新输入")

        # 此时记得把原来的值return回去
        return confirm_pwd


def admin_reset(request, nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list')

    title = "重置密码 - {}".format(row_object.username)

    if request.method == 'GET':
        form = AdminResetModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, 'admin_edit.html', {'form': form, 'title': title})