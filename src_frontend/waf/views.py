from django.http import HttpResponse
from django.views import generic

from .models import Log,Rule,Fulllog
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
    FulllogGet = Fulllog.objects.get(log = logGet)
    print(FulllogGet)
    return render(request, 'waf/log_detail.html', {"log": logGet,'Fulllog':FulllogGet})

def log_del(request,nid):  #删除
    Log.objects.filter(id=nid).delete()
    return redirect("log")