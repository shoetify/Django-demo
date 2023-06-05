from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """数据统计页面"""
    return render(request, "chart_list.html")


def chart_bar(request):
    """构造一个柱状图数据"""
    legend = ['销量']
    xAxis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    data_list = [
        {
            "name": '销量',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20],
        },
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            "xAxis": xAxis,
            "data_list": data_list,
        }
    }

    return JsonResponse(result)
