import pytest

from src.forecast import predict


paramed_data = [
    ([1, 1, 1, 1, 1, 1], [1]),
]


class TestPredict:
    @pytest.mark.parametrize("data, pred", paramed_data)
    def test_predict(self, data, pred):
        res = predict(data, smoothing_level=0.5)
        assert res == pred

    def test_predict_len(self):
        res = predict([1, 2, 3, 4, 5], smoothing_level=0.5)
        assert len(res) == 1
