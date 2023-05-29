import json
import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from studentManagement.utils.bootstrap import BootStrapModelForm
from studentManagement import models
from studentManagement.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # 该语句会将Order的全部属性生成为表
        # fields = "__all__"

        # oid（订单号）不需要生成为表
        exclude = ["oid", "admin"]


def order_list(request):
    """订单列表"""

    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = OrderModelForm()

    context = {
        'form': form,
        'queryset': page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    """新建订单（Ajax请求）"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 系统自动填写oid数据
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 获取管理员数据
        form.instance.admin_id = request.session["info"]["id"]

        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request):
    """删除订单"""
    uid = request.GET.get('uid')
    print(uid)
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """根据ID获取订单数据"""
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    result = {
        "status": True,
        "data": row_dict,
    }

    return JsonResponse({"status": True, "data": result})
