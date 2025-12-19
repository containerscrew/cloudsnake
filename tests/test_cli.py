# from typer.testing import CliRunner
# from cloudsnake.cli.cli import app
# from importlib.metadata import version
#
# runner = CliRunner()
# app_version = version("cloudsnake")
#
#
# def test_app():
#     result = runner.invoke(app, ["version"])
#     assert result.exit_code == 0
#     assert f"cloudsnake version: {app_version}" in result.stdout
