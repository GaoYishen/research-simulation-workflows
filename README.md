# 科研仿真记录与交接 · Research Simulation Workflows

**仿真跑了很多版本，仍能找到：用了哪些参数、结果对应哪些文件、下一步该做什么。**

Research simulation tracking, SHA-256 file integrity checks, and reproducible handoff reports for scientific computing.

[![Tests](https://github.com/GaoYishen/research-simulation-workflows/actions/workflows/tests.yml/badge.svg)](https://github.com/GaoYishen/research-simulation-workflows/actions/workflows/tests.yml) ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

用一份算例清单（manifest）连接参数、输入文件、运行状态与检查证据，再生成 Markdown 交接报告。Python 3.10+ 标准库，包含三个可复用的 Agent Skills。

## 解决科研计算中的三个常见问题

| 你遇到的情况 | 这个工具怎么帮忙 |
|---|---|
| “这个结果到底是哪份输入跑出来的？” | 显式记录文件路径和 SHA-256 指纹，核对文件是否变化 |
| “任务停止了，还是已经验证通过了？” | 分别记录运行状态与声明检查结果 |
| “换个会话或换个人，还能接着做吗？” | 生成包含目标、参数、证据、限制和下一步的交接报告 |

```mermaid
flowchart LR
    A[参数与文件] --> B[算例清单 manifest]
    B --> C[文件完整性检查]
    C --> D[Markdown 交接报告]
    D --> E[继续研究或交接协作]
```

## 先看效果

仓库提供三个可复现的合成情景：

| 示例 | 运行状态 | 声明检查 |
|---|---|---|
| [synthetic-success](examples/synthetic-success) | 已完成 | 通过 |
| [synthetic-failure](examples/synthetic-failure) | 已完成 | 失败 |
| [synthetic-stopped](examples/synthetic-stopped) | 手动停止 | 尚未验证 |

还可以打开 [交互演示](demo/index.html)，查看算例记录与文件指纹的工作方式。

## 一分钟上手

```sh
git clone https://github.com/GaoYishen/research-simulation-workflows.git
cd research-simulation-workflows
python workflow.py check examples/synthetic-success/manifest.json
python workflow.py handoff examples/synthetic-success/manifest.json --output handoff.md
```

打开生成的 `handoff.md`，即可查看目标、参数、文件校验、检查结论与下一步。

Windows 可用 `py -3` 代替 `python`。输出文件采用新建方式保存。

`check` 的退出码 0 表示算例记录有效；计算结论请查看运行状态和声明检查项。

<details>
<summary>本地运行交互演示</summary>

在仓库目录运行：

```sh
python -m http.server 18766 --bind 127.0.0.1
```

打开 <http://127.0.0.1:18766/demo/>。演示使用预设情景，在浏览器本地计算合成内容的文件指纹；Python 工具则检查 manifest 中列出的实际文件。

</details>

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

## 如何理解检查结果

SHA-256 用于核对文件与已记录指纹是否一致。验证状态来自清单中声明的检查项；`reported_checks_passed` 表示已完成运行的声明检查通过且记录有效。物理模型验证需要相应计算或实验依据。

示例证据文件按原始字节计算哈希；仓库保留其原始换行符，确保 Windows/Linux 检查一致。

## 测试与贡献

```sh
python -m unittest discover -s tests -v
```

欢迎通过 Issue 提供可复现的问题或工作流需求。贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)，字段说明见 [docs/manifest.md](docs/manifest.md)，来源说明见 [PROVENANCE.md](PROVENANCE.md)。

## English overview

Portable research simulation tracking for scientific computing: create explicit case manifests, verify file integrity with SHA-256, separate run status from declared validation checks, and generate Markdown research handoff reports. Includes three Agent Skills for simulation case management, run review, and session handoff, plus synthetic examples and an interactive demo.

## 相关工具

- [有限元网格检查](https://github.com/GaoYishen/abaqus-mesh-audit)：二维网格质量与连接关系筛查。
- [电池容量与倍率核算](https://github.com/GaoYishen/battery-capacity-audit)：容量、N/P、倍率电流与厚度计算。

## License

[MIT License](LICENSE)。
