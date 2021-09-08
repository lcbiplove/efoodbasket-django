from users.models import Trader
from django.core.checks import messages
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from .models import Product, ProductCategory, Query, Rating, Review, Shop, ProductImage, WishList
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .permissions import ShopOwnerRequired, ProductOwnerRequired, QuestionOwnerRequired, \
                            AnswerOwnerRequired, ReviewOwnerRequired, WishListOwnerRequired
from users.permissions import TraderRequired, CustomerRequired
from django.contrib import messages
from .forms import CreateProductForm
from django.utils import timezone
from django.db.models import Avg

class ShopCreateView(TraderRequired, SuccessMessageMixin, CreateView):
    model = Shop
    template_name = 'add-shop.html'
    fields = ['name', 'address', 'contact']
    success_message = 'Shop Added successfully!'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_trader:
            shop_count = Shop.objects.filter(trader__id=request.user.trader.id).count()
            if shop_count >= 2:
                messages.add_message(request, messages.INFO, 'You can only add upto 2 shops.', 'info')
                return redirect('shop_list')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.trader = self.request.user.trader
        return form

    def get_success_url(self):
        success_url = super().get_success_url()
        next_page = self.request.GET.get('next')
        if next_page:
            success_url = next_page
        return success_url

class ShopUpdateView(SuccessMessageMixin, ShopOwnerRequired, UpdateView):
    model = Shop
    template_name = 'edit-shop.html'
    context_object_name = 'shop'
    fields = ['name', 'address', 'contact']
    success_message = 'Shop updated successfully!'

class ShopListView(TraderRequired, ListView):
    model = Shop
    template_name = 'shops.html'
    context_object_name = 'shops'

    def get_queryset(self):
        return Shop.objects.filter(trader__user__id=self.request.user.id).select_related('trader', 'trader__user')

class ShopDeleteView(ShopOwnerRequired, DeleteView):
    model = Shop
    success_url = reverse_lazy('shop_list')
    http_method_names = ['post']

    def http_method_not_allowed(self, request, *args, **kwargs):
        return redirect(self.success_url)

