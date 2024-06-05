from typing import List
from uuid import UUID

import pytest

from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase
from store.core.exceptions import NotFoundException


async def test_usecases_create_shoud_return_success(product_in):
    result = await product_usecase.create(body=product_in)
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"


async def test_usecases_get_shoud_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"


async def test_usecases_get_shoud_return_not_found():
    with pytest.raises(NotFoundException) as err:
        product_id = UUID("fce6cc37-10b9-4a8e-a8b2-977df327001b")
        await product_usecase.get(id=product_id)

    assert (
        err.value.message
        == "Product not found with filter: fce6cc37-10b9-4a8e-a8b2-977df327001b"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_shoud_return_success():
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) > 1


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_shoud_return_sucess_filtered():
    query = {"price": {"$gt": 5000, "$lt": 8000}}
    result = await product_usecase.filter(query)

    assert isinstance(result, List)
    assert len(result) == 2


async def test_usecases_update_shoud_return_success(product_up, product_inserted):
    product_up.price = 7500
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


async def test_usecases_delete_shoud_return_success(product_up, product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


async def test_usecases_delete_shoud_return_not_found():
    with pytest.raises(NotFoundException) as err:
        product_id = UUID("fce6cc37-10b9-4a8e-a8b2-977df327001b")
        await product_usecase.delete(id=product_id)

    assert (
        err.value.message
        == "Product not found with filter: fce6cc37-10b9-4a8e-a8b2-977df327001b"
    )
