from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from goods.models import GoodsSKU
from user.models import Address
from order.models import OrderInfo, OrderGoods
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from django.http import JsonResponse
from datetime import datetime
from django.db import transaction
# Create your views here.


# /order/place
class OrderPlaceView(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user

        # get paras
        sku_ids = request.POST.getlist('sku_ids')

        # verify paras
        if not sku_ids:

            return redirect(reverse('cart:show'))

        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        skus = []
        total_count = 0
        total_price = 0
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)
            count = conn.hget(cart_key, sku_id)
            subprice = sku.price * int(count)
            sku.count = int(count)
            sku.subprice = subprice
            skus.append(sku)
            total_count += int(count)
            total_price += subprice

        transit_price = 10

        total_pay = total_price + transit_price

        addrs = Address.objects.filter(user=user)

        sku_ids = ','.join(sku_ids)
        context = {'skus': skus,
                   'sku_ids': sku_ids,
                   'total_count': total_count,
                   'total_price': total_price,
                   'transit_price': transit_price,
                   'total_pay': total_pay,
                   'addrs': addrs
                   }

        return render(request, 'place_order.html', context)


# user ajax post
# /order/commit
# pessimistic lock
'''
class OrderCommitView(View):
    # all mysql queries in a transaction
    @transaction.atomic
    def post(self, request):
        user = request.user

        if not user.is_authenticated:

            return JsonResponse({'res': 0, 'errmsg': 'user not login'})

        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')

        if not all([addr_id, pay_method, sku_ids]):

            return JsonResponse({'res': 1, 'errmsg': 'incomplete data'})

        if pay_method not in OrderInfo.PAY_METHODS.keys():

            return JsonResponse({'res': 2, 'errmsg': 'invalid pay menthod'})

        try:
            addr = Address.objects.get(id=addr_id)

        except Address.DoesNotExist:

            return JsonResponse({'res': 3, 'errmsg': 'invalid address'})


        # handle: create order

        # order id: 20191229140201 + user id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)

        # transit_price
        transit_price = 10

        # total price and total count
        total_count = 0
        total_price = 0

        # set savepoint
        save_id = transaction.savepoint()
        try:
            # add record in df_order_info
            order = OrderInfo.objects.create(order_id=order_id, user=user, addr=addr, pay_method=pay_method,
                                             total_count=total_count, total_price=total_price, transit_price=transit_price)

            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id

            sku_ids = sku_ids.split(',')

            for sku_id in sku_ids:

                try:
                    # Pessimistic Lock, lock when querying
                    sku = GoodsSKU.objects.select_for_update().get(id=sku_id)

                except:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 4, 'errmsg': 'goods not exist'})

                count = conn.hget(cart_key, sku_id)

                if int(count) > sku.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 6, 'errmsg': 'out of stock'})

                # add records in df_order_goods same records number as goods in the order
                OrderGoods.objects.create(order=order, sku=sku, count=count, price=sku.price)

                # update stock and sales
                sku.stock -= int(count)
                sku.sales += int(count)
                sku.save()

                # total_price and total_count
                subprice = sku.price * int(count)
                total_count += int(count)
                total_price += subprice

            # update order
            order.total_count = total_count
            order.total_price = total_price
            order.save()

        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 7, 'errmsg': 'place order fail'})

        # commit transaction
        transaction.savepoint_commit(save_id)

        # clear cart info
        conn.hdel(cart_key, *sku_ids)

        return JsonResponse({'res': 5, 'message': 'create order successfully'})
'''

# optimistic lock
class OrderCommitView(View):
    # all mysql queries in a transaction
    @transaction.atomic
    def post(self, request):
        user = request.user

        if not user.is_authenticated:

            return JsonResponse({'res': 0, 'errmsg': 'user not login'})

        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        sku_ids = request.POST.get('sku_ids')

        if not all([addr_id, pay_method, sku_ids]):

            return JsonResponse({'res': 1, 'errmsg': 'incomplete data'})

        if pay_method not in OrderInfo.PAY_METHODS.keys():

            return JsonResponse({'res': 2, 'errmsg': 'invalid pay menthod'})

        try:
            addr = Address.objects.get(id=addr_id)

        except Address.DoesNotExist:

            return JsonResponse({'res': 3, 'errmsg': 'invalid address'})

        # handle: create order

        # order id: 20191229140201 + user id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)

        # transit_price
        transit_price = 10

        # total price and total count
        total_count = 0
        total_price = 0

        # set savepoint
        save_id = transaction.savepoint()
        try:
            # add record in df_order_info
            order = OrderInfo.objects.create(order_id=order_id, user=user, addr=addr, pay_method=pay_method,
                                             total_count=total_count, total_price=total_price, transit_price=transit_price)

            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id

            sku_ids = sku_ids.split(',')

            for sku_id in sku_ids:
                for i in range(3):
                    try:
                        # Pessimistic Lock, lock when querying
                        sku = GoodsSKU.objects.get(id=sku_id)

                    except:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 4, 'errmsg': 'goods not exist'})

                    count = conn.hget(cart_key, sku_id)

                    if int(count) > sku.stock:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 6, 'errmsg': 'out of stock'})

                    # update stock and sales
                    orgin_stock = sku.stock
                    new_stock = orgin_stock - int(count)
                    new_sales = sku.sales + int(count)

                    # update df_goods_sku set stock=new_stock, sales=new_sales
                    # where id=sku_id and stock = orgin_stock
                    res = GoodsSKU.objects.filter(id=sku_id, stock=orgin_stock).update(stock=new_stock, sales=new_sales)
                    if res == 0:
                        if i == 2:
                            transaction.savepoint_rollback(save_id)
                            return JsonResponse({'res': 7, 'errmsg': 'place order fail'})
                        continue

                    # add records in df_order_goods same records number as goods in the order
                    OrderGoods.objects.create(order=order, sku=sku, count=count, price=sku.price)

                    # total_price and total_count
                    subprice = sku.price * int(count)
                    total_count += int(count)
                    total_price += subprice

                    break

            # update order
            order.total_count = total_count
            order.total_price = total_price
            order.save()

        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 7, 'errmsg': 'place order fail'})

        # commit transaction
        transaction.savepoint_commit(save_id)

        # clear cart info
        conn.hdel(cart_key, *sku_ids)

        return JsonResponse({'res': 5, 'message': 'create order successfully'})
