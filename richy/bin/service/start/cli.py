import argparse
import logging

from errorhandling import ErrorCode

from richy._lib.constants import RICHY_SERVICE_HOST, RICHY_SERVICE_PORT


def setup_cmdline_parser(parser: argparse.ArgumentParser):
	help_msg = ""
	parser.add_argument("--host", required=False, default=RICHY_SERVICE_HOST, type=str, help=help_msg)
	parser.add_argument("--port", required=False, default=RICHY_SERVICE_PORT, type=int, help=help_msg)


def main(is_interactive: bool, parsed_args: argparse.Namespace) -> ErrorCode:
	host: str | None = parsed_args.host
	port: int | None = parsed_args.port

	if not host:
		if is_interactive:
			host = input("Please provide a host: ")
		else:
			logging.error("No host provided.")
			return 1

	if not port:
		if is_interactive:
			port = int(input("Please provide a port: "))
		else:
			logging.error("No port provided.")
			return 1

	from richy.bin.service.start import _mod as mod

	mod.assert_setup()

	import uvicorn

	uvicorn.run("richy.bin.service.start._mod:app", host=host, port=port, reload=True)
	return 0
