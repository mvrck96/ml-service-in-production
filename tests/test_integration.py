class TestIntegration:
    def test_startup(self, mock_client):
        assert mock_client.get("/").status_code == 200
