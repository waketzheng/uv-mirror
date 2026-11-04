import pytest_mock

import uv_mirror.cli
from uv_mirror.cli import app


def test_set(mocker: pytest_mock.MockerFixture):
    mocker.patch("uv_mirror.cli.UvMirror.set", return_value=None)
    app()
    uv_mirror.cli.UvMirror.set.assert_called_once()  # type:ignore
