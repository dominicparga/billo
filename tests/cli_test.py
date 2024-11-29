def test_cli():
	from billo.bin import cli

	assert cli.main is not None
