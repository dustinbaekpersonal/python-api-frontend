"""Test for items.py."""
import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "store_id, expected_status, expected_response",
    [
        (
            "1",
            200,
            [
                {
                    "created_date": "2024-03-03T19:39:00.933000",
                    "id": 1,
                    "product_name": "milk",
                    "stock_level": 10,
                    "store_id": 1,
                },
            ],
        ),  # successful API call
        (
            "3",
            404,
            {"detail": "Store is not found."},
        ),  # wrong API call
    ],
)
def test_get_stock_levels_by_store_id(store_id, expected_status, expected_response) -> None:
    """Unit test for get_stock_levels."""
    response = client.get(f"/inventory/{store_id}/")
    assert response.status_code == expected_status
    assert response.json() == expected_response


# # TODO: Ideally we should patch _read_db function
# def test_get_stock_levels_db(monkeypatch: pytest.MonkeyPatch) -> None:
#     """Unit test for get_stock_levels to read from database."""
#     def replace_read_db() -> pd.DataFrame:
#         """Function to replace """
#         return pd.DataFrame(
#             {
#                 "stock_level": ["10"],
#                 "datetime": ["20"],
#             },
#             index = ['milk']
#         )
#     # Use monkeypatch to replace the original function with the mock
#     monkeypatch.setattr("api.items._read_db", replace_read_db)
#     response = client.get("/stock-levels", params={"product":"milk"})
#     assert response.status_code == 200
#     assert response.json() == {
#         "stock_level":'10',
#         "datetime": '20',
#         }
