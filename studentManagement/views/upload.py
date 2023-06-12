from django.shortcuts import render, HttpResponse
from django import forms
from studentManagement.utils.bootstrap import BootStrapForm
import os
from studentManagement import models

from student.student import settings


def upload_list(request):
    """上传文件"""
    if request.method == "GET":
        return render(request, "upload_list.html")

    file_object = request.FILES.get("avatar")

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("...")


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    title = "Form上传"

    if request.method == "GET":
        form = UpForm()
        context = {
            "title": title,
            "form": form,
        }
        return render(request, "upload_form.html", context)

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 1. 读取图片内容，写入到文件夹中并获取文件的路径
        image_object = form.cleaned_data.get("img")

        # file_path = "studentManaqement/static/files/{}".format(image_object.name)
        file_path = os.path.join(settings.MEDIA_ROOT, image_object.name)

        f = open(file_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 2. 把文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=file_path,
        )

        return HttpResponse("...")

    return render(request, "upload_form.html", {"form": form, "title": title})
