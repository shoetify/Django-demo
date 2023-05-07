from django.shortcuts import render, redirect
from studentManagement import models
from studentManagement.utils.pagination import Pagination
from django import forms

def user_list(request):
    """ 用户管理 """

    # 去数据库中获取所有的用户列表
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request, queryset, page_size=5)

    context = {
        'queryset': page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, 'user_list.html', context)

def user_add(request):
    """ 增加用户 """
    if request.method == 'GET':
        context = {
            "gender_choice": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all(),
        }
        return render(request, 'user_add.html', context)

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    ac = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gd = request.POST.get('gd')
    dp = request.POST.get('dp')

    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=ac, create_time=ctime, gender=gd,
                                   depart_id=dp)

    return redirect("/user/list")

class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="Name")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "gender", "depart", "create_time", "account"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件， 添加了“class”： “form-control”
        for name, field in self.fields.items():
            if name != "password":
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}

def user_model_form_add(request):
    """添加用户（modelform版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，进行数据校验
    form = UserModelForm(data=request.POST)  # UserModelForm取得POST请求的所有数据，并一一对应
    if form.is_valid():  # 对数据进行校验
        # 校验成功，数据合法，则保存至数据库
        form.save()  # 保存至定义时候的数据表里
        return redirect("/user/list")

    # 校验失败，在页面中显示错误信息
    return render(request, 'user_model_form_add.html', {"form": form})
    # 此时的form已经包含了错误信息，所以会在页面中进行显示

def user_model_form_edit(request, nid):
    """编辑用户"""

    # 根据ID去数据库获取要编辑的那一行数据（对象）
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)

    if form.is_valid():
        form.save()
        return redirect('/user/list')
    return render(request, 'user_edit.html', {'form': form})

def user_delete(request, nid):
    """删除用户"""

    models.UserInfo.objects.filter(id=nid).delete()

    return redirect('/user/list')