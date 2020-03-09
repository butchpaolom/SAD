from django.db.models.signals import post_save
from paypal.standard.ipn.models import *
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=CustomerInfo)
def create_transaction(sender, instance, created, **kwargs):
    if created:
        print('From signals: ' + str(instance.final_order.trans_id))
        final_order = FinalOrder.objects.get(trans_id=str(instance.final_order.trans_id))
        Transaction.objects.create(final_order=final_order)

@receiver(post_save, sender=PayPalIPN)
def update_transaction(sender, instance, created, **kwargs):
    if created:
        #look for transaction
        transaction = Transaction.objects.get(final_order__trans_id=instance.invoice)
        if instance.payment_status == 'Completed':
            transaction.paid = True
            transaction.save()
            orders = transaction.final_order.orders.all()
            for order in orders:
                quantity = order.quantity
                order.product.stock = order.product.stock - quantity
                for each in Product.objects.all():
                    if order.product.product_name == each.product_name:
                        each.stock = order.product.stock
                        each.save()
                order.product.save()


                