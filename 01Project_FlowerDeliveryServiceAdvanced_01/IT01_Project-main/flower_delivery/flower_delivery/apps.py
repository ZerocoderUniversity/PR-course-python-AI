from django.apps import AppConfig

class FlowerDeliveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flower_delivery'

    def ready(self):
        pass
