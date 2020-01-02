# from haystack.views import SearchView
from haystack.generic_views import SearchView

from goods.models import GoodsType


class GoodsSearchView(SearchView):
    # def extra_context(self):
    #     context = super(GoodsSearchView, self).extra_context()
    #     types = GoodsType.objects.all()
    #     context['types'] = types
    #     return context

    # def get_context_data(self, *args, **kwargs):
    #     # context = super(GoodsSearchView, self).get_context_data(*args, **kwargs)
    #     types = GoodsType.objects.all()
    #     # context['types'] = types
    #     context = super(SearchView, self).get_context_data(**kwargs)
    #     context.update({'facets': self.queryset.facet_counts()})
    #     context.update({'types': types})
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(GoodsSearchView, self).get_context_data(*args, **kwargs)
        types = GoodsType.objects.all()
        context.update({'types': types})
        return context
    pass
