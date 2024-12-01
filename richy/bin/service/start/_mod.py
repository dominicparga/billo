from fastapi import FastAPI

from richy._lib.constants import ALPHA_VANTAGE_API_KEY
from richy._lib.downloading import Downloading

app = FastAPI()


def _assert_ALPHA_VANTAGE_API_KEY() -> str:
	assert ALPHA_VANTAGE_API_KEY, "No Api Key provided."
	return ALPHA_VANTAGE_API_KEY


def assert_setup():
	_assert_ALPHA_VANTAGE_API_KEY()


@app.post(f"/{Downloading.TimeSeries.ENTRYPOINT}", response_model=Downloading.TimeSeries.Response)
async def read_root(request: Downloading.TimeSeries.Request) -> Downloading.TimeSeries.Response:
	api_key: str = _assert_ALPHA_VANTAGE_API_KEY()
	return Downloading.TimeSeries.Response.try_from(
		Downloading.TimeSeries.api_key(api_key=api_key).fetch(symbol=request.symbol)
	)
