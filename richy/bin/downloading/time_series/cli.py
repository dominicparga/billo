import argparse
import json
import logging
from typing import Any

from errorhandling import ErrorCode, Result

from richy._lib.downloading import API_KEY_TYPE, SYMBOL_TYPE


def setup_cmdline_parser(parser: argparse.ArgumentParser):
	help_msg = "Stock and ETF symbols"
	parser.add_argument("--symbol", required=False, default=None, type=str, help=help_msg)


def _run(api_key: API_KEY_TYPE, symbol: str) -> ErrorCode:
	from richy._lib.downloading._mod import Downloading

	result: Result.Ok[dict[str, Any]] | Result.Err[str] = Downloading.TimeSeries.api_key(api_key=api_key).fetch(
		symbol=symbol
	)
	if isinstance(result, Result.Ok):
		logging.info(json.dumps(result.obj, indent=4))
	else:
		logging.error(result.obj)

	return 0


def main(api_key: API_KEY_TYPE, is_interactive: bool, parsed_args: argparse.Namespace) -> ErrorCode:
	parsed_args_symbol = parsed_args.symbol

	symbol: SYMBOL_TYPE | None = None
	if not symbol:
		symbol = parsed_args_symbol
	if not symbol:
		if is_interactive:
			symbol = input("Please enter your stock/ETF symbol: ")
	if not symbol:
		logging.error("Missing symbol")
		return 1

	return _run(api_key=api_key, symbol=symbol)
