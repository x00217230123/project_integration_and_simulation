# 验证记录

本次用原项目的 fixture 导航逻辑运行离线集成流程，实际运行了老师提供的 IR-SIM 脚本。

- 64 种状态：64 通过，0 失败。
- 原项目导航检查：14 通过，0 失败。
- pytest：64 个导航用例和 9 个集成检查，共 73 通过。
- easy：到达目标，150 步。
- medium：到达目标，148 步。
- difficult：到达目标，187 步。
- custom：到达目标，193 步。
- 成功率：100%，效率率：100%，平均步数：169.5。

4 个环境的 collision_or_done 均为 false。
报告、环境输出和 trace.log 已保留。
老师的 run_visual.sh、test_irsim_with_agent.py 和原始世界文件与导入仓库逐字节相同。
从上传的原项目合并的文件中，只有 developer_agent.py 改变；原有测试、fixture、生成代码和旧 artifacts 均保留。main.py 等集成模块在老师模板基础上完成。
GitHub 版本另增加了独立的 Ollama 客户端，关闭额外思考并对 429/503 重试，未修改 analyst_agent.py 或 planner_agent.py 的内容。
新增文件没有额外代码注释，developer_agent.py 原有注释保留。

这里没有 Ollama 服务，Qwen 的实际生成、评审和修订没有在线运行，不能声称已经验证。
修订函数的输入传递、代码验证和独立文件保存通过模拟模型响应的单元测试。
本机安装 Ollama 和 qwen3:8b 后运行 `python main.py --force-revision`，可以强制演示一次实际修订并重新运行测试、模拟和四个 IR-SIM 环境。
在线结果可能与离线结果不同，应检查新的 pipeline_status.json 和各项报告。
