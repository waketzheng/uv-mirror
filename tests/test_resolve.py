import pytest
import typer

from uv_mirror.cli import SourceChoices, resolve_source


class TestResolve:
    def test_well_know_source(self):
        url, insecure_host = resolve_source(SourceChoices.tx.name)
        url2, insecure_host2 = resolve_source(SourceChoices.tx.value)
        url3, insecure_host3 = resolve_source(SourceChoices.tx.label)
        assert url == url2 == url3 == "https://mirrors.cloud.tencent.com/pypi/simple"
        assert insecure_host == insecure_host2 == insecure_host3 == ""

    def test_custom_source(self):
        url, insecure_host = resolve_source("http://private.domain.com")
        url2, insecure_host2 = resolve_source("http://private.domain.com/pypi/simple")
        url3, insecure_host3 = resolve_source("http://private.domain.com/pypi/simple/")
        assert url == "http://private.domain.com"
        assert url2 == "http://private.domain.com/pypi/simple"
        assert url3 == "http://private.domain.com/pypi/simple/"
        assert insecure_host == insecure_host2 == insecure_host3 == "private.domain.com"

    def test_invalid_source(self):
        with pytest.raises(
            typer.exceptions.Abort, match="Unknown source 'invalid-source'"
        ):
            resolve_source("invalid-source")
