from django.shortcuts import render, redirect
from studentManagement import models
from studentManagement.utils.pagination import Pagination
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms

def pretty_list(request):
    """靓号列表"""

    # # 根据用户访问的页码，计算出分页相关的数据
    # page = int(request.GET.get('page', 1))
    # pageSize = 10
    # startNum = (page - 1) * pageSize
    # endNum = page * pageSize

    # 搜索号码
    data_dict = {}
    value = request.GET.get('q')  # value获取url中 “?q=..." 的内容
    if value:
        # 如果搜索了内容（也就是q有值），则搜索字典的内容，否则则输出全部
        data_dict["mobile__contains"] = value

    queryset = models.PrettyNum.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset

    # total_page = (total_count + pageSize - 1) / pageSize

    # if page > 5:
    #     start_page = page - 5
    # else:
    #     start_page = 1
    # if page + 5 < total_page:
    #     end_page = page + 5
    # else:
    #     end_page = total_page
    #
    # page_str_list = []
    # page_string = ""
    # if page == 1:
    #     previous_page = 1
    # else:
    #     previous_page = page - 1
    # ele = '''
    #             <li>
    #             <a href="?page={}" aria-label="Previous">
    #                 <span aria-hidden="true">&laquo;</span>
    #             </a>
    #         </li>
    # '''.format(previous_page)
    # page_str_list.append(ele)
    #
    # for i in range(start_page, int(end_page + 1)):
    #     if i == page:
    #         ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)  # 利用格式化生成分页语句
    #     page_str_list.append(ele)
    #
    # if page == total_page:
    #     next_page = page
    # else:
    #     next_page = page + 1
    # ele = '''
    #             <li>
    #             <a href="?page={}" aria-label="Next">
    #                 <span aria-hidden="true">&raquo;</span>
    #             </a>
    #         </li>
    # '''.format(next_page)
    # page_str_list.append(ele)
    #
    # page_string = mark_safe("".join(page_str_list))  # 前段语句输入到“page_string"中
    page_string = page_object.html()
    context = {
        'queryset': page_queryset,
        "page_string": page_string,
    }

    return render(request, 'pretty_list.html', context)

class PrettyModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^04\d{8}', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件， 添加了“class”： “form-control”
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_price(self):  # clean_ 后面跟着需要验证的字段
        txt_price = self.cleaned_data["price"]  # 获取该字段的值
        if txt_price < 0:
            raise ValidationError("价格需大于0")  # 抛出异常（错误信息）
        return txt_price  # 验证通过，返回原值

    def clean_mobile(self):
        # 通过查询数据库的方式放置手机号重复

        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()

        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

def pretty_add(request):
    """添加靓号"""

    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {'form': form})

    # 用户POST提交数据，进行数据校验
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list")

    return render(request, 'Pretty_add.html', {"form": form})

class PrettyModelForm1(forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        disabled=True,
        validators=[RegexValidator(r'^04\d{8}', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件， 添加了“class”： “form-control”
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_price(self):  # clean_ 后面跟着需要验证的字段
        txt_price = self.cleaned_data["price"]  # 获取该字段的值
        if txt_price < 0:
            raise ValidationError("价格需大于0")  # 抛出异常（错误信息）
        return txt_price  # 验证通过，返回原值

def pretty_edit(request, nid):
    """编辑靓号"""

    # 根据ID去数据库获取要编辑的那一行数据（对象）
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyModelForm1(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    form = PrettyModelForm1(data=request.POST, instance=row_object)

    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    return render(request, 'pretty_edit.html', {'form': form})