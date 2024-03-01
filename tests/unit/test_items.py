"""Test for items.py."""
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "product, expected_status, expected_response",
    [
        (
            "milk",
            200,
            {
                "stock_level": {
                    "Sainsbury's Euston": "",
                    "Sainsbury's Holborn": "",
                    "Sainsbury's Soho": "",
                    "Sainsbury's Barbican": "",
                },
                "datetime": {
                    "Sainsbury's Euston": "",
                    "Sainsbury's Holborn": "",
                    "Sainsbury's Soho": "",
                    "Sainsbury's Barbican": "",
                },
            },
        ),  # successful API call
        (
            "cup",
            422,
            {
                "detail": [
                    {
                        "ctx": {"expected": "'milk', 'bread', 'fruit' or 'vegetables'"},
                        "input": "cup",
                        "loc": ["query", "product"],
                        "msg": "Input should be 'milk', 'bread', 'fruit' or 'vegetables'",
                        "type": "enum",
                    }
                ]
            },
        ),  # wrong API call
    ],
)
def test_get_stock_levels(
    product: str, expected_status: int, expected_response: dict
) -> None:
    """Unit test for get_stock_levels."""
    response = client.get("/stock-levels", params={"product": product})
    assert response.status_code == expected_status
    assert response.json() == expected_response


## TODO: Ideally we should patch _read_db function
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
#     assert response.json() == {"asdf":'asdf'}
