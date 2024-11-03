from api.models import Payment


class PaymentService:
    """
    Service to handle payment processing.
    """

    def process_payment(self, order, payment_data):
        # Simulate payment processing
        payment_method = payment_data['method']
        amount = payment_data['amount']

        if payment_method not in ['credit_card', 'paypal']:
            raise ValueError("Invalid payment method")

        # Assume payment goes through successfully for now
        Payment.objects.create(order=order, method=payment_method, amount=amount)
        return True
