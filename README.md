# Awesome Fixed-Income Skills

聚合、整理并定期更新「精而专」的**固定收益研究** skill（信用研究、利率与流动性、固收策略、机构行为、固收数据、可转债等），面向固收投研、信用研究与债券量化研究者。

> 本项目由 [awesome-financial-skills](https://github.com/) 改造而来：原项目覆盖泛金融专题（产业链、生物医药、量化交易等），本项目聚焦固收领域，并针对**信用研究**做了专项强化（城投/产业/地产/二永债、信用利差、评级违约、化债），同时屏蔽了消费金融（FICO/信用卡/消费贷）与加密领域的检索噪声。

## 目标

- 按**固收专题**发现 skill（信用债、利率与流动性、固收策略、机构行为、固收数据、可转债）
- 每个专题在评分筛选后保留约 **10 个**高质量结果（先多抓、再精选）
- 通过 CI 产出候选清单与代码包，经人工审核后合入分类文档

## 目录

- [信用债研究](categories/credit-bond.md) — 信用利差、城投/产业/地产/二永债、评级违约、化债（**旗舰专题**）
- [利率与流动性](categories/rates-liquidity.md) — 利率债、货币政策、资金面、超储、存单票据
- [固收策略](categories/fi-strategy.md) — 久期、骑乘、杠杆套息、曲线策略、利差分位数
- [机构行为](categories/institution-behavior.md) — 债基、理财、托管数据、净买入跟踪
- [固收数据](categories/bond-data.md) — 中债估值、债券行情、数据接口
- [可转债](categories/convertible.md) — 转债估值、条款博弈、转债策略

## 自动发现流水线

配置文件：`search_params.json`（按 `topics` 专题检索 + 黑名单 + 固收/技能信号词）

```text
search_params.json
        │
        ▼
tools/fetch_candidates.py   # 专题搜索 → 评分 → 每专题保留 ~10 个
        │
        ├─ candidates/by_topic/<topic_id>.json
        └─ candidates/all_candidates.json
        │
        ▼
tools/package_skills.py     # 按专题下载并解压到 artifacts/skills/<topic_id>/
        │
        ▼
tools/create_candidate_prs.py / tools/apply_candidates.py
```

评分要求同时满足：

1. 命中固收领域信号词（`finance_signals`）
2. 命中该专题信号词（`topic_signals`）
3. 综合分 ≥ `global.min_score`
4. 未命中黑名单与硬负例（消费金融/加密/量子计算等噪声）

### 本地运行

```bash
pip install -r requirements.txt
export GITHUB_TOKEN=ghp_xxx          # 可选：无 token 时降级为非认证模式（限流，仅适合小范围试用）

# 跑全部专题（每专题精选约 10 个）
python tools/fetch_candidates.py

# 只跑信用债 + 利率流动性
TOPIC_IDS=credit_bond,rates_liquidity python tools/fetch_candidates.py

# 下载精选仓库
python tools/package_skills.py
```

常用环境变量：

| 变量 | 含义 | 默认 |
|------|------|------|
| `TOPIC_IDS` | 逗号分隔专题 id | 全部 |
| `TARGET_PER_TOPIC` | 每专题保留数量 | 10 |
| `MAX_RESULTS` | 每专题搜索扫描上限 | 100 |
| `MIN_STARS` | 最低 star 数 | 3 |
| `DRY_RUN` | `1` 只预览不改库 | 1 |

专题 id 见 `search_params.json` → `topics[].id`：`credit_bond`、`rates_liquidity`、`fi_strategy`、`institution_behavior`、`bond_data`、`convertible`。

### GitHub Actions

工作流：`.github/workflows/main.yml`

- 每周一自动运行，也可手动触发并指定 `topic_ids` / `target_per_topic` / `dry_run`
- 产物 artifact：`candidates_json`（候选清单）、`skills_archive`（按专题分目录的仓库包）

## 条目格式

```markdown
- [skill-name](链接) — 一行简述。来源：xxx。最后更新时间：YYYY-MM-DD。
```

贡献与质量门槛见 [CONTRIBUTING.md](CONTRIBUTING.md)。
