from django.shortcuts import render, redirect
from .models import Menu, Order, OrderItem
from .forms import OrderForm
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.views import View


class MenuLV(ListView):
    model = Menu
    template_name = "kiosk/menu_all.html" # 디폴트 html
    context_object_name = 'menus' # menu_list가 디폴트


class AddToCartView(View):
    def post(self, request):
        menu_id = request.POST.get('menu_id')
        quantity = request.POST.get('quantity')

        print("Received menu_id:", menu_id)
        print("Received quantity:", quantity)
 
        # 기존 카트 데이터 가져오기
        cart = request.session.get('cart', {})

        if menu_id and quantity:
            try:
                menu = Menu.objects.get(pk=menu_id)
                # if 'cart' not in request.session:
                #     request.session['cart'] = {}
                
                if menu_id in cart:
                    cart[menu_id]['quantity'] += int(quantity)
                else:
                    cart[menu_id] = {'quantity': int(quantity), 'menu': menu.menu, 'price': menu.price}

                # 세션에 업데이트된 카트 데이터 저장
                request.session['cart'] = cart

                print("After adding to cart, session:", request.session.get('cart'))
                
                return HttpResponse(status=200, content=f"Success: 주문 정보가 장바구니에 추가되었습니다.")
            except Menu.DoesNotExist:
                return HttpResponse(status=400, content="Error: 잘못된 메뉴입니다.")
        else:
            return HttpResponse(status=400, content="Error: 메뉴와 수량을 모두 선택해주세요.")

class GetOrderInfo(View):
    def get(self, request):
        # 세션에서 현재 사용자의 주문 항목들을 가져오기
        cart = request.session.get('cart', {})
        
        # 주문 항목 리스트 초기화
        order_items = []
        total_price = 0
        
        # 카트에서 각 주문 항목의 정보 가져오기
        for menu_id, item_data in cart.items():
            menu = Menu.objects.get(pk=menu_id)
            quantity = item_data['quantity']
            order_items.append({'menu': menu.menu, 'quantity': quantity})
            total_price += menu.price * quantity
        
        # 주문 정보를 JSON 형태로 반환
        data = {
            'order_items': order_items,
            'total_price': total_price,
        }
        return JsonResponse(data)


class ProcessOrderView(View):
    def post(self, request):
        if 'cart' in request.session:
            cart = request.session['cart']
            total_price = sum(item['quantity'] * item['price'] for item in cart.values())
            
            # 주문 테이블 생성 및 저장
            order = Order.objects.create(total_price=total_price, total_items=len(cart))
            
            # 주문 항목 테이블 생성 및 저장
            for item_id, item_data in cart.items():
                menu_id = item_id
                quantity = item_data['quantity']
                menu = Menu.objects.get(pk=menu_id)
                OrderItem.objects.create(order=order, menu=menu, quantity=quantity)
            
            # 카트 비우기
            request.session.pop('cart')
            return HttpResponse(status=200, content="Success: 주문이 처리되었습니다.")
        else:
            return HttpResponse(status=400, content="Error: 장바구니에 주문 정보가 없습니다.")