from typing import List
from uuid import UUID

import pytest

from tests.schemas.factories import product_data
from fastapi import status


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    del content["created_at"]
    del content["updated_at"]
    del content["id"]
    esperado = {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": 8500,
        "status": True,
    }
    assert response.status_code == status.HTTP_201_CREATED
    assert content == esperado


async def test_controller_create_should_return_missing(client, products_url):
    data = product_data()
    del data["name"]
    response = await client.post(products_url, json=data)

    assert response.status_code == 422


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()
    del content["created_at"]
    del content["updated_at"]
    esperado = {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": 8500,
        "status": True,
    }

    assert response.status_code == status.HTTP_200_OK
    assert content == esperado


async def test_controller_get_should_return_not_found(client, products_url):
    id = UUID("fce6cc37-10b9-4a8e-a8b2-977df327001b")
    response = await client.get(f"{products_url}{id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Product not found with filter: {id}"}


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    data = {"price": 7500, "updated_at": "2024-06-05 12:08"}
    response = await client.patch(f"{products_url}{product_inserted.id}", json=data)

    content = response.json()
    del content["created_at"]
    # del content['updated_at']
    esperado = {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": 7500,
        "status": True,
        "updated_at": "2024-06-05T12:08:00",
    }

    assert response.status_code == status.HTTP_200_OK
    assert content == esperado


async def test_controller_patch_should_return_not_found(client, products_url):
    id = UUID("fce6cc37-10b9-4a8e-a8b2-977df327001b")
    data = {"price": 7500}
    response = await client.patch(f"{products_url}{id}", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Product not found with filter: {id}"}


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    id = UUID("fce6cc37-10b9-4a8e-a8b2-977df327001b")
    response = await client.delete(f"{products_url}{id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Product not found with filter: {id}"}
