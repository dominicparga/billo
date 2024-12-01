from enum import Enum
from typing import Any, TypeAlias, Union

import requests
from errorhandling import Result
from pydantic import BaseModel

API_KEY_TYPE: TypeAlias = str
SYMBOL_TYPE: TypeAlias = str

_URL_TEMPLATE: str = "https://www.alphavantage.co/query?apikey={apikey}&function={function}&symbol={symbol}"


class Downloading:
	class TimeSeries:
		# GENERAL

		def __init__(self, api_key: API_KEY_TYPE, is_called_privately: bool = False) -> None:
			if not is_called_privately:
				raise Exception(f"Constructor of {Downloading.TimeSeries.__class__} shall be called private only.")
			self._api_key = api_key

		class Outputsize(Enum):
			COMPACT = "compact"
			FULL = "full"

		# CLI

		@classmethod
		def api_key(cls: type["Downloading.TimeSeries"], api_key: API_KEY_TYPE) -> "Downloading.TimeSeries":
			return Downloading.TimeSeries(api_key=api_key, is_called_privately=True)

		def fetch(
			self, symbol: SYMBOL_TYPE, outputsize: Union["Downloading.TimeSeries.Outputsize", None] = None
		) -> Result.Ok[dict[str, Any]] | Result.Err[str]:
			response: requests.Response = requests.get(
				url=_URL_TEMPLATE.format(apikey=self._api_key, function="TIME_SERIES_DAILY", symbol=symbol)
			)
			data: dict[str, Any] = response.json()
			return Result.ok(data)

		# REST API

		ENTRYPOINT: str = f"download/time-series"

		class Request(BaseModel):
			symbol: str

		class Response(BaseModel):
			data: dict[str, Any]
			err_msg: str

			@classmethod
			def try_from(
				cls: type["Downloading.TimeSeries.Response"],
				result: Result.Ok[dict[str, Any]] | Result.Err[str],
			) -> "Downloading.TimeSeries.Response[dict[str, Any]]":
				if isinstance(result, Result.Ok):
					return Downloading.TimeSeries.Response(
						data=result.obj,
						err_msg="",
					)
				else:
					return Downloading.TimeSeries.Response(
						data={},
						err_msg=result.obj,
					)
