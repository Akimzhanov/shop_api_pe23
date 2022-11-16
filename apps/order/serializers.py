from rest_framework import serializers
from .models import Order, OrderItems



class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['product', 'quantity']


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'address', 'total_sum', 'items']

    # self.products.quantity

    def create(self, validated_data):
        items = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user  # для того чтобы узнать от кого запрос
        order = super().create(validated_data)
        total_sum = 0
        orders_items = []
        for item in items:
            orders_items.append(OrderItems(
                order = order,
                product = item['product'],
                quantity = item['quantity']
            ))
            total_sum += item['product'].price * item['quantity']
        
        OrderItems.objects.bulk_create(orders_items)      #bulk_create() принимает список объектов
        order.total_sum = total_sum
        order.save()
        return order  #super().create(validated_data)   =  Order.objects.create(**validated_data)





