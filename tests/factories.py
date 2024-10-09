"""
Test Factory to make fake objects for testing
"""

import factory
from decimal import Decimal
from service.models import Products


class ProductsFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Products

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    description = factory.Faker("text")
    price = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)

    # Todo: Add your other attributes here...
