import argparse
from enum import Enum

from errorhandling import ErrorCode

import richy.bin.service.start.cli


class _ServiceCmdlineExecution(Enum):
	START = "start"


def setup_cmdline_parser(parser: argparse.ArgumentParser):
	help_msg: str

	help_msg = (
		"The API key for accessing alphavantage.co. "
		"In case this is not provided, ALPHA_VANTAGE_API_KEY from environment is checked. "
		"If the value is still empty, then user is asked if --interactive is provided."
	)
	parser.add_argument("--api-key", required=False, default=None, type=str, help=help_msg)

	help_msg = ""
	subparsers = parser.add_subparsers(help=help_msg, required=True)
	parser.set_defaults(service_cmdline_execution=None)

	help_msg = ""
	subparser = subparsers.add_parser(name=_ServiceCmdlineExecution.START.value, help=help_msg)
	richy.bin.service.start.cli.setup_cmdline_parser(parser=subparser)
	subparser.set_defaults(service_cmdline_execution=_ServiceCmdlineExecution.START)


def main(is_interactive: bool, parsed_args: argparse.Namespace) -> ErrorCode:
	if _ServiceCmdlineExecution.START == parsed_args.service_cmdline_execution:
		return richy.bin.service.start.cli.main(is_interactive=is_interactive, parsed_args=parsed_args)
	else:
		return 1
