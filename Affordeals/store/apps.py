from django.apps import AppConfig


class StoreConfig(AppConfig):
    """
    Configuration for the Store application.

    Attributes:
    - default_auto_field (str): Specifies the type of auto-generated field to
      use for primary keys.
    - name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
