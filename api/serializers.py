from rest_framework import serializers
from .models import Category, Supplier, Product, Order, OrderDetail, Payment, Inventory, InventoryTransaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_info']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), source='supplier')
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'supplier', 'price', 'supplier_id', 'category_id']

class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderDetail.objects.create(order=order, **item_data)
        return order

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_date', 'amount', 'payment_method', 'status']

class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Inventory
        fields = ['product', 'stock_level']

class InventoryTransactionSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()

    class Meta:
        model = InventoryTransaction
        fields = ['inventory', 'quantity', 'transaction_type', 'transaction_date']
