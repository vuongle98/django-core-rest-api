class NotificationService:
    """
    Service to handle user notifications like order confirmation.
    """
    def send_order_confirmation(self, order):
        # Send email or notification to the user
        user = order.user
        message = f"Dear {user.username}, your order {order.id} has been confirmed."
        print(message)  # Placeholder for actual notification (e.g., email, SMS)
