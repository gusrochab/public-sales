from sorl.thumbnail import ImageField, get_thumbnail
from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ImmobileKind(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AutomobileModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AutomobileBrand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AutomobileKind(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


class Like_Immobile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    immobile = models.ForeignKey('Immobile', on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='Like', max_length=10)

    def __str__(self):
        return str(self.immobile)


class Immobile(models.Model):
    kind = models.ForeignKey(ImmobileKind, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        null=True, blank=True, max_digits=15, decimal_places=2)
    size = models.DecimalField(
        null=True, blank=True, max_digits=15, decimal_places=2)
    rooms = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    url_origin = models.URLField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    date_auction = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='immobile_pics')
    liked = models.ManyToManyField(
        User, default=None, blank=True, related_name='liked')

    def __str__(self):
        return self.name

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        x1 = y1 = 0
        x2 = img.width
        y2 = img.height
        if img.width > 300:
            x1 = img.width/2 - 150
            x2 = img.width/2 + 150
        if img.height > 180:
            y1 = img.height/2 - 90
            y2 = img.height/2 + 90
        img = img.crop((x1, y1, x2, y2))
        # output_size = (300, 180)
        # img.thumbnail(output_size)
        img.save(self.image.path)


class Automobile(models.Model):
    model = models.ForeignKey(AutomobileModel, on_delete=models.CASCADE)
    brand = models.ForeignKey(AutomobileBrand, on_delete=models.CASCADE)
    kind = models.ForeignKey(AutomobileKind, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    year = models.IntegerField()
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    url_origin = models.URLField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    date_auction = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(
        null=True, blank=True, max_digits=15, decimal_places=2)
    image = models.ImageField(null=True, blank=True,
                              upload_to='automobile_pics')
    liked = models.ManyToManyField(User, default=None, blank=True)

    def __str__(self):
        return self.name

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        x1 = y1 = 0
        x2 = img.width
        y2 = img.height
        if img.width > 300:
            x1 = img.width/2 - 150
            x2 = img.width/2 + 150
        if img.height > 180:
            y1 = img.height/2 - 90
            y2 = img.height/2 + 90
        img = img.crop((x1, y1, x2, y2))
        # output_size = (300, 180)
        # img.thumbnail(output_size)
        img.save(self.image.path)
