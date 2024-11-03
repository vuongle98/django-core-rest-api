from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from api.models import Product, Order, Inventory, Payment
from api.serializers import OrderSerializer, PaymentSerializer
from api.services.inventory_service import InventoryService
from api.services.notification_service import NotificationService
from api.services.payment_service import PaymentService


class ProcessOrderView(APIView):
    """
    View to handle user order processing, including order creation, payment, and inventory adjustment.
    """

    def post(self, request):
        try:
            # Step 1: Validate and Create the Order
            order_serializer = OrderSerializer(data=request.data)
            order_serializer.is_valid(raise_exception=True)
            order = order_serializer.save(user=request.user)  # User who placed the order

            # Step 2: Check Product Availability
            self.check_inventory(order)

            # Step 3: Process Payment
            payment_data = request.data.get('payment')
            payment_serializer = PaymentSerializer(data=payment_data)
            payment_serializer.is_valid(raise_exception=True)
            payment_service = PaymentService()
            if not payment_service.process_payment(order, payment_serializer.validated_data):
                raise ValueError("Payment failed")

            # Step 4: Adjust Inventory
            self.adjust_inventory(order)

            # Step 5: Update Order Status and Notify User
            order.status = 'CONFIRMED'
            order.save()

            notification_service = NotificationService()
            notification_service.send_order_confirmation(order)

            return Response({'message': 'Order processed successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def check_inventory(self, order):
        """
        Checks whether the ordered products have enough stock available.
        """
        inventory_service = InventoryService()
        for item in order.items.all():
            if not inventory_service.is_product_available(item.product, item.quantity):
                raise ValueError(f"Product {item.product.name} is out of stock or insufficient quantity")

    def adjust_inventory(self, order):
        """
        Adjusts the inventory by reducing the stock levels for the ordered products.
        """
        inventory_service = InventoryService()
        for item in order.items.all():
            inventory_service.reduce_stock(item.product, item.quantity)
