import pytest
import pytest_mock
import typer
from asynctor.utils import Shell

from uv_mirror.cli import SourceChoices, app


def test_list_command():
    cmd = "uv-mirror --list"
    out = Shell(cmd).capture_output()
    assert all(i.name in out for i in SourceChoices)
    cmd += " --verbose"
    out = Shell(cmd).capture_output()
    assert all(i.label in out for i in SourceChoices)


def test_list(mocker: pytest_mock.MockerFixture):
    mocker.patch("typer.echo")
    with pytest.raises(typer.exceptions.Exit):
        app(display=True)
    typer.echo.assert_called_once()  # type:ignore
    mocker.patch("typer.echo")
    mocker.patch("typer.secho")
    with pytest.raises(typer.exceptions.Exit):
        app(display=True, verbose=True)
    typer.echo.assert_called_once()  # type:ignore
    typer.secho.assert_called_once()  # type:ignore
