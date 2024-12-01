import argparse
import logging
from enum import Enum
from getpass import getpass

from errorhandling import ErrorCode

import richy.bin.downloading.time_series
from richy._lib.constants import ALPHA_VANTAGE_API_KEY
from richy._lib.downloading import API_KEY_TYPE


class _DownloadingCmdlineExecution(Enum):
	TIME_SERIES_DAILY = "time-series-daily"


def setup_cmdline_parser(parser: argparse.ArgumentParser):
	help_msg: str

	help_msg = (
		"The API key for accessing alphavantage.co. "
		"In case this is not provided, ALPHA_VANTAGE_API_KEY from environment is checked. "
		"If the value is still empty, then user is asked if --interactive is provided."
	)
	parser.add_argument("--api-key", required=False, default=None, type=str, help=help_msg)

	parser.set_defaults(downloading_cmdline_execution=None)

	help_msg = ""
	subparsers = parser.add_subparsers(help=help_msg, required=True)

	help_msg = ""
	subparser = subparsers.add_parser(name=_DownloadingCmdlineExecution.TIME_SERIES_DAILY.value, help=help_msg)
	richy.bin.downloading.time_series.cli.setup_cmdline_parser(parser=subparser)
	subparser.set_defaults(downloading_cmdline_execution=_DownloadingCmdlineExecution.TIME_SERIES_DAILY)


def main(is_interactive: bool, parsed_args: argparse.Namespace) -> ErrorCode:
	parsed_args_api_key = parsed_args.api_key
	api_key: API_KEY_TYPE | None = None
	if not api_key:
		api_key = parsed_args_api_key
	if not api_key:
		api_key = ALPHA_VANTAGE_API_KEY
	if not api_key:
		if is_interactive:
			api_key = getpass("Please enter your ALPHA_VANTAGE_API_KEY: ")
	if not api_key:
		logging.error("Missing API Key")
		return 1

	# https://www.fintut.com/alpha-vantage-api-limits/
	# free plan: 5 per minute, 500 per day
	# paid plan: 75 per minute, inf per day

	if parsed_args.downloading_cmdline_execution == _DownloadingCmdlineExecution.TIME_SERIES_DAILY:
		return richy.bin.downloading.time_series.cli.main(
			api_key=api_key, is_interactive=is_interactive, parsed_args=parsed_args
		)
	else:
		return 1
