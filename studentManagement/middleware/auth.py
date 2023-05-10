from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    """中间件1"""

    def process_request(self, request):
        # 如果方法中没有返回值（返回None），则会继续运行后面的中间件
        # 如果有返回值（返回值，HttpResponse, render, redirect等）则会从这个中间件跳出，不运行后面的中间件

        # 1. 如果请求的页面是登录页面， 则不作检查
        if request.path_info in ["/login", "/image/code"]:
            return

        # 2. 读取当前访问用户的session新信息
        info_dict = request.session.get('info')

        # 3. 如果有信息（已经登陆过），则继续往后走
        # 4. 如果没有登陆过（重定向至登录页面）
        if not info_dict:
            return redirect('/login')

        # print("M1.process_request")
        # return redirect(/login)
