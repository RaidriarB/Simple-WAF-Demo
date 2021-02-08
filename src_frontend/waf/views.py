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