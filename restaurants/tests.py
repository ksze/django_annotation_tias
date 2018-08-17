from django.db.models import When, Case, BooleanField
from django.test import TestCase


from restaurants.models import Restaurant, Cuisine, Chef, Table


# Create your tests here.
class AnnotationTests(TestCase):
    def test_annotation(self):
        r1 = Restaurant.objects.create(name='r1')
        r2 = Restaurant.objects.create(name='r2')
        r3 = Restaurant.objects.create(name='r3')
        r4 = Restaurant.objects.create(name='r4')

        french = Cuisine.objects.create(name='French')
        italian = Cuisine.objects.create(name='Italian')

        # r1 has both a French chef and an Italian chef.
        Chef.objects.create(name='french chef', cuisine=french, restaurant=r1)
        Chef.objects.create(name='italian chef', cuisine=italian, restaurant=r1)

        # r2 only has a French chef.
        Chef.objects.create(name='french chef', cuisine=french, restaurant=r2)

        # r3 only has an Italian chef.
        Chef.objects.create(name='italian chef', cuisine=italian, restaurant=r3)

        # r4 has no chef at all.

        for restaurant in (r1, r2, r3, r4):
            Table.objects.create(restaurant=restaurant, number=1)

        tables = Table.objects.annotate(
            restaurant_has_french_chef=Case(
                When(restaurant__chefs__cuisine=french, then=True),
                default=False,
                output_field=BooleanField(),
            ),
            restaurant_has_italian_chef=Case(
                When(restaurant__chefs__cuisine=italian, then=True),
                default=False,
                output_field=BooleanField(),
            ),
        )

        for table in tables:
            self.assertEqual(table.restaurant_has_french_chef, table.restaurant.chefs.filter(cuisine=french).exists())
            self.assertEqual(table.restaurant_has_italian_chef, table.restaurant.chefs.filter(cuisine=italian).exists())
