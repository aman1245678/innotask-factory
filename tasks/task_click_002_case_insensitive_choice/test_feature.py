import click
import pytest
from click.testing import CliRunner

def test_case_insensitive_choice():
    choice_type = click.Choice(["Apple", "Banana"], case_sensitive=False)
    ctx = click.Context(click.Command("test"))
    
    # Should normalize uppercase to canonical choice
    assert choice_type.convert("apple", None, ctx) == "Apple"
    assert choice_type.convert("BANANA", None, ctx) == "Banana"

def test_case_insensitive_invalid():
    choice_type = click.Choice(["Apple", "Banana"], case_sensitive=False)
    ctx = click.Context(click.Command("test"))
    with pytest.raises(click.BadParameter):
        choice_type.convert("Cherry", None, ctx)
