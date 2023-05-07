"""
自定义的分页组件，使用说明：

在后端页面中：
def pretty_list(request):

    # 1. 根据自己的情况筛选数据
    queryset = models.PrettyNum.objects.filter(**data_dict)

    # 2. 实例化分页对象
    page_object = Pagination(request,queryset)

    context = {
        'queryset': page_object.page_queryset,
        "page_string": page_object.html(),
    }

    return render(request, 'pretty_list.html', context)

在前段页面中：

    {% for obj in queryset %}
        {{ obj.xx }}
    {% endfor %}

    <ul class="pagination">
        {{ page_string}}
    </ul>

"""

from django.utils.safestring import mark_safe

class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        page = str(request.GET.get(page_param, 1))
        self.page_param = page_param

        # 解决分页和搜索不能同时存在的bug
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True      # 使得query_dict = request.GET中的参数可改动
        self.query_dict = query_dict

        # 数据校验
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        self.total_page_count = (total_count + page_size - 1) / page_size
        self.plus = plus

    def html(self):
        if self.page > 5:
            start_page = self.page - 5
        else:
            start_page = 1
        if self.page + 5 < self.total_page_count:
            end_page = self.page + 5
        else:
            end_page = self.total_page_count

        page_str_list = []
        page_string = ""
        if self.page == 1:
            previous_page = 1
        else:
            previous_page = self.page - 1

        self.query_dict.setlist(self.page_param, [previous_page])   #只更改url中“page=”的参数
        ele = '''
                    <li>
                    <a href="?{}" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
        '''.format(self.query_dict.urlencode())     #urlencode()函数为获得url后面所有的传入参数
        page_str_list.append(ele)

        for i in range(start_page, int(end_page + 1)):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)  # 利用格式化生成分页语句
            page_str_list.append(ele)

        if self.page == self.total_page_count:
            next_page = self.page
        else:
            next_page = self.page + 1
        self.query_dict.setlist(self.page_param, [next_page])
        ele = '''
                    <li>
                    <a href="?{}" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>
        '''.format(self.query_dict.urlencode())
        page_str_list.append(ele)

        page_string = mark_safe("".join(page_str_list))  # 前段语句输入到“page_string"中

        return(page_string)
