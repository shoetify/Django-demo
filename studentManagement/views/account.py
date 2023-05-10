from django.shortcuts import render
from django import forms
from studentManagement import models
from studentManagement.utils.bootstrap import BootStrapForm
from studentManagement.utils.encrypt import md5
from django.shortcuts import redirect, HttpResponse
from studentManagement.utils.checkCode import check_code



# Form 组件的写法
class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,  # 表示该项不能为空
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,  # 表示该项不能为空
    )

    def clean_password(self):
        # 将密码的明文转变为密文
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


# ModelForm 组件的写法
class LoginModelForm(forms.ModelForm):
    class Meta:
        models = models.Admin
        field = ['username', 'password']


def login(request):
    """登录"""

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码

        # 数据库校验用户名和密码是否正确，获取用户对象 或者 None
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()  # 将数据文件（格式为字典）作为语句查询数据库

        # 如果用户名或者密码错误
        if not admin_object:
            form.add_error("password", "用户名或密码错误")  # 主动添加错误信息在password栏显示错误信息
            return render(request, 'login.html', {'form': form})

        # 如果用户名和密码正确
        # 网站需要生成一个随机字符串； 并将‘info'信息写到用户浏览器的cookie中； 再写入到session中；
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}

        return redirect("/admin/list")

    return render(request, 'login.html', {'form': form})


def logout(request):
    """注销"""

    request.session.clear()

    return redirect('/login')


from io import BytesIO
def image_code(request):
    """生成图片验证码"""

    # 调用utils的checkCode函数，生成图片
    img, code_str = check_code()

    #将图片保存在stream中
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


