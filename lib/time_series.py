from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from pandas import Series

class TS(object):
    def __init__(self):
        self.model = None
        self.output = None
        self.sarimax_param = None

    @staticmethod
    def sarimax_best_param(ts_data, periodicity, verbose=False):
        """
        p       AR "autoregressive" parameters
        d       differences
        ma      MA "Moving Average" parameters
        s       Periodicity
        """
        p = d = q = (0, 1)
        pdq = [(ar, diff, ma) for ar in p for diff in d for ma in q]
        pdqs = [(c[0], c[1], c[2], periodicity) for c in pdq]

        params, value = (None, None)
        for pdq_params in pdq:
            for pdqs_params in pdqs:
                output = TS.sarimax_model(ts_data, pdq_params, pdqs_params)
                if value is None or output.aic < value:
                    params, value = ((pdq_params, pdqs_params), output.aic)
                    if verbose:
                        print('SARIMA Parameters:', (pdq_params, pdqs_params),'AIC:', output.aic)
        return params

    @staticmethod
    def sarimax_model(ts_data, order, seasonal_order, enforce_stationarity=False, enforce_invertibility=False):
        model = SARIMAX(endog=ts_data,
                        order=order,
                        seasonal_order=seasonal_order,
                        enforce_stationarity=False,
                        enforce_invertibility=False
                        )
        output = model.fit(maxiter=250)
        return output


    @staticmethod
    def adf_test(ts_data):
        dftest = adfuller(ts_data)
        dfoutput = Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
        for key,value in dftest[4].items():
            dfoutput['Critical Value (%s)'%key] = value
        return dfoutput