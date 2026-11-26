import click
from click.testing import CliRunner

def test_deprecated_option_warning(capsys):
    @click.command()
    @click.option("--old-flag", deprecated=True)
    def cli(old_flag):
        click.echo("Executed!")

    runner = CliRunner()
    result = runner.invoke(cli, ["--old-flag", "value"])
    assert result.exit_code == 0
    assert "Executed!" in result.output
    assert "Option '--old-flag' is deprecated" in result.output or "deprecated" in result.output.lower()

def test_custom_deprecation_message():
    @click.command()
    @click.option("--legacy", deprecated="Use --modern instead.")
    def cli(legacy):
        click.echo("Done")

    runner = CliRunner()
    result = runner.invoke(cli, ["--legacy", "val"])
    assert result.exit_code == 0
    assert "Use --modern instead" in result.output
