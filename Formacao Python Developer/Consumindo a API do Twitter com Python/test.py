from src.services import _get_trends
from unittest import mock

def test_get_trends_success():
    # Arrange
    mock_api = mock.Mock()
    mock_api.trends_place.return_value = [
        {
            "trends": []
        }
    ]

    # Act
    trends = _get_trends(woe_id=1000, api=mock_api)

    # Assert
    assert trends == []