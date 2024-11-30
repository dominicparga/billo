import argparse
import sys
from enum import Enum

import richy._lib.logging
import richy.bin.downloading
from errorhandling import ErrorCode
from richy._lib.logging import SupportedLogLevel


class _CmdlineExecution(Enum):
	DOWNLOADING = "download"


def _setup_cmdline_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="richy", description="Richy is your financing and trading supporter.")

	parser.add_argument(
		"--log-level",
		type=str,
		default=SupportedLogLevel.INFO.name.lower(),
		choices=list(map(lambda sll: sll.name.lower(), SupportedLogLevel)),
	)

	help_msg: str
	parser.set_defaults(cmdline_execution=None)

	help_msg = ""
	subparsers = parser.add_subparsers(help=help_msg, required=True)

	help_msg = "TODO"
	subparser = subparsers.add_parser(name=_CmdlineExecution.DOWNLOADING.value, help=help_msg)
	richy.bin.downloading.cli.setup_cmdline_parser(parser=subparser)
	subparser.set_defaults(cmdline_execution=_CmdlineExecution.DOWNLOADING)

	return parser


def main(args: list[str] | None = None) -> ErrorCode:
	if args is None:
		args = sys.argv[1:]
	parser: argparse.ArgumentParser = _setup_cmdline_parser()
	parsed_args: argparse.Namespace = parser.parse_args(args=args)

	log_level: SupportedLogLevel | None = SupportedLogLevel.try_from(parsed_args.log_level)
	richy._lib.logging.setup(log_level=log_level)

	if parsed_args.cmdline_execution is None:
		parser.print_help()
		sys.exit(1)
	elif parsed_args.cmdline_execution == _CmdlineExecution.DOWNLOADING:
		richy.bin.downloading.cli.main(parsed_args=parsed_args)

	return 0
