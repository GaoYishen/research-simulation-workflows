# First release

1. Choose the GitHub owner. Proposed public repository name: `research-simulation-workflows`. MIT license is already included; the copyright notice uses the project contributors' collective name.
2. Run unit tests and Skill validators. Inspect all tracked files for private content.
3. Authenticate locally with `gh auth login`. Never paste tokens into a manifest or chat.
4. Create an empty public repository, add its remote, then push the reviewed commit.
5. Publish the reviewed ZIP as a release asset if desired. Include Python 3.10+ and the scientific-validation limitation in release notes.

The initial local preparation does not itself create or publish a GitHub repository.

## Publication checklist / 发布核对

2026-11-04：用户已授权发布到个人账号 GaoYishen。MIT 已确认。本节作为后续发布的核对步骤，不表示当前仓库尚未发布。

- 完成 `gh auth login`，确认目标个人账号或组织。
- 在本仓库目录查看 `git status`，检查待发布文件和提交。
- 使用发布者自己的 Git 身份创建首次提交，不代填作者姓名或邮箱。
- 创建公开仓库前检查同名仓库是否存在，避免推送到无关项目。
- 推送后核实仓库可访问、LICENSE 和示例齐全，并查看 Actions 测试结果。
