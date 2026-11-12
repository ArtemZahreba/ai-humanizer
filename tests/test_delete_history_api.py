from unittest.mock import patch

from app import app


def test_delete_history_api():
    with app.test_client() as client:

        # 1. Successful deletion
        with patch(
            "routes.history.HistoryService.delete_history",
            return_value=True
        ) as mock_delete:

            response = client.delete(
                "/api/history/1?client_id=test_client"
            )

            assert response.status_code == 200
            assert response.json["status"] == "success"

            mock_delete.assert_called_once_with(
                history_id=1,
                client_id="test_client"
            )

            print("SUCCESS: Delete history API test passed!")

        # 2. Record not found
        with patch(
            "routes.history.HistoryService.delete_history",
            return_value=False
        ):
            response = client.delete(
                "/api/history/999?client_id=test_client"
            )

            assert response.status_code == 404

            print("SUCCESS: Missing history API test passed!")

        # 3. Missing client_id
        with patch(
            "routes.history.HistoryService.delete_history"
        ) as mock_delete:

            response = client.delete("/api/history/1")

            assert response.status_code == 400
            mock_delete.assert_not_called()

            print("SUCCESS: Missing client ID API test passed!")

        # 4. Invalid client_id
        with patch(
            "routes.history.HistoryService.delete_history",
            side_effect=ValueError("Client ID is required")
        ):
            response = client.delete(
                "/api/history/1?client_id=%20"
            )

            assert response.status_code == 400

            print("SUCCESS: Invalid client ID API test passed!")

        # 5. Unexpected error
        with patch(
            "routes.history.HistoryService.delete_history",
            side_effect=Exception("Database error")
        ):
            response = client.delete(
                "/api/history/1?client_id=test_client"
            )

            assert response.status_code == 500

            print("SUCCESS: Server error API test passed!")


if __name__ == "__main__":
    test_delete_history_api()
    print("\nAll Delete History API tests passed!")