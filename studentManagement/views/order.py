from django.shortcuts import render

def order_list(request):
    """订单列表"""

    return render(request, "order_list.html")