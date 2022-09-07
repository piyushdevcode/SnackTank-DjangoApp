from django.apps import AppConfig


class HomepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homepage'

    # Monkey Patching
    def ready(self) -> None:
        from .models import User

        def get_cartitems_count(self):
            from .models import CartItems

            return CartItems.objects.filter(cart__is_paid=False, cart__user=self).count()
        
        User.add_to_class("get_cartitems_count",get_cartitems_count)
        
