from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Menu(models.Model):
    menu = models.CharField('Menu', max_length=20)
    price = models.PositiveIntegerField('Price')

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menus'

    def __str__(self):
        return self.menu

class Order(models.Model):
    order_number = models.AutoField('Order Number', primary_key=True)
    order_date = models.DateTimeField('Order Date', auto_now_add=True)
    total_price = models.PositiveIntegerField('Total Price', default=0)  # 주문의 총 가격
    total_items = models.PositiveIntegerField('Total Items', default=0)  # 주문의 총 항목 수

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantity')

    class Meta:
        verbose_name = 'order_item'
        verbose_name_plural = 'order_items'

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total_items(sender, instance, **kwargs):
    # 주문의 총 항목 수 계산
    order = instance.order
    total_items = order.orderitem_set.count()
    order.total_items = total_items
    order.save()

    # 주문의 총 가격 업데이트
    total_price = sum(item.menu.price * item.quantity for item in order.orderitem_set.all())
    order.total_price = total_price
    order.save()
