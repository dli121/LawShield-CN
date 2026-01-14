import json
import pytest
import sys
import os

# 把项目根目录加入系统路径，确保能找到 src
sys.path.append(os.getcwd())

from src.core.policy_engine import engine


def load_dataset():
    """读取测试数据集"""
    with open("tests/dataset.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("case", load_dataset())
def test_compliance_rules(case):
    """
    核心测试逻辑：
    遍历 dataset.json 里的每一个 case，
    验证 engine.check_input 的结果是否符合预期。
    """
    query = case["query"]
    expected_block = case["should_block"]

    # 调用你的规则引擎 (不消耗 API 额度，只测本地逻辑)
    is_blocked, _, _ = engine.check_input(query)

    # 断言：实际结果必须等于预期结果
    assert (
        is_blocked == expected_block
    ), f"测试失败！问题: '{query}' | 预期拦截: {expected_block} | 实际拦截: {is_blocked}"
