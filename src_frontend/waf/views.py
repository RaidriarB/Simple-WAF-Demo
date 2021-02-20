from django.http import HttpResponse
from django.views import generic

from .models import Log,Rule,Fulllog,Whitelist,Blacklist
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect

class IndexView(generic.TemplateView):
    template_name = 'waf/index.html'

class LogView(generic.ListView):
    template_name = 'waf/table.html'
    context_object_name = 'latest_log_list'

    def get_queryset(self):
        return Log.objects.order_by('time')[:20]

class RuleView(generic.ListView):
    template_name = 'waf/rule.html'
    context_object_name = 'rule_list'

    def get_queryset(self):
        return Rule.objects.all()

class FormView(generic.TemplateView):
    template_name = 'waf/form.html'

class ChartView(generic.TemplateView):
    template_name = 'waf/chart.html'

class EmptyView(generic.TemplateView):
    template_name = 'waf/empty.html'

class TabPanelView(generic.TemplateView):
    template_name = 'waf/tab-panel.html'

class UIElementsView(generic.TemplateView):
    template_name = 'waf/ui-elements.html'

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
        return redirect("rule")

def rule_create(request):
    if request.method=="GET":
        return render(request, 'waf/rule_create.html')
    elif request.method=="POST":
        contentGet=request.POST.get("content")      #拿到提交的数据
        descriptionGet=request.POST.get("description")
        actionGet = request.POST.get("action")
        Rule.objects.create(content = contentGet, description = descriptionGet, action = actionGet)
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
    return redirect("Whitelist")

def Whitelist_edit(request,nid):  #修改
    if request.method=="GET":
        obj=Whitelist.objects.filter(id=nid).first()
        return render(request, 'waf/Whitelist_edit.html', {"obj": obj})
    elif request.method=="POST":      #拿到提交的数据
        urlGet=request.POST.get("url")
        ipGet = request.POST.get("ip")
        Whitelist.objects.filter(id=nid).update(url = urlGet, ip = ipGet)
        return redirect("Whitelist")

def Whitelist_create(request):
    if request.method=="GET":
        return render(request, 'waf/Whitelist_create.html')
    elif request.method=="POST":
        urlGet=request.POST.get("url")
        ipGet = request.POST.get("ip")
        Whitelist.objects.create(url = urlGet, ip = ipGet)
        return redirect("Whitelist")
#Blacklist
def Blacklist_del(request,nid):  #删除
    Blacklist.objects.filter(id=nid).delete()
    return redirect("Blacklist")

def Blacklist_edit(request,nid):  #修改
    if request.method=="GET":
        obj=Blacklist.objects.filter(id=nid).first()
        return render(request, 'waf/Blacklist_edit.html', {"obj": obj})
    elif request.method=="POST":      #拿到提交的数据
        urlGet=request.POST.get("url")
        ipGet = request.POST.get("ip")
        Blacklist.objects.filter(id=nid).update(url = urlGet, ip = ipGet)
        return redirect("Blacklist")

def Blacklist_create(request):
    if request.method=="GET":
        return render(request, 'waf/Blacklist_create.html')
    elif request.method=="POST":
        urlGet=request.POST.get("url")
        ipGet = request.POST.get("ip")
        Blacklist.objects.create(url = urlGet, ip = ipGet)
        return redirect("Blacklist")