import argparse
import sys
from enum import Enum

from errorhandling import ErrorCode

import richy._lib.logging
import richy.bin.downloading
import richy.bin.service
from richy._lib.logging import SupportedLogLevel


class _CmdlineExecution(Enum):
	DOWNLOADING = "download"
	SERVICE = "service"


def _setup_cmdline_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="richy", description="Richy is your financing and trading supporter.")

	parser.add_argument(
		"--log-level",
		type=str,
		default=SupportedLogLevel.INFO.name.lower(),
		choices=list(map(lambda sll: sll.name.lower(), SupportedLogLevel)),
	)

	help_msg = "Ask user interactively for missing info."
	parser.add_argument("--interactive", action="store_true", required=False, default=None, help=help_msg)

	help_msg: str
	parser.set_defaults(cmdline_execution=None)

	help_msg = ""
	subparsers = parser.add_subparsers(help=help_msg, required=True)

	help_msg = "TODO"
	subparser = subparsers.add_parser(name=_CmdlineExecution.DOWNLOADING.value, help=help_msg)
	richy.bin.downloading.cli.setup_cmdline_parser(parser=subparser)
	subparser.set_defaults(cmdline_execution=_CmdlineExecution.DOWNLOADING)

	help_msg = "TODO"
	subparser = subparsers.add_parser(name=_CmdlineExecution.SERVICE.value, help=help_msg)
	richy.bin.service.cli.setup_cmdline_parser(parser=subparser)
	subparser.set_defaults(cmdline_execution=_CmdlineExecution.SERVICE)

	return parser


def main(args: list[str] | None = None) -> ErrorCode:
	if args is None:
		args = sys.argv[1:]
	parser: argparse.ArgumentParser = _setup_cmdline_parser()
	parsed_args: argparse.Namespace = parser.parse_args(args=args)

	log_level: SupportedLogLevel | None = SupportedLogLevel.try_from(parsed_args.log_level)
	richy._lib.logging.setup(log_level=log_level)

	is_interactive: bool = parsed_args.interactive

	if parsed_args.cmdline_execution is None:
		parser.print_help()
		sys.exit(1)
	elif parsed_args.cmdline_execution == _CmdlineExecution.DOWNLOADING:
		richy.bin.downloading.cli.main(is_interactive=is_interactive, parsed_args=parsed_args)
	elif parsed_args.cmdline_execution == _CmdlineExecution.SERVICE:
		richy.bin.service.cli.main(is_interactive=is_interactive, parsed_args=parsed_args)

	return 0
