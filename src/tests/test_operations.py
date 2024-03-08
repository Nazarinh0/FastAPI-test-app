from httpx import AsyncClient


async def test_add_operation(async_client: AsyncClient):
    response = await async_client.post("/operations/", json={
        "quantity": "25.5",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": "2024-03-08T19:23:51.365",
        "type": "Выплата купонов",
    })
    print(response)
    assert response.status_code == 200


async def test_get_operation(async_client: AsyncClient, operation_fixture):
    operation_id = operation_fixture.get("id")  

    response = await async_client.get(f"/operations/{operation_id}") 

    assert response.status_code == 200, "Failed to fetch operation"


# async def test_get_operation(async_client: AsyncClient):
#     response = await async_client.get("/operations/", params={
#         "operation_id": "1",
#     })

#     assert response.status_code == 200
