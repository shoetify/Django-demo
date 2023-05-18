from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def task_list(request):
    """任务列表"""
    return render(request, "task_list.html")

@csrf_exempt
def task_ajax(request):
    print(request.POST)

    return HttpResponse("成功了")