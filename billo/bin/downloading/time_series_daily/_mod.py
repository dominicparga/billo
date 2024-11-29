import json
import logging
from typing import Any, ParamSpec, Protocol, TypeVar, Union

import requests
from errorhandling import ErrorCode

from .._datastructures import API_KEY_TYPE, SYMBOL_TYPE

_URL_TEMPLATE: str = "https://www.alphavantage.co/query?apikey={apikey}&function={function}&symbol={symbol}"

_P = ParamSpec("_P")
_R = TypeVar("_R", covariant=True)


class _Functionable(Protocol[_P, _R]):
	@staticmethod
	def identifier() -> str: ...

	@classmethod
	def api_key(cls: type["_Functionable[_P, _R]"], api_key: API_KEY_TYPE) -> "_Functionable[_P, _R]": ...

	def fetch(self, *args: _P.args, **kwargs: _P.kwargs) -> _R: ...


class AlphaVantage:
	@staticmethod
	def try_from(value: str) -> Union[type["AlphaVantage.TimeSeriesDaily"], None]:
		for function in [function for function in [AlphaVantage.TimeSeriesDaily]]:
			if value.lower() == function.identifier().lower():
				return function
		return None

	class TimeSeriesDaily(_Functionable[[SYMBOL_TYPE], dict[str, Any]]):
		def __init__(self, api_key: API_KEY_TYPE, is_called_privately: bool = False) -> None:
			if not is_called_privately:
				raise Exception(
					f"Constructor of {AlphaVantage.TimeSeriesDaily.__class__} shall be called private only."
				)
			self._api_key = api_key

		@staticmethod
		def identifier() -> str:
			return "TIME_SERIES_DAILY"

		@classmethod
		def api_key(cls: type["AlphaVantage.TimeSeriesDaily"], api_key: API_KEY_TYPE) -> "AlphaVantage.TimeSeriesDaily":
			return AlphaVantage.TimeSeriesDaily(api_key=api_key, is_called_privately=True)

		def fetch(self, symbol: SYMBOL_TYPE) -> dict[str, Any]:
			response: requests.Response = requests.get(
				url=_URL_TEMPLATE.format(
					apikey=self._api_key, function=AlphaVantage.TimeSeriesDaily.identifier(), symbol=symbol
				)
			)
			data: dict[str, Any] = response.json()
			return data


def run(api_key: API_KEY_TYPE, function: str, symbol: SYMBOL_TYPE) -> ErrorCode:
	data: dict[str, Any]

	if function.lower() == AlphaVantage.TimeSeriesDaily.identifier().lower():
		client: AlphaVantage.TimeSeriesDaily = AlphaVantage.TimeSeriesDaily.api_key(api_key)
		data = client.fetch(symbol=symbol)
	else:
		raise Exception(f"Unknown AlphaVantage function: {function}")
	logging.debug(json.dumps(data, indent=4))
	return 0
