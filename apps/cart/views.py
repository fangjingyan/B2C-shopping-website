from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
# Create your views here.


# add goods to the cart
# 1. ajax post
# 2. pass parameters: goods id(sku.id) and amount(count)
# /cart/add
class CartAddView(View):

    def post(self, request):
        # receive data
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': 'user not login'})

        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # verity data
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': 'incomplete data'})

        try:
            count = int(count)

        except Exception as e:

            return JsonResponse({'res': 2, 'errmsg': 'goods amount wrong'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)

        except GoodsSKU.DoesNotExist:

            return JsonResponse({'res': 3, 'errmsg': 'goods not exist'})

        # handle: add to cart
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        # if sku_id not in hash, hget return None
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            count += int(cart_count)

        # check stock
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': 'out of stock'})
        conn.hset(cart_key, sku_id, count)

        total_count = conn.hlen(cart_key)

        return JsonResponse({'res': 5, 'total_count': total_count, 'message': 'add successfully'})


# /cart/
class CartInfoView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        # from redis get cart info
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        cart_dict = conn.hgetall(cart_key)

        skus = []
        total_count = 0
        total_price = 0
        for sku_id, count in cart_dict.items():
            sku = GoodsSKU.objects.get(id=sku_id)
            sub_price = sku.price * int(count)
            sku.sub_price = sub_price
            sku.count = int(count)
            skus.append(sku)
            total_price += sub_price
            total_count += int(count)

        context = {'total_price': total_price,
                   'total_count': total_count,
                   'skus': skus}

        return render(request, 'cart.html', context)


# use ajax post
# /cart/update
class CartUpdateView(View):

    def post(self, request):

        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': 'user not login'})

        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'errmsg': 'incomplete data'})

        try:
            count = int(count)

        except Exception as e:

            return JsonResponse({'res': 2, 'errmsg': 'goods amount wrong'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)

        except GoodsSKU.DoesNotExist:

            return JsonResponse({'res': 3, 'errmsg': 'goods not exist'})

        conn = get_redis_connection('default')

        cart_key = 'cart_%d'%user.id

        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': 'out of stock'})

        conn.hset(cart_key, sku_id, count)

        vals = conn.hvals(cart_key)
        total_count = 0
        for val in vals:
            total_count += int(val)

        return JsonResponse({'res': 5, 'total_count': total_count, 'message': 'update successfully'})


# use ajax post
# /cart/delete
class CartDeleteView(View):
    def post(self, request):

        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': 'user not login'})

        sku_id = request.POST.get('sku_id')

        if not sku_id:
            return JsonResponse({'res': 1, 'errmsg': 'invalid data'})

        try:
            sku = GoodsSKU.objects.get(id=sku_id)

        except GoodsSKU.DoesNotExist:

            return JsonResponse({'res': 2, 'errmsg': 'goods not exist'})

        conn = get_redis_connection('default')

        cart_key = 'cart_%d'%user.id

        conn.hdel(cart_key, sku_id)

        vals = conn.hvals(cart_key)
        total_count = 0
        for val in vals:
            total_count += int(val)

        return JsonResponse({'res': 3, 'total_count': total_count, 'message': 'delete successfully'})
