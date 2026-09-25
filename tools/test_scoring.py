#!/usr/bin/env python3
"""Lightweight tests for scoring boundaries (fixed-income edition)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scoring import contains_any, score_text


def test_quant_not_quantum():
    assert contains_any("quant trading strategy", ["quant"])
    assert not contains_any("munich quantum toolkit", ["quant"])
    assert not contains_any("llm quantization awq", ["quant"])


def test_hard_negative_quantum():
    r = score_text(
        "munich-quantum-toolkit/qecc quantum error correction",
        finance_signals=["quant", "finance"],
        topic_signals=["quant", "backtest"],
        skill_signals=["toolkit"],
        blacklist=[],
    )
    assert r["rejected"]


def test_hard_negative_consumer_credit():
    """消费金融噪声（FICO/信用卡/消费贷）必须被一票否决，避免污染信用研究检索。"""
    for text in [
        "credit card default prediction with fico scoring",
        "lending club loan approval model",
        "home credit default risk kaggle",
        "信用卡违约预测 消费金融评分卡",
    ]:
        r = score_text(
            text,
            finance_signals=["credit", "finance"],
            topic_signals=["credit risk", "default"],
            skill_signals=["model"],
            blacklist=[],
        )
        assert r["rejected"], text


def test_hard_negative_crypto():
    """bonding curve / defi 不得混入债券信号。"""
    r = score_text(
        "defi bonding curve protocol for token bond issuance",
        finance_signals=["bond", "token"],
        topic_signals=["bond", "yield"],
        skill_signals=["protocol"],
        blacklist=[],
    )
    assert r["rejected"]


def test_boundary_fi_abbreviations():
    """固收缩写按词边界匹配：omo 命中，但 promotion 里的 omo 不命中。"""
    assert contains_any("omo 公开市场操作 mlf 降准", ["omo", "mlf"])
    assert not contains_any("promotion campaign video", ["omo"])
    assert not contains_any("abcdef repo1", ["cb"])
    assert contains_any("cb 转债估值", ["cb"])


def test_credit_bond_topic_pass():
    """标准信用债研究仓库应通过信用债专题评分。"""
    r = score_text(
        "fixed-income-credit-skill 信用债 城投债 信用利差 分析框架 评级跟踪",
        finance_signals=["fixed income", "信用", "利差", "债券"],
        topic_signals=["信用债", "城投债", "信用利差", "信用评级"],
        skill_signals=["framework", "skill"],
        blacklist=["game"],
    )
    assert not r["rejected"], r
    assert r["finance_hits"], r
    assert r["topic_hits"], r
    assert r["score"] >= 7, r


def test_rates_liquidity_topic_pass():
    """利率与流动性专题：资金面/超储/DR007 仓库应通过。"""
    r = score_text(
        "bank-liquidity-tracker 资金面跟踪 超储测算 dr007 逆回购 流动性日历",
        finance_signals=["流动性", "利率", "债券"],
        topic_signals=["资金面", "超储", "dr007", "逆回购", "流动性"],
        skill_signals=["tracker", "pipeline"],
        blacklist=[],
    )
    assert not r["rejected"], r
    assert r["score"] >= 7, r


if __name__ == "__main__":
    test_quant_not_quantum()
    test_hard_negative_quantum()
    test_hard_negative_consumer_credit()
    test_hard_negative_crypto()
    test_boundary_fi_abbreviations()
    test_credit_bond_topic_pass()
    test_rates_liquidity_topic_pass()
    print("OK")
