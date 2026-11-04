# Manifest v1

文件采用 UTF-8 JSON；示例和模板是字段的完整示范。

| 字段 | 含义 |
|---|---|
| schema_version | 固定为 1 |
| case_id / objective | 算例标识与目的，非空字符串 |
| parameters | name、value、unit 列表；无量纲单位写 1 |
| files | 明确列出的相对路径与 SHA-256；至少一个 |
| run_status | not_started / running / completed / failed / stopped / unknown |
| checks | name、criterion、status、evidence；status 为 pass / fail / not_run |
| limitations | 已知限制列表 |
| next_action | 下一项具体行动 |

执行过的检查必须引用 files 中已索引的证据文件。路径使用 /，禁止绝对路径、.. 及越出算例目录的符号链接。
记录完整性错误会令 check 返回 1；格式/文件读取错误返回 2。记录有效返回 0，包括尚未开始或声明检查失败的记录。
必须另外查看 validation：not_established / reported_checks_failed / reported_checks_passed。
空 checks、未完成运行、缺失证据或哈希错误均不能产生 reported_checks_passed。
本工具不独立审查 criterion 是否充分，也不验证文件内容是否支持声明。