class ProductCreateView(SuccessMessageMixin, TraderRequired, CreateView):
    form_class = CreateProductForm
    template_name = 'add-product.html'
    success_message = 'Product Added successfully!'

    def dispatch(self, request, *args, **kwargs):
        if not Shop.objects.filter(trader__user__id=self.request.user.id).exists() and request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'You need to have at least a shop to add product.', 'info')
            return redirect(reverse_lazy('shop_create') + '?next=' + reverse_lazy('product_create'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.filter(trader__user__id=self.request.user.id)
        context['categories'] = ProductCategory.objects.all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.trader = self.request.user.trader
        self.object.save()
        img_files = form.files.getlist('image')
        for file in img_files:
            ProductImage.objects.create(image=file, product=self.object)
        return super().form_valid(form)

class ProductSearchFilter(ListView):
    context_object_name = 'products'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_rating'] = self.request.GET.get('rating', '')
        context['selected_min_price'] = self.request.GET.get('minPrice', '')
        context['selected_max_price'] = self.request.GET.get('maxPrice', '')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        rating = self.request.GET.get('rating', '')
        min_price = self.request.GET.get('minPrice', '')
        max_price = self.request.GET.get('maxPrice', '')

        if rating:
            queryset = queryset.annotate(average_rating=Avg('product_ratings__rating')).filter(average_rating__gte=rating)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

class VisitTraderView(ProductSearchFilter):
    model = Product
    template_name = 'manage-products.html'
    queryset = Product.objects.filter().select_related('shop')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'trader'):
            context['is_visitor_owner'] = str(self.request.user.trader.id) == self.kwargs.get('pk', '')
        else:
            context['is_visitor_owner'] = False

        if self.kwargs.get('pk', ''):
            context['trader'] = Trader.objects.get(pk=self.kwargs.get('pk', ''))
        return context

class ManageProductView(TraderRequired, VisitTraderView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_visitor_owner'] = True
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    queryset = Product.objects.filter().select_related('shop__trader', 'shop__trader__user')

class ProductUpdateView(SuccessMessageMixin, ProductOwnerRequired, UpdateView):
    model = Product
    template_name = 'edit-product.html'
    success_message = 'Product Updated successfully!'
    context_object_name = 'product'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.filter(trader__user__id=self.request.user.id)
        context['categories'] = ProductCategory.objects.all()
        return context

class ProductDeleteView(SuccessMessageMixin, ProductOwnerRequired, DeleteView):
    model = Product
    success_url = reverse_lazy('product_manage')
    http_method_names = ['post']
    success_message = 'Product deleted successfully!'

    def http_method_not_allowed(self, request, *args, **kwargs):
        return redirect(self.success_url)

class QueryCreateView(CustomerRequired, CreateView):
    model = Query
    fields = ['question']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.product = Product.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        payload = self.get_response_data()
        return JsonResponse(payload)

    def form_invalid(self, form):
        return JsonResponse({
            'error': form['question'].errors[0]
        })

    def get_response_data(self) -> dict:
        data = {}
        data['query_id'] = self.object.id
        data['question'] = self.object.question
        data['question_by'] = self.object.user.fullname
        data['time_since'] = 'just now'
        data['product_id'] = self.object.product.id
        return data


class QueryDeleteView(QuestionOwnerRequired, DeleteView):
    model = Query
    success_url = reverse_lazy('product_manage')
    http_method_names = ['post']

    def http_method_not_allowed(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class AnswerUpdateView(AnswerOwnerRequired, UpdateView):
    model = Query
    fields = ['answer']
    http_method_names = ['post']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.answer_date = timezone.now()
        self.object.save()
        payload = self.get_response_data()
        return JsonResponse(payload)

    def form_invalid(self, form):
        return JsonResponse({
            'error': form['answer'].errors[0]
        })

    def get_response_data(self) -> dict:
        data = {}
        data['query_id'] = self.object.id
        data['answer'] = self.object.answer
        data['time_since'] = 'just now'
        data['product_id'] = self.object.product.id
        return data

class AnswerDeleteView(AnswerOwnerRequired, UpdateView):
    model = Query
    fields = ['answer']
    http_method_names = ['post']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.answer = None
        self.object.answer_date = None
        self.object.save()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class RatingCreateUpdateView(CustomerRequired, CreateView):
    model = Rating
    fields = ['rating',]

    def form_valid(self, form):
        rating = form.cleaned_data.get("rating")
        self.object, _ = Rating.objects.update_or_create(
            user=self.request.user, 
            product=Product.objects.get(pk=self.kwargs['pk']), 
            defaults={
                'rating': rating
            }
        )
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({
            'error': form['rating'].errors[0]
        })

class ReviewCreateUpdateView(CustomerRequired, CreateView):
    model = Review
    fields = ['review',]

    def form_valid(self, form):
        review = form.cleaned_data.get("review")
        try:
            rating = Rating.objects.get(user__id=self.request.user.id, product__id=self.kwargs['pk'])
            self.object, _ = Review.objects.update_or_create(
                rating=rating, 
                defaults={
                    'review': review
                }
            )
            return JsonResponse({'success': True})
        except:
            return JsonResponse({
                'error': 'Please give rating before adding your review.'
            })

    def form_invalid(self, form):
        return JsonResponse({
            'error': form['review'].errors[0]
        })

class ReviewDeleteView(ReviewOwnerRequired, DeleteView):
    model = Review
    success_url = reverse_lazy('product_manage')
    http_method_names = ['post']

    def http_method_not_allowed(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)

class WishListView(CustomerRequired, ProductSearchFilter):
    template_name = 'wishlists.html'
    
    def get_queryset(self):
        user_id = self.request.user.id
        return Product.objects.filter(product_wishlists__user__id=user_id)

class WishCreateView(CustomerRequired, CreateView):
    model = WishList
    fields = []
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.product = Product.objects.get(pk=self.kwargs['id'])
        self.object.save()
        return JsonResponse({'success': 'ok'})

    def form_invalid(self, form):
        return JsonResponse({'error': form.errors})
    
class WishDeleteView(WishListOwnerRequired, DeleteView):
    model = WishList
    success_url = reverse_lazy('home')
    http_method_names = ['post']

    def http_method_not_allowed(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def get_object(self):
        object = self.model.objects.get(product__id=self.kwargs['id'], user__id=self.request.user.id)
        return object

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)