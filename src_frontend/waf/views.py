from django.core import paginator
from django.http import HttpResponse,request
from django.views import generic,View

from .models import Log,Rule,Fulllog,Whitelist,Blacklist

from django.db.models import Count
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import socket
def update_rules():
    signal = "<-UPDATE->"
    s = socket.socket()
    s.connect(("0.0.0.0", 12345))
    s.sendall(signal.encode())


class RuleView(generic.ListView):
    template_name = 'waf/rule.html'
    context_object_name = 'rule_list'

    def get_queryset(self):
        return Rule.objects.all()

def index(request):
    rulesum,flowsum,passrate,blockrate,lograte = 0,0,0,0,0

    rulesum = Rule.objects.all().aggregate(Count('id'))['id__count']
    flowsum = Log.objects.all().aggregate(Count('id'))['id__count']

    psum = Log.objects.filter(action='PASS').aggregate(Count('id'))['id__count']
    bsum = Log.objects.filter(action='BLOCK').aggregate(Count('id'))['id__count']
    lsum = Log.objects.filter(action='LOG').aggregate(Count('id'))['id__count']

    if flowsum == 0:
        passrate,blockrate,lograte = 0,0,0
    else:
        passrate = round(psum*100 / flowsum , 2)
        blockrate = round(bsum*100 / flowsum , 2)
        lograte = round(lsum*100 / flowsum , 2)
    print(rulesum,flowsum,psum,bsum,lsum)

    params = {"rulesum":rulesum,"flowsum":flowsum,"passrate":passrate,"blockrate":blockrate,"lograte":lograte}

    return render(request, 'waf/index.html', params)

class WhitelistView(generic.ListView):
    template_name = 'waf/Whitelist.html'
    context_object_name = 'Whitelist_list'

    def get_queryset(self):
        return Whitelist.objects.all()

class BlacklistView(generic.ListView):
    template_name = 'waf/Blacklist.html'
    context_object_name = 'Blacklist_list'

    def get_queryset(self):
        return Blacklist.objects.all()

def rule_del(request,nid):  #删除
    Rule.objects.filter(id=nid).delete()
    update_rules()
    return redirect("rule")

def rule_edit(request,nid):  #修改
    if request.method=="GET":
        obj=Rule.objects.filter(id=nid).first()
        return render(request, 'waf/rule_edit.html', {"obj": obj})
    elif request.method=="POST":
        contentGet=request.POST.get("content")      #拿到提交的数据
        descriptionGet=request.POST.get("description")
        actionGet = request.POST.get("action")
        Rule.objects.filter(id=nid).update(content = contentGet, description = descriptionGet, action = actionGet)
        update_rules()
        return redirect("rule")

def rule_create(request):
    if request.method=="GET":
        return render(request, 'waf/rule_create.html')
    elif request.method=="POST":
        contentGet=request.POST.get("content")      #拿到提交的数据
        descriptionGet=request.POST.get("description")
        actionGet = request.POST.get("action")
        Rule.objects.create(content = contentGet, description = descriptionGet, action = actionGet)
        update_rules()
        return redirect("rule")

def log_detail(request,nid):
    logGet = Log.objects.filter(id=nid).first()
    FulllogGet = Fulllog.objects.filter(log = logGet).first()
    return render(request, 'waf/log_detail.html', {"log": logGet,'Fulllog':FulllogGet})

def log_del(request,nid):  #删除
    Log.objects.filter(id=nid).delete()
    return redirect("log")
#Whitelist
def Whitelist_del(request,nid):  #删除
    Whitelist.objects.filter(id=nid).delete()
    update_rules()
    return redirect("Whitelist")

def Whitelist_edit(request,nid):  #修改
    if request.method=="GET":
        obj=Whitelist.objects.filter(id=nid).first()
        return render(request, 'waf/Whitelist_edit.html', {"obj": obj})
    elif request.method=="POST":      #拿到提交的数据
        urlGet=request.POST.get("url")
        ipGet = request.POST.get("ip")
        Whitelist.objects.filter(id=nid).update(url = urlGet, ip = ipGet)
        update_rules()
        return redirect("Whitelist")

def Whitelist_create(request):
    if request.method=="GET":
        return render(request, 'waf/Whitelist_create.html')
    elif request.method=="POST":
        urlGet=request.POST.get("url")
        ipGet = request.POST.get("ip")
        Whitelist.objects.create(url = urlGet, ip = ipGet)
        update_rules()
        return redirect("Whitelist")
#Blacklist
def Blacklist_del(request,nid):  #删除
    Blacklist.objects.filter(id=nid).delete()
    update_rules()
    return redirect("Blacklist")

def Blacklist_edit(request,nid):  #修改
    if request.method=="GET":
        obj=Blacklist.objects.filter(id=nid).first()
        return render(request, 'waf/Blacklist_edit.html', {"obj": obj})
    elif request.method=="POST":      #拿到提交的数据
        urlGet=request.POST.get("url")
        ipGet = request.POST.get("ip")
        Blacklist.objects.filter(id=nid).update(url = urlGet, ip = ipGet)
        update_rules()
        return redirect("Blacklist")

def Blacklist_create(request):
    if request.method=="GET":
        return render(request, 'waf/Blacklist_create.html')
    elif request.method=="POST":
        urlGet=request.POST.get("url")
        ipGet = request.POST.get("ip")
        Blacklist.objects.create(url = urlGet, ip = ipGet)
        update_rules()
        return redirect("Blacklist")

def Log_index(request):
    log_list = Log.objects.order_by('-time')
    if request.method=='GET':
        data = split_page(log_list,request)
        data.update({'latest_log_list':data['page'].object_list})
        return render(request,'waf/table.html',data)

def split_page(object_list, request, per_page=20):
    paginator = Paginator(object_list, per_page)
    # 取出当前需要展示的页码, 默认为1
    page_num = request.GET.get('page', default='1')
    # 根据页码从分页器中取出对应页的数据
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger as e:
        # 不是整数返回第一页数据
        page = paginator.page('1')
        page_num = 1
    except EmptyPage as e:
        # 当参数页码大于或小于页码范围时,会触发该异常
        print('EmptyPage:{}'.format(e))
        if int(page_num) > paginator.num_pages:
            # 大于 获取最后一页数据返回
            page = paginator.page(paginator.num_pages)
        else:
            # 小于 获取第一页
            page = paginator.page(1)

    # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
    page_num = int(page_num)
    if page_num < 6:
        if paginator.num_pages <= 10:
            dis_range = range(1, paginator.num_pages + 1)
        else:
            dis_range = range(1, 11)
    elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
        dis_range = range(page_num - 5, page_num + 5)
    else:
        dis_range = range(paginator.num_pages - 9, paginator.num_pages + 1)

    data = {'page': page, 'paginator': paginator, 'dis_range': dis_range }
    return data
