# Claude 自动修复 Bug 技能 - 使用指南

> 帮助开发者和团队高效使用 Claude 自动修复代码 Bug | 版本 2.0 | 2025-11-13

---

## 📚 目录

1. [入门指南](#入门指南)
2. [典型工作流程](#典型工作流程)
3. [工具命令详解](#工具命令详解)
4. [团队集成](#团队集成)
5. [常见问题](#常见问题)
6. [故障排除](#故障排除)

---

## 入门指南

### 什么是这个技能？

这个技能提供了一套完整的框架和工具，用于：
- 使用 Claude AI 自动分析代码 Bug
- 生成多个修复方案
- 输出专业的修复报告
- 提供测试和部署指导

### 核心优势

- ✅ **自动化分析** - 快速分析 Bug 的根本原因
- ✅ **多方案对比** - 获得多个修复方案的优缺点分析
- ✅ **标准化报告** - 生成可交接的专业文档
- ✅ **测试覆盖** - 自动生成单元测试和测试清单
- ✅ **最佳实践** - 遵循行业标准的修复流程

### 适用场景

| 场景 | 说明 | 优先级 |
|------|------|--------|
| **紧急 Bug** | 快速找到根本原因和修复方案 | 🔴 高 |
| **复杂问题** | 深入分析相关问题和潜在风险 | 🔴 高 |
| **知识转移** | 为新员工创建清晰的修复文档 | 🟡 中 |
| **流程建立** | 在团队中建立标准化的修复流程 | 🟡 中 |
| **代码审查** | 作为代码审查中的参考和基准 | 🟢 低 |

---

## 典型工作流程

### 流程 1: 快速修复 (15-30 分钟)

**适用**: 紧急 Bug，需要快速修复

```
步骤 1: 问题描述 (5分钟)
  ├─ 写出清晰的问题标题
  ├─ 列出复现步骤
  └─ 提供错误日志和代码片段

步骤 2: Claude 分析 (5分钟)
  ├─ 运行: fix-bug-with-codex <file> --detailed
  └─ Claude 生成修复方案

步骤 3: 快速验证 (5-10分钟)
  ├─ 阅读修复报告
  ├─ 运行建议的测试
  └─ 在本地验证修复

步骤 4: 部署 (5分钟)
  ├─ 提交代码审查
  ├─ 合并到主分支
  └─ 部署到测试环境
```

**输出**: 修复代码 + 快速验证通过

### 流程 2: 深度分析 (1-2 小时)

**适用**: 复杂 Bug，需要多方案对比和文档

```
步骤 1: 完整问题描述 (10分钟)
  ├─ 提供所有 10 个必需要素
  ├─ 包含详细的代码片段
  ├─ 环境信息完整
  └─ 提供相关的日志和截图

步骤 2: Claude 7 阶段分析 (20分钟)
  ├─ Stage 1: 问题分析
  ├─ Stage 2: 代码定位
  ├─ Stage 3: 根本原因分析
  ├─ Stage 4: 方案设计
  ├─ Stage 5: 代码实现
  ├─ Stage 6: 测试设计
  └─ Stage 7: 报告生成

步骤 3: 方案评估 (15分钟)
  ├─ 理解所有提议的方案
  ├─ 对比优缺点
  └─ 选择最适合项目的方案

步骤 4: 完整测试 (20分钟)
  ├─ 运行所有生成的单元测试
  ├─ 执行集成测试
  ├─ 验证边界情况
  └─ 检查回归测试清单

步骤 5: 文档整理 (10分钟)
  ├─ 整理修复报告
  ├─ 记录决策理由
  ├─ 准备部署指导
  └─ 更新项目文档

步骤 6: 部署准备 (5分钟)
  ├─ 准备回滚计划
  ├─ 通知相关团队
  └─ 设置监控告警
```

**输出**: 完整修复报告 + 测试用例 + 部署指导

### 流程 3: 团队流程建立 (半天工作坊)

**适用**: 为整个团队建立标准化的修复流程

```
阶段 1: 培训 (1 小时)
  ├─ 介绍技能和工作流程
  ├─ 讲解 10 个必需要素
  ├─ 演示 Claude 分析过程
  └─ Q&A

阶段 2: 实践 (1.5 小时)
  ├─ 选择 1-2 个现有的 Bug
  ├─ 分小组使用工作流程
  ├─ 生成修复报告
  └─ 互相审查和讨论

阶段 3: 流程定制 (1 小时)
  ├─ 根据项目情况定制模板
  ├─ 建立 Bug 描述的团队标准
  ├─ 定义修复报告的要求
  └─ 集成到开发工作流程中

阶段 4: 反馈和优化 (持续)
  ├─ 收集团队反馈
  ├─ 迭代改进流程
  ├─ 分享成功案例
  └─ 定期审查和更新
```

**输出**: 团队标准 + 模板库 + 最佳实践指南

---

## 工具命令详解

### 命令格式

```bash
fix-bug-with-codex <source_file> [options]
```

### 常用命令示例

```bash
# 示例 1: 基础分析
fix-bug-with-codex app.py --language python

# 示例 2: 详细报告
fix-bug-with-codex login.js --language javascript --detailed

# 示例 3: 指定 Bug 位置
fix-bug-with-codex main.rs --language rust --line 45 --context 15

# 示例 4: 输出到文件
fix-bug-with-codex api.js --output fix_report.md --detailed

# 示例 5: 使用自定义配置
fix-bug-with-codex service.py --model claude-opus --temperature 0.2 --max-tokens 3000

# 示例 6: 处理多文件问题
fix-bug-with-codex main.js --context 20 --detailed --output comprehensive_report.md
```

### 选项详解

#### 必需选项

| 选项 | 说明 | 例子 |
|------|------|------|
| `<source_file>` | 要分析的源文件路径 | `app.py`, `login.js` |

#### 推荐选项

| 选项 | 说明 | 默认值 | 例子 |
|------|------|--------|------|
| `--language` | 编程语言（通常自动检测） | 自动 | `--language python` |
| `--detailed` | 生成详细分析报告 | false | `--detailed` |
| `--output` | 输出文件路径 | stdout | `--output report.md` |

#### 高级选项

| 选项 | 说明 | 默认值 | 范围 |
|------|------|--------|------|
| `--line` | Bug 所在行号 | 全文件 | 正整数 |
| `--context` | 上下文行数（前后各 N 行） | 10 | 5-50 |
| `--model` | Claude 模型版本 | claude-opus-4 | claude-opus, claude-sonnet |
| `--temperature` | 创意度（低=稳定，高=多样） | 0.2 | 0.0-1.0 |
| `--max-tokens` | 最大 Token 数 | 3000 | 1000-8000 |

#### 配置文件

创建 `.codex-config.yaml` 保存常用配置：

```yaml
# .codex-config.yaml
claude:
  model: "claude-opus-4"
  temperature: 0.2
  max_tokens: 3000

output:
  format: "markdown"
  include_tests: true
  include_explanation: true
  include_alternatives: true

analysis:
  depth: "deep"           # shallow, medium, deep
  include_refactoring: true
  security_check: true
  performance_check: true

reporting:
  include_deployment_guide: true
  include_rollback_plan: true
  include_monitoring_setup: true
```

---

## 团队集成

### 集成到 GitHub Workflow

```yaml
# .github/workflows/auto-bug-fix.yml
name: Automated Bug Analysis

on:
  issues:
    types: [labeled]

jobs:
  analyze-bug:
    runs-on: ubuntu-latest
    if: contains(github.event.issue.labels.*.name, 'bug')

    steps:
      - uses: actions/checkout@v3

      - name: Analyze Bug with Claude
        run: |
          fix-bug-with-codex \
            src/problematic_file.js \
            --detailed \
            --output bug_analysis.md

      - name: Add Analysis to Issue
        run: |
          gh issue comment ${{ github.event.issue.number }} \
            --body "## 自动 Bug 分析已完成\n\n$(cat bug_analysis.md)"
```

### 集成到开发工作流程

#### 步骤 1: 标准化 Bug 模板

在 `.github/ISSUE_TEMPLATE/bug_report.md` 中：

```markdown
---
name: Bug Report
about: 报告一个 Bug
title: "[BUG] "
labels: bug
---

<!-- 填写以下 10 个必需要素 -->

## 1. Bug 标题
<!-- 简洁的 Bug 摘要（50 字以内）-->

## 2. 问题描述
<!-- 详细说明 Bug 的表现形式 -->

## 3. 复现步骤
<!-- 清晰的分步说明 -->
1. ...
2. ...

## 4. 预期行为
<!-- 如果正常应该发生什么 -->

## 5. 实际行为
<!-- 当前系统实际做了什么 -->

## 6. 环境信息
- OS:
- Browser:
- Version:

## 7. 错误日志
<!-- 完整的堆栈跟踪 -->

## 8. 代码片段
<!-- 相关的代码片段（10-20 行）-->

## 9. 影响范围
<!-- 受影响用户、严重等级 -->

## 10. 附加信息
<!-- 相关 Issue、临时解决方案 -->
```

#### 步骤 2: 创建修复工作流程

1. Bug 报告提交
2. 团队成员运行分析: `fix-bug-with-codex <file> --detailed`
3. 在 PR 中包含修复报告
4. 代码审查和测试验证
5. 部署和监控

#### 步骤 3: 文档化决策

在每个 PR 的描述中包含：

```markdown
## 修复说明

### 问题分析
<!-- Claude 的根本原因分析摘要 -->

### 选择的方案
<!-- 为什么选择这个方案而不是其他 -->

### 测试验证
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 回归测试清单检查

### 部署计划
<!-- 部署步骤和监控指标 -->
```

---

## 常见问题

### Q1: Bug 描述不完整时怎么办？

**A**: 使用 10 要素检查清单：

1. 如果缺少信息，请求用户补充
2. 从可用信息出发，提出具体的问题
3. 例如：
   ```
   "我看到你提到了 CORS 错误。能否提供：
   - 完整的错误日志？
   - 您使用的浏览器版本？
   - 重现问题的具体步骤？"
   ```

### Q2: 应该使用哪个 Claude 模型？

**A**: 根据场景选择：

| 模型 | 速度 | 准确度 | 成本 | 推荐场景 |
|------|------|--------|------|---------|
| claude-opus-4 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 高 | 复杂 Bug 深度分析 |
| claude-sonnet | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中 | 日常 Bug 修复（推荐） |
| claude-opus | ⭐⭐⭐⭐ | ⭐⭐⭐ | 低 | 快速初步分析 |

### Q3: 如何处理安全敏感的代码？

**A**:

1. **不要提交生产环境代码** - 使用示例或匿名化代码
2. **使用本地工具** - 如果可能，在本地运行分析
3. **过滤敏感数据** - 移除密钥、密码、用户数据
4. **标记为机密** - 在报告中标记敏感信息

示例：

```javascript
// ✅ 安全的代码提交方式
async function authenticateUser(credentials) {
  // 敏感信息已移除
  const response = await apiCall('/auth', {
    username: '[REDACTED]',
    password: '[REDACTED]'
  });
  return response;
}
```

### Q4: 多人合作时如何协调？

**A**: 遵循以下流程：

1. **Bug 报告者** - 提供完整描述
2. **分析负责人** - 运行 Claude 分析
3. **技术负责人** - 评估修复方案
4. **实现开发者** - 实现选定方案
5. **代码审查者** - 审查修复代码
6. **QA 团队** - 验证修复
7. **发布负责人** - 监控部署

### Q5: 如何避免修复不适当的问题？

**A**:

1. **再现问题** - 自己重现 Bug 以确认存在
2. **理解根本原因** - 不要只表面修复
3. **检查类似问题** - 查看是否有相关问题
4. **评估修复范围** - 修复是否过度或不足
5. **编写测试** - 测试用例会帮助验证修复

---

## 故障排除

### 问题 1: "找不到代码文件"

**症状**: 运行命令后提示找不到文件

**解决方案**:
```bash
# 确认文件路径
ls -la src/problematic_file.js

# 使用绝对路径
fix-bug-with-codex /full/path/to/file.js
```

### 问题 2: "语言检测失败"

**症状**: Claude 无法识别编程语言

**解决方案**:
```bash
# 显式指定语言
fix-bug-with-codex app.js --language javascript
```

### 问题 3: "生成的代码在我的环境中不工作"

**症状**: 修复代码不适用于项目

**解决方案**:
1. 提供更多的环境信息
2. 包含项目的依赖版本
3. 提供完整的错误日志
4. 请求 Claude 生成替代方案

### 问题 4: "报告太长或太短"

**症状**: 生成的报告不符合预期

**解决方案**:
```bash
# 调整详细程度
fix-bug-with-codex file.js --detailed        # 更详细
fix-bug-with-codex file.js                   # 简洁版

# 调整 Token 上限
fix-bug-with-codex file.js --max-tokens 5000  # 更长的报告
```

### 问题 5: "我需要多个修复方案"

**症状**: 只得到一个修复方案

**解决方案**:
1. 在 Bug 描述中明确要求多个方案
2. 使用 `--detailed` 标志获得详细分析
3. 询问 Claude 考虑的替代方案

---

## 最佳实践检查清单

### 每次提交 Bug 描述前

- [ ] 包含 Bug 标题（简洁准确）
- [ ] 提供完整的复现步骤
- [ ] 包含预期和实际行为
- [ ] 列出环境信息（OS、浏览器、版本）
- [ ] 提供错误日志或堆栈跟踪
- [ ] 包含代码片段（标注行号）
- [ ] 说明影响范围和严重等级
- [ ] 附加任何相关信息

### 收到修复报告后

- [ ] 仔细阅读根本原因分析
- [ ] 理解所有提议的修复方案
- [ ] 对比不同方案的优缺点
- [ ] 在本地环境验证修复
- [ ] 运行所有推荐的测试
- [ ] 检查是否有相关或相似问题

### 实施修复前

- [ ] 获得代码审查批准
- [ ] 确保所有测试通过
- [ ] 准备好回滚计划
- [ ] 通知相关团队成员
- [ ] 设置监控和告警

### 部署和监控

- [ ] 在测试环境验证
- [ ] 灰度部署到 5-10% 用户
- [ ] 监控错误率和性能指标（24-48 小时）
- [ ] 无问题后全量部署
- [ ] 收集用户反馈
- [ ] 更新相关文档

---

## 下一步

### 新手开发者
1. 阅读快速参考 (QUICK-REFERENCE.md)
2. 完成一次快速修复流程
3. 学习 10 个必需要素
4. 实践深度分析流程

### 技术负责人
1. 为团队定制修复模板
2. 建立 Bug 描述标准
3. 整合到 GitHub Workflow
4. 培训团队成员

### 项目经理
1. 了解修复流程需要的时间
2. 为 Bug 分析分配资源
3. 跟踪修复进度
4. 收集团队反馈

---

## 获得帮助

- **完整指南**: 参考 SKILL.md
- **快速参考**: 参考 QUICK-REFERENCE.md
- **问题报告**: 在 GitHub 提交 Issue
- **反馈建议**: 分享您的使用经验

---

版本: 2.0 | 最后更新: 2025-11-13 | Claude AI Development Team

**开始使用**: 提供完整的 Bug 描述 → 运行分析 → 获得修复方案 → 部署和监控
