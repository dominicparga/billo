import logging
from enum import Enum
from typing import Union


class SupportedLogLevel(Enum):
	def __init__(self, identifier: str, official_value: int) -> None:
		self._identifier: str = identifier
		self._official_value: int = official_value

	@property
	def identifier(self) -> str:
		return self._identifier

	@property
	def official_value(self) -> int:
		return self._official_value

	DEBUG = "debug", logging.DEBUG
	INFO = "info", logging.INFO
	WARN = "warn", logging.WARN
	ERROR = "error", logging.ERROR

	@classmethod
	def try_from(cls: type["SupportedLogLevel"], value: str | int) -> Union["SupportedLogLevel", None]:
		for support_log_level in SupportedLogLevel:
			if (value == support_log_level.identifier) or (value == support_log_level.official_value):
				return support_log_level
		return None


def setup(log_level: SupportedLogLevel | None):
	if log_level is None:
		log_level = SupportedLogLevel.WARN
	logging.basicConfig(
		level=log_level.official_value,
		format="[%(asctime)s][%(levelname)s] %(message)s",
		datefmt="%Y-%m-%d][%H:%M:%S",
	)
