from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DecimalField, PositiveIntegerField, Model, EmailField, ForeignKey, CASCADE, \
    BooleanField, TextChoices, PROTECT, TextField, ManyToManyField, SET_NULL
from django_resized import ResizedImageField

from apps.models.base import BaseModel
from apps.models.payments import PaymentHistory


class User(AbstractUser):
    phone = CharField(max_length=255, unique=True)
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='users',
                              default='media/product-default.jpg')
    address = CharField(max_length=555, blank=True, null=True)
    telegram_id = CharField(max_length=55, null=True, blank=True)
    bot_is_activate = BooleanField(default=False)
    balance = DecimalField(max_digits=30, decimal_places=2, default=0)  # main balance
    bonus = PositiveIntegerField(default=0)  # bonus balance
    deposit = DecimalField(max_digits=30, decimal_places=2, default=0)  # deposit balance
    coin = PositiveIntegerField(default=0)
    region = ForeignKey('apps.Region', SET_NULL, null=True, blank=True)
    district = ForeignKey('apps.District', SET_NULL, null=True, blank=True)
    favourite = ManyToManyField('apps.Product', 'favourites')

    @property
    def payout(self):
        amounts = self.paymenthistory_set.filter(
            status=PaymentHistory.StatusChoices.ACCEPTED
        ).values_list('amount', flat=True)
        return sum(amounts)

    @property
    def image_url(self):
        try:
            url = self.image.image.url
        except (ValueError, AttributeError):
            url = 'https://via.placeholder.com/100x100'
        return url

    @property
    def favorites(self):
        # if self.favorite_set.exists():
        return self.favorite_set.all()
        # return False

    @property
    def favorites_id(self):
        if self.favorite_set.exists():
            return self.favorite_set.values_list('product_id', flat=True)
        return False


class Contact(Model):
    phone = CharField(max_length=255)
    email = EmailField(max_length=255)
    telegram = CharField(max_length=255)

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'


class Favorite(Model):
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)


class Ticket(BaseModel):
    class SenderTextChoice(TextChoices):
        CUSTOMER = 'customer', 'xaridor'
        COURIER = 'courier', 'kuryer'
        ADMIN = 'admin', 'admin'
        SALESMAN = 'salesman', 'sotuvchi'
        OTHER = 'other', 'boshqa'

    class PurposeTextChoice(TextChoices):
        ISSUE = 'issue', 'muammo'
        SUGGESTION = 'suggestion', 'taklif'

    author = ForeignKey(User, PROTECT)
    sender = CharField(max_length=55, choices=SenderTextChoice.choices)
    sender_name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    ticket_purpose = CharField(max_length=55, choices=PurposeTextChoice.choices)
    message = TextField()
