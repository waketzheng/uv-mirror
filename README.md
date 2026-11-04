# uv-mirror
uv便捷换源脚本(创建或修改全局uv.toml)

## Usage

- 如果uv还没换过源，而且阿里云能通，可以这样给它换源：
```bash
# 从阿里云下载uv-mirror后，创建本地的全局uv.toml，并写入清华源
uvx --index https://mirrors.aliyun.com/pypi/simple uv-mirror qh
```
- 如果uv已经换过源，且uvx可用，直接这样换源：
```bash
# 更换为腾讯源
uvx uv-mirror tx
```
*注：uv-mirror --list列出的国内源，目前只有清华源跟官方的pypi源操持一致，会往uv.lock中写入upload-time*
