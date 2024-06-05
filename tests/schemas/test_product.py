import pytest
from pydantic import ValidationError

from store.schemas.product import ProductIn
from tests.schemas.factories import product_data


def test_schemas_return_success():
    # product = ProductIn(**data)
    product = ProductIn.model_validate(product_data())

    assert product.name == "Iphone 14 pro Max"


def test_schemas_return_raise():
    data = product_data()
    del data["status"]

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "Iphone 14 pro Max", "quantity": 10, "price": 8500},
        "url": "https://errors.pydantic.dev/2.7/v/missing",
    }
