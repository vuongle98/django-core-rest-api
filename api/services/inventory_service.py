from api.models import Inventory


class InventoryService:
    """
    Service to handle inventory-related logic such as checking stock and adjusting it.
    """
    def is_product_available(self, product, quantity):
        inventory = Inventory.objects.get(product=product)
        return inventory.stock >= quantity

    def reduce_stock(self, product, quantity):
        inventory = Inventory.objects.get(product=product)
        if inventory.stock >= quantity:
            inventory.stock -= quantity
            inventory.save()
        else:
            raise ValueError(f"Not enough stock for product {product.name}")