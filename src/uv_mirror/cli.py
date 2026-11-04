import socket
from typing import Annotated

import typer
from asynctor.enums import TextChoices
from pip_conf import SOURCES, System, UvMirror  # type:ignore[import-untyped]


def set_http_global_timeout() -> None:
    socket.setdefaulttimeout(5)


class SourceChoices(TextChoices):
    tx = "tencent", "腾讯"
    ali = "aliyun", "阿里"
    qh = "qinghua", "清华"
    db = "douban", "豆瓣"
    dx = "dianxin", "电信"
    hw = "huawei", "华为"
    gf = "pypi", "官方"
    cer = "cernet", "联合"


def _parse_domain(value: str) -> str:
    rest = value.split("://", 1)[-1]
    return rest.split("/", 1)[0]


def resolve_source(value: str) -> tuple[str, str]:
    if value.startswith("http"):
        return value, "" if value.startswith("https") else _parse_domain(value)
    try:
        s = SourceChoices[value]
    except KeyError:
        try:
            s = SourceChoices(value)
        except ValueError:
            try:
                s = {i.label: i for i in SourceChoices}[value]  # type:ignore[assignment]
            except KeyError:
                # TODO: ecs
                raise typer.Abort(f"Unknown source {value!r}") from None
    slim = SOURCES[s.value]
    url = f"https://{slim}/simple"
    return url, ""


def app(
    source: Annotated[str | None, typer.Argument(help="镜像源别名或完整URL")] = None,
    display: Annotated[bool, typer.Option("--list", help="展示镜像源别名")] = False,
    python: Annotated[
        str | None, typer.Option(help="python standalone镜像地址")
    ] = None,
    no_python: Annotated[
        bool, typer.Option("--no-python", help="擦除python standalone镜像地址")
    ] = False,
    extra: Annotated[str | None, typer.Option(help="备选镜像源")] = None,
    force: Annotated[
        bool,
        typer.Option("-y", "--force", "--noinput", "--no-input", help="无需确认全选Y"),
    ] = False,
    verbose: bool = False,
) -> None:
    if display:
        aliases = "\n".join(i.name for i in SourceChoices)
        typer.echo(f"镜像源列表：\n{aliases}")
        if verbose:
            text = "\n".join(
                f"{i.value}({i.name}): {i.label}\n{resolve_source(i.value)[0]}"
                for i in SourceChoices
            )
            typer.secho(f"\n对应关系：\n{text}", fg=typer.colors.CYAN)
        raise typer.Exit()
    url, _ = resolve_source(source or "qh")  # TODO: find out the fastest source
    extra_info = None
    if extra is not None:
        extra_info = resolve_source(extra)[::-1]  # to be optimized
    is_windows = System.is_win()
    # TODO: auto backup config file when removing python mirror without --no-python
    set_http_global_timeout()
    rc = UvMirror(
        url, is_windows, replace=force, extra_info=extra_info, verbose=verbose
    ).set(python)
    if rc:  # return code must be 0 or None
        raise typer.Exit(rc)


def main() -> None:
    typer.run(app)


if __name__ == "__main__":
    main()
