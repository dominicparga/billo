import logging
import os
import sys
from pathlib import Path

# set env-path
# checking whether I'm running as bundled applicatino (exe) or as script
# https://stackoverflow.com/a/51061279
_is_running_as_app_not_as_script: bool = getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


if _is_running_as_app_not_as_script:
	_repo_root_dirpath = Path(str(sys._MEIPASS))  # type: ignore
else:
	# root of whole repo, not root of the python app
	_repo_root_dirpath = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent

# read in .env
if not _is_running_as_app_not_as_script:
	env_filepath: Path = _repo_root_dirpath.joinpath(".env")
	if env_filepath.exists():
		with open(file=_repo_root_dirpath.joinpath(".env"), mode="r", encoding="UTF-8") as env_file:
			for line in env_file.readlines():
				line = line.strip()
				if line.startswith("#"):
					continue
				if len(line) == 0:
					continue

				k, v = line.split("=")

				k = k.strip().strip('"')
				v = v.strip().strip('"')

				if k not in os.environ:
					os.environ[k] = v
	else:
		logging.info("Env file {} does not exist.", env_filepath)


ALPHA_VANTAGE_API_KEY: str | None = os.environ.get("ALPHA_VANTAGE_API_KEY")
RICHY_SERVICE_HOST: str | None = os.environ.get("RICHY_SERVICE_HOST")
RICHY_SERVICE_PORT: int | None = int(os.environ["RICHY_SERVICE_PORT"]) if os.environ.get("RICHY_SERVICE_PORT") else None
RICHY_SERVICE_CERT_PEM_FILEPATH: str | None = os.environ.get("RICHY_SERVICE_CERT_PEM_FILEPATH")
RICHY_SERVICE_KEY_PEM_FILEPATH: str | None = os.environ.get("RICHY_SERVICE_KEY_PEM_FILEPATH")
RICHY_SERVICE_KEY_PEM_PASSWORD: str | None = os.environ.get("RICHY_SERVICE_KEY_PEM_PASSWORD")
