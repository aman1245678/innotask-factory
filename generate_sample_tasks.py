"""
InnoTask Factory — Sample Task Generator Script for pallets/click.
Generates fully compliant Harbor v0.25 task packages.
"""

from pathlib import Path
from core.extractor import FeatureExtractor
from core.task_packager import HarborTaskPackager
from core.verifier import HarborTaskVerifier

def generate_click_tasks():
    extractor = FeatureExtractor(
        repo_url="https://github.com/pallets/click",
        baseline_commit="7eb021a68430dc0702d1d0ad510617ad4ea9ad27"
    )
    packager = HarborTaskPackager(output_root="tasks")

    # Task 1: Deprecated Option Flag
    task_1 = extractor.generate_task_from_feature_spec(
        task_id="task_click_001_deprecated_option",
        title="Add `deprecated` parameter and warning to `click.Option`",
        description=(
            "Extend Click's option decorator and Option class to support a `deprecated` flag. "
            "When users invoke a CLI command providing a deprecated option, Click should output "
            "a formatted deprecation warning to stderr without aborting command execution."
        ),
        acceptance_criteria=[
            "Support `deprecated=True` on `click.Option`, emitting warning: 'Option \"<name>\" is deprecated.'",
            "Support `deprecated=\"Custom message\"`, emitting the custom explanation string.",
            "Warnings must be emitted to sys.stderr via Click's echo or standard warnings.",
            "Command execution must succeed normally (exit code 0) after warning.",
            "All existing Click option tests and parameters must remain 100% backward-compatible."
        ],
        affected_files=["src/click/core.py"],
        feature_test_code="""import click
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
""",
        reference_patch="""--- a/src/click/core.py
+++ b/src/click/core.py
@@ -2310,6 +2310,7 @@ class Option(Parameter):
         prompt_required: bool = True,
         count: bool = False,
         show_envvar: bool = False,
+        deprecated: bool | str = False,
         **attrs: t.Any,
     ) -> None:
+        self.deprecated = deprecated
@@ -2500,6 +2501,13 @@ class Option(Parameter):
             value = self.process_value(ctx, value)
 
+        if value is not None and self.deprecated:
+            msg = f"Option '{self.opts[0]}' is deprecated." if self.deprecated is True else str(self.deprecated)
+            echo(f"Warning: {msg}", err=True)
+
         if self.expose_value:
             ctx.params[self.name] = value
""",
        difficulty="medium"
    )

    # Task 2: Case Sensitive Choice
    task_2 = extractor.generate_task_from_feature_spec(
        task_id="task_click_002_case_insensitive_choice",
        title="Add `case_sensitive=False` support to `click.Choice` parameter type",
        description=(
            "Allow `click.Choice` to accept case-insensitive user input when `case_sensitive=False`. "
            "The parsed value returned to the command function should be normalized to the canonical choice spelling."
        ),
        acceptance_criteria=[
            "Support `case_sensitive: bool = True` on `click.Choice`.",
            "When `case_sensitive=False`, choices match case-insensitively (e.g., 'RED' matches 'red').",
            "The returned parameter value must match the original choice capitalization.",
            "Invalid options must still raise `click.BadParameter` error.",
            "Default behavior must preserve strict `case_sensitive=True` matching."
        ],
        affected_files=["src/click/types.py"],
        feature_test_code="""import click
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
""",
        reference_patch="""--- a/src/click/types.py
+++ b/src/click/types.py
@@ -175,6 +175,7 @@ class Choice(ParamType):
     def __init__(
         self,
         choices: t.Sequence[str],
+        case_sensitive: bool = True,
     ) -> None:
         self.choices = choices
+        self.case_sensitive = case_sensitive
@@ -200,6 +201,11 @@ class Choice(ParamType):
         normed_value = value
+        if not self.case_sensitive:
+            match = next((c for c in self.choices if c.lower() == value.lower()), None)
+            if match is not None:
+                return match
         if normed_value in self.choices:
             return normed_value
""",
        difficulty="easy"
    )

    p1 = packager.package_task(task_1)
    p2 = packager.package_task(task_2)

    print(f"Generated task 1 at: {p1}")
    print(f"Generated task 2 at: {p2}")

    # Validate task 1
    v1 = HarborTaskVerifier(p1)
    res1 = v1.run_full_validation_suite()
    print("Task 1 Validation:", res1)

    # Validate task 2
    v2 = HarborTaskVerifier(p2)
    res2 = v2.run_full_validation_suite()
    print("Task 2 Validation:", res2)

if __name__ == "__main__":
    generate_click_tasks()
