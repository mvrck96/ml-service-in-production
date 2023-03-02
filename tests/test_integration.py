import pytest

from conftest import probe_names


class TestIntegration:
    def test_startup(self, mock_client):
        assert mock_client.get("/").status_code == 200
        assert mock_client.get("/metrics").status_code == 200
        assert mock_client.get("/docs").status_code == 200
        assert mock_client.get("/health/liveness").status_code == 200
        assert mock_client.get("/health/readiness").status_code == 200

    @pytest.mark.parametrize("req", probe_names)
    def test_probes(self, mock_client, req):
        probe = mock_client.get(f"/health/{req}")
        assert probe.json() == {req: True}
