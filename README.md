# Integration and Simulation

在原来的项目中加入了测试、模拟、IR-SIM benchmark、两个 reviewer 和统一入口。
原项目的源码只有 developer_agent.py 修改，其他原始文件保留。

## 安装和运行

在项目目录打开终端：

```bash
python -m pip install -r requirements.txt
ollama pull qwen3:8b
ollama serve
```

如果 Ollama 已经启动，不要重复启动服务。另开终端执行：

```bash
python main.py --force-revision
```

在线流程按顺序运行 Analyst、Planner、Developer、Test Agent、pytest、Simulation、Reviewer、IR-SIM Benchmark 和 Benchmark Reviewer。
如果测试或 benchmark 失败，Developer 接收原代码、两个 review、benchmark、requirements 和 plan，请 Qwen 生成修订代码。
修订保存在 generated/navigation_logic_revised.py，再将修订应用到运行入口并重新运行测试、模拟、两个 review 和四个 IR-SIM 环境。
默认最多修订一次，可以使用 `python main.py --max-revisions 3` 增加次数。
未通过时返回退出码 1，不把失败结果写成通过。

```bash
python main.py --offline
```

离线模式使用 tests/fixtures 内的原始结果，不调用 Qwen，也不进行 LLM 修订。
它用于检查集成流程，不能代替在线作业验证。
模拟中的 64 个状态使用原项目 plan 中的方向优先级；在线 Test Agent 另外根据本次 requirements、plan 和代码生成测试。

## 可视化

Linux、WSL 或 Git Bash 下运行老师提供的命令：

```bash
./run_visual.sh irsim_worlds/world_easy.yaml
./run_visual.sh irsim_worlds/world_medium.yaml
./run_visual.sh irsim_worlds/world_difficult.yaml
./run_visual.sh irsim_worlds/world_custom.yaml
```

Windows 也可以直接运行 `python test_irsim_with_agent.py irsim_worlds/world_easy.yaml`，然后替换环境文件名。
老师仓库中的困难环境叫 world_hard.yaml，因此保留该文件并复制为 PDF 中的 world_difficult.yaml。
run_visual.sh 和 test_irsim_with_agent.py 从老师仓库原样复制。
benchmark 通过子进程运行该脚本，使用无窗口绘图后端保存真实数值结果。

## 结果

trace.log 记录每个步骤和环境运行结果。
artifacts/simulation_report.json 保存 64 种状态的预期动作、实际动作和通过率。
artifacts/irsim_benchmark_report.json 保存四个环境的成功率、效率和平均步数。
artifacts/simulation_review.json 和 benchmark_review.json 保存评审意见。
artifacts/initial 和 revision_1 等目录保存每轮报告。
artifacts/pipeline_status.json 区分 offline 与 online，以及最终是否通过。
效率要求是到达目标且步数不超过 200，最大步数为 300，沿用老师脚本。
collision_or_done 是老师脚本的终止字段，不能仅凭该字段断言一定发生碰撞。

## 测试

```bash
python tests/test_generated_navigation_logic.py
python -m pytest tests/test_integration.py generated/test_navigation.py -q
```

交付验证详情见 VALIDATION.md。

当前仓库原先只有老师模板，现已加入你上传的原项目文件，成为可独立运行的合并版本。PDF 要求提交到原项目仓库，因此若老师指定了另一个原项目仓库，应把本次提交同步到该仓库。

在线调用关闭 Qwen 的额外思考输出。Ollama 返回 429 或 503 时最多重试两次，每次间隔 3 秒；持续失败仍会报错。trace.log 在本机运行时生成。
