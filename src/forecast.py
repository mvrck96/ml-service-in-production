from typing import List

from statsmodels.tsa.holtwinters import SimpleExpSmoothing


def predict(data: List[float], smoothing_level: float) -> float:
    """Predicts next value of given time series.

    @param data[List[float]]: Time series
    @param smoothing_level[float]: smoothing level for SES model
    @return [float]: Predicted value
    """
    model = SimpleExpSmoothing(data)
    fitted_model = model.fit(smoothing_level=smoothing_level)
    return fitted_model.predict(len(data), len(data))
