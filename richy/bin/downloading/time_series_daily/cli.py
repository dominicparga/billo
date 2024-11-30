import argparse
import logging

from errorhandling import ErrorCode

from .._datastructures import API_KEY_TYPE, SYMBOL_TYPE

_FUNCTION_NAME: str = "TIME_SERIES_DAILY"


def setup_cmdline_parser(parser: argparse.ArgumentParser):
	help_msg = "Stock and ETF symbols"
	parser.add_argument("--symbol", required=False, default=None, type=str, help=help_msg)


def main(api_key: API_KEY_TYPE, is_user_interaction_allowed: bool, parsed_args: argparse.Namespace) -> ErrorCode:
	parsed_args_symbol = parsed_args.symbol

	symbol: SYMBOL_TYPE | None = None
	if not symbol:
		symbol = parsed_args_symbol
	if not symbol:
		if is_user_interaction_allowed:
			symbol = input("Please enter your stock/ETF symbol: ")
	if not symbol:
		logging.error("Missing symbol")
		return 1

	from . import _mod as mod

	mod.run(api_key=api_key, function=_FUNCTION_NAME, symbol=symbol)

	return 0
