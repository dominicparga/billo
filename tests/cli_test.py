def test_cli():
	from richy.bin import cli

	assert cli.main is not None
