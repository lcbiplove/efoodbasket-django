from django.http import request
from django.views.generic.edit import UpdateView
from .models import Notification
from products.models import Product
from django.views.generic import ListView
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse

# Create your views here.
class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    paginate_by = 30

class SearchView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'
    queryset = Product.objects.filter().select_related('shop')
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.request.GET.get('searchBy', '')
        context['search_key'] = self.request.GET.get('q', '')
        context['order_by'] = self.request.GET.get('orderBy', '')
        context['selected_rating'] = self.request.GET.get('rating', '')
        context['selected_min_price'] = self.request.GET.get('minPrice', '')
        context['selected_max_price'] = self.request.GET.get('maxPrice', '')
        context['sorts_by'] = self.get_sorts_by()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        search_category = self.request.GET.get('searchBy')
        order_by = self.request.GET.get('orderBy', '')
        rating = self.request.GET.get('rating', '')
        min_price = self.request.GET.get('minPrice', '')
        max_price = self.request.GET.get('maxPrice', '')

        if query:
            queryset = queryset.filter(name__icontains=query)

        if search_category:
            queryset = queryset.filter(category__id=search_category)

        if rating:
            queryset = queryset.annotate(average_rating=Avg('product_ratings__rating')).filter(average_rating__gte=rating)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if order_by:
            sorts_by = self.get_sorts_by()
            field = next(item for item in sorts_by if item["value"] == order_by)['order_by']

            queryset = field.endswith('rating') and \
                        queryset.annotate(average_rating=Avg('product_ratings__rating')).order_by(field) or \
                        queryset.order_by(field)

        return queryset

    def get_sorts_by(self, queryset=None):
        my_list = [
            {
                'value': 'latest',
                'display': 'Latest',
                'order_by': '-added_date',
            },
            {
                'value': 'price_low',
                'display': 'Price: Low to High',
                'order_by': 'price',
            },
            {
                'value': 'price_high',
                'display': 'Price: High to Low',
                'order_by': '-price',
            },
            {
                'value': 'rating_low',
                'display': 'Rating: Low to High',
                'order_by': 'average_rating',
            },
            {
                'value': 'rating_high',
                'display': 'Rating: High to Low',
                'order_by': '-average_rating',
            },
        ]
        return my_list

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.model.objects.filter(user__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unseen_count'] = Notification.user_unseen_count(user=self.request.user)
        return context

class NotificationUpdateView(UpdateView):
    model = Notification
    fields = ['is_seen']
    http_method_names = ['post']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_seen = True
        self.object.save()
        return JsonResponse({'success': 'ok'})

    def form_invalid(self, form):
        return JsonResponse({'error': form.errors})
