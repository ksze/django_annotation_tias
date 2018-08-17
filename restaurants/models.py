from django.db import models


# Create your models here.
class Restaurant(models.Model):
    name = models.TextField(unique=True)


class Cuisine(models.Model):
    """ Cuisine; like Szechuan, French, Italian, etc. """
    name = models.TextField(unique=True)


class Chef(models.Model):
    """ Each restaurant can have multiple chefs, but each chef of the given
        restaurant must specialize in one distinct cuisine.

        E.g. You could have these restaurants and chefs:
        - Barbie's Steakhouse
            - Paul, French cuisine
            - Giorgio, Italian cuisine
        - The Jade Garden
            - Ping, Szechuan cuisine
            - George, French cuisine
    """
    name = models.TextField()
    restaurant = models.ForeignKey(Restaurant, related_name='chefs', on_delete=models.PROTECT)
    cuisine = models.ForeignKey(Cuisine, related_name='chefs', on_delete=models.PROTECT)

    class Meta:
        unique_together = (('restaurant', 'cuisine'),)


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='tables', on_delete=models.PROTECT)
    number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('restaurant', 'number'),)
