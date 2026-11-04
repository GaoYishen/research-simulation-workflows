# Research Simulation Workflows

给科研计算建立可追溯的算例清单、检查文件完整性，并生成可继续工作的交接报告。
Portable case manifests, integrity checks, and research handoffs.

这是独立的科研工作流工具，不包含 PRIME 求解器、计算方法源码、真实项目数据或软件许可证。
只需 Python 3.10+，无第三方 Python 依赖，也不要求安装 Abaqus。

## 立即试用

想先看效果，可打开 `demo/index.html` 查看合成算例交互演示。若浏览器不允许本地文件使用 SHA-256，在仓库目录运行 `python -m http.server 18766 --bind 127.0.0.1`，然后打开 `http://127.0.0.1:18766/demo/`。演示不读取真实文件；网页中的运行状态为预设情景，文件指纹在浏览器本地计算。此演示独立于下方 Python 工具。

下载仓库 ZIP 并解压，在仓库目录打开终端：

```sh
python workflow.py check examples/synthetic-success/manifest.json
python workflow.py handoff examples/synthetic-success/manifest.json --output handoff.md
python -m unittest discover -s tests -v
```

Windows 也可用 `py` 代替 `python`。脚本拒绝覆盖已有输出文件。
三个示例分别展示：已完成且声明检查通过、已完成但检查失败、手动停止且尚未验证。
失败示例的记录本身可以完整有效；`check` 返回 0 只表示记录有效，不表示计算成功。
示例证据文件按原始字节计算哈希；`.gitattributes` 禁止 Git 自动转换这些 `.txt` 文件的换行符，以保持 Windows/Linux 检查一致。编辑器若改变文件换行，也会被视为文件变化。

## 用于自己的算例

```sh
python workflow.py init /path/to/case --id demo-001 --files input.txt run.log --output /path/to/case/manifest.json
python workflow.py check /path/to/case/manifest.json
python workflow.py handoff /path/to/case/manifest.json --output my-handoff.md
```

`init` 只索引明确列出的文件，不扫描整个项目。manifest 必须放在算例目录根部。
创建后编辑 objective、parameters、run_status、checks、limitations、next_action。
模板见 [templates/manifest.json](templates/manifest.json)，字段说明见 [docs/manifest.md](docs/manifest.md)。
先声明验收标准，再记录运行和验证证据；文件更新后应建立新记录，不能用更新哈希掩盖非预期变更。

## 三个 Agent Skills

- `simulation-case-manifest`：建立参数、文件和来源清单。
- `simulation-run-review`：检查完整性，区分运行状态和验证结论。
- `research-session-handoff`：保留证据、限制与下一步。

保留整个仓库；让支持 Agent Skills 的助手读取 `skills/<name>/SKILL.md` 即可使用。
这三个 Skill 共用仓库根部脚本，不能只复制一个 SKILL.md 后删除其余仓库文件。
示例请求：“请按 simulation-run-review 检查 examples/synthetic-stopped/manifest.json，并说明还能得出哪些结论。”

## 能力边界

SHA-256 检查只能发现相对已记录哈希的文件变化；不能证明文件来源真实。
验证状态基于使用者声明的检查项，工具不会重新计算物理指标，也不会解析任意求解器日志。
`reported_checks_passed` 仅表示已完成运行的声明检查均通过且记录有效，不是完整模型验证认证。
当前不执行求解器、不上传数据、不调用大模型服务。

## 来源与发布

本仓库根据科研计算记录的通用需求新写。未复制第三方插件或已有 Skill 正文。
所有示例均为合成记录，无专有求解器接口。见 [PROVENANCE.md](PROVENANCE.md)。
贡献要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。发布步骤见 [docs/release.md](docs/release.md)。

## License

本仓库采用 [MIT License](LICENSE)，允许使用、修改与再分发，并要求保留版权及许可声明。
授权仅适用于本仓库包含的内容；不包含 PRIME 私有求解器、未公开研究资料或商业求解软件的使用权。
