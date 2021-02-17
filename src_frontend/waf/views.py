from django.http import HttpResponse
from django.views import generic

from .models import Log


class IndexView(generic.TemplateView):
    template_name = 'waf/index.html'

class LogView(generic.ListView):
    template_name = 'waf/table.html'
    context_object_name = 'latest_log_list'

    def get_queryset(self):
        return Log.objects.order_by('time')[:5]

class RuleView(generic.ListView):
    pass

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