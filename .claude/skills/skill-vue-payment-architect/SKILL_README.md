# Vue 支付平台全栈 AI Skill

🚀 **专为印度支付平台设计的Claude AI Skill** - 对标支付宝&京东金融

> 金融级别的Vue 3 + Nuxt 3开发指南，涵盖架构设计、安全合规、高性能优化

---

## 📚 Skill 完整内容

### 核心开发指南 (1,200+ 行)
**文件**: `SKILL.md`

完整的支付平台前端开发指南，包含：

**13个详细章节**：
1. 支付平台架构基础 - 三大支柱(安全、高并发、实时性)
2. 项目架构设计 - 推荐的目录结构和模块划分
3. 支付安全最佳实践 - PCI-DSS合规、数据加密、前端防护
4. 关键业务流程 - 支付状态机、KYC流程、风险控制
5. 高并发与实时性 - WebSocket实时更新、乐观更新、幂等性
6. 离线优先架构 - 数据同步、本地缓存、Service Worker
7. 多国市场支持 - 多语言、多货币支持、地区差异处理
8. 性能优化与低端设备 - Lighthouse目标、Core Web Vitals、4G优化
9. 完整案例 - 转账功能从需求到代码的完整实现
10. 测试策略 - 单元测试、集成测试、E2E测试示例
11. 生产部署清单 - 上线前的完整检查清单
12. 常见问题与故障排除 - QA和性能调试
13. 总结与最佳实践 - 核心要点回顾

**50+ 代码示例**：
- TypeScript状态机实现
- Vue 3 Composition API组件
- Pinia状态管理
- Service Worker离线缓存
- Playwright E2E测试
- 安全的API客户端配置

---

### 自动化工具脚本 (800+ 行代码)
**目录**: `scripts/`

#### 1️⃣ payment-project-init.py (400+ 行)
一键初始化支付平台项目

```bash
python scripts/payment-project-init.py \
  --name=my-payment-app \
  --features=kyc,transfer,wallet,upi
```

**功能**:
- ✅ 生成符合标准的Nuxt 3项目结构
- ✅ 自动配置TypeScript严格模式
- ✅ 生成package.json、nuxt.config.ts等配置
- ✅ 创建环境变量模板(.env.example)
- ✅ 生成PCI-DSS合规性检查清单
- ✅ 输出完整的README和下一步指南

**生成内容**:
- 项目脚手架 (src/ 完整目录结构)
- 5个配置文件 (Nuxt、TypeScript、Vite、Tailwind、package.json)
- 合规文档 (COMPLIANCE.json)
- 开发文档 (README.md)

#### 2️⃣ security-audit.py (500+ 行)
自动化代码安全审计

```bash
python scripts/security-audit.py \
  --path=. \
  --severity=high
```

**检查项** (12个不同的安全问题类别):
- 敏感数据泄露 (passwords, tokens, API keys in console/logs)
- 不安全的存储 (localStorage/sessionStorage中的敏感数据)
- eval/Function使用
- 硬编码的秘密
- 不安全的HTTP连接
- SQL注入风险
- XSS漏洞 (v-html、innerHTML)
- 过宽的CORS配置
- 缺少CSRF保护
- 弱密码验证
- 生产环境的console语句
- 注释中的敏感信息

**输出**:
- 彩色终端报告 (按严重程度分组)
- JSON格式的详细报告 (security-audit-report.json)
- 修复建议和优先级排序

#### 3️⃣ 即将推出的脚本
- `architecture-validator.py` - 验证架构和模块设计
- `compliance-checker.py` - RBI/NPCI合规性检查
- `perf-monitor.py` - 集成Playwright的性能监控

---

### 参考资源库 (2,000+ 行文档)
**目录**: `reference/`

#### 📐 payment-state-machine.md (400+ 行)
支付状态机设计完整指南

**内容**:
- 6个核心状态的定义和转换规则
- 完整的状态转换表
- TypeScript类型定义和实现
- 风险控制集成
- 幂等性和重试机制
- 网络中断处理策略
- 状态转换的守卫条件
- 完整的单元测试示例

**状态**: IDLE → VALIDATING → OTP_PENDING → PROCESSING → SUCCESS/FAILED

#### 🔐 pci-dss-compliance-guide.md (400+ 行)
PCI-DSS合规完整实施指南

**10个需求的详细说明**:
1. 安全网络 - 防火墙、默认密码、Token化
2. 不存储敏感身份数据 - 永远不存储卡号、CVV、PIN
3. 保护已存储数据 - AES-256加密、访问控制
4. 加密传输 - HTTPS/TLS 1.2+、证书固定
5. 防病毒 - CSP、XSS防护
6. 安全应用 - 输入验证、错误处理
7. 访问控制 - 最小权限原则、基于角色的访问
8. 访问ID - 用户追踪、唯一身份标识
9. 物理访问 - HTTPS、Secure标志、缓存禁用
10. 监控访问 - 审计日志、异常监控

**代码示例**:
- 安全的支付Token处理
- Web Crypto API加密
- CSP和安全头配置
- 审计日志实现

#### 📋 rbi-compliance-checklist.md (400+ 行)
印度央行 (RBI) 和NPCI完整合规清单

**8个核心要求**:
1. 数据本地化 - 所有用户数据必须在印度服务器
2. 加密标准 - AES-256、TLS 1.2+
3. 身份认证 - KYC/AML流程、3个等级
4. 审计日志 - 6年保留、不可修改、消息摘要验证
5. 风险管理 - 交易监控、黑名单检查、STR报告
6. 通知披露 - 条款、隐私政策、收费、风险披露
7. 故障处理 - 99.9%可用性、4小时RTO、1小时RPO
8. 定期审查 - 月度、季度、年度合规检查

**包含**:
- 月度/季度/年度检查清单
- 常见违规和罚款
- 相关法规列表

#### 🎨 vue-payment-form-template.vue (400+ 行)
生产就绪的支付表单组件

**3步工作流**:
1. 输入基本信息 (金额、收款人、说明)
2. 确认交易 (显示摘要、风险提示)
3. OTP验证 (发送、重新发送、超时处理)

**完整功能**:
- 输入验证 (金额、收款人、余额检查)
- 错误处理和提示
- 加载状态管理
- OTP倒计时和重新发送
- 风险警告集成
- 完整的辅助功能 (无障碍)
- Tailwind CSS样式
- TypeScript类型安全

#### 其他参考文档
- `architecture-patterns/` - 架构模式库 (即将推出)
- `code-templates/` - 代码模板库 (即将推出)
- `case-studies/` - 实际案例研究 (即将推出)

---

### MCP工具集成 (详见 MCP_INTEGRATION.md)
**文件**: `MCP_INTEGRATION.md` (13 KB)

#### Context7 集成
实时查询最新的文档和最佳实践

**使用场景**:
```
Claude → Context7: "Vue 3 WebSocket最佳实践"
Context7 → Claude: 官方文档、示例代码、最佳实践

Claude → Context7: "RBI支付规定2024"
Context7 → Claude: 最新通函、法律要求、示例
```

#### Playwright 集成
自动化E2E测试、性能测试、可访问性验证

**测试场景**:
```
E2E测试: 完整的支付流程 (KYC → 支付 → 成功)
性能测试: 4G网络模拟 (2Mbps, 100ms延迟)
可访问性: WCAG 2.1 AA标准验证
跨浏览器: Chromium, Firefox, Safari, 移动浏览器
```

---

## 🎯 使用示例

### 例子1: 初始化新项目

```bash
$ python scripts/payment-project-init.py -n payment-app -f kyc,transfer,wallet

# 输出：
# ✨ 项目初始化完成!
# 📂 项目位置: payment-app
# 📋 启用功能: kyc, transfer, wallet
#
# 下一步:
#    cd payment-app
#    npm install
#    npm run dev
```

### 例子2: 安全审计

```bash
$ python scripts/security-audit.py -p . -s high

# 输出：
# 🔍 开始安全审计: .
#
# 🔴 CRITICAL: 1 问题
#    1. 敏感数据在日志中暴露
#       📄 src/api/payment.ts:45
#       💡 移除所有敏感数据日志
#
# 🟠 HIGH: 3 问题
#
# 📊 统计
# ├─ 总问题数: 4
# ├─ 严重: 1
# └─ 高: 3
#
# 💾 报告已保存到: security-audit-report.json
```

### 例子3: 查询最新的Vue最佳实践

```
用户: @claude "我需要在Nuxt 3中实现实时余额更新"

Claude会：
1. 查看SKILL.md第5章"高并发与实时性"
2. 使用context7查询"Nuxt 3 WebSocket real-time 2024"
3. 参考reference/vue-payment-form-template.vue
4. 提供完整的useRealtimeUpdates()实现
5. 给出测试建议和性能优化提示
```

### 例子4: 验证RBI合规性

```
用户: @claude "我需要确保完全遵守RBI规定"

Claude会：
1. 使用reference/rbi-compliance-checklist.md
2. 运行security-audit.py扫描敏感数据处理
3. 使用context7查询最新的RBI通函
4. 检查数据本地化、加密、审计日志等
5. 生成详细的合规性报告和建议清单
```

---

## 📊 内容总览

| 组件 | 文件/目录 | 大小 | 内容量 |
|------|---------|------|--------|
| **核心指南** | SKILL.md | 60 KB | 1,200+ 行 |
| **脚本工具** | scripts/ | 30 KB | 900+ 行 |
| **参考资源** | reference/ | 40 KB | 1,500+ 行 |
| **MCP集成** | MCP_INTEGRATION.md | 13 KB | 400+ 行 |
| **其他文档** | README等 | 50 KB | - |
| **总计** | - | **190+ KB** | **5,000+ 行** |

---

## 🚀 关键特性

### ✅ 完全覆盖印度支付市场
- RBI数据本地化要求
- NPCI UPI支付标准
- 11种印度官方语言
- INR和国际货币支持

### 🔐 金融级安全
- PCI-DSS完整合规指南
- 敏感数据加密和处理
- 自动化安全审计工具
- CSRF、XSS、SQL注入防护

### ⚡ 高性能优化
- Core Web Vitals达成指南
- 4G网络性能优化
- Service Worker离线缓存
- 代码分割和动态导入

### 🏗️ 专业架构设计
- 模块化项目结构
- 状态机驱动的支付流程
- WebSocket实时更新
- 离线-在线无缝同步

### 🤖 AI友好的设计
- 适配Claude的学习和推理能力
- 丰富的代码示例和模板
- MCP工具集成支持
- 渐进式的难度和深度

---

## 📖 快速导航

**第一次使用?**
→ 从 README.md 开始，然后运行 `payment-project-init.py`

**想学架构设计?**
→ 阅读 SKILL.md 的第1-3章和 reference/payment-state-machine.md

**关心安全性?**
→ 学习 SKILL.md 第3章，运行 security-audit.py，查看 reference/pci-dss-compliance-guide.md

**需要合规检查?**
→ 查看 reference/rbi-compliance-checklist.md，运行 compliance-checker.py (即将推出)

**要优化性能?**
→ 参考 SKILL.md 第8章，使用 playwright 进行性能测试

**做完整实现?**
→ 研究 SKILL.md 第9章的转账案例，参考 vue-payment-form-template.vue

---

## 🎓 学习时间估计

| 水平 | 时间 | 路径 |
|------|------|------|
| **初学者** | 1-2小时 | README → SKILL.md 1-3章 → 项目初始化 |
| **中级** | 3-5小时 | 深入SKILL.md 4-8章 → 实现基本功能 |
| **高级** | 5+小时 | 精读所有文档 → 自定义脚本 → 优化部署 |

---

## ✨ Skill 的独特价值

这不仅是文档，而是：
- **智能助手**: Claude可以理解支付平台的复杂性，提供专业建议
- **自动化工具**: 一键初始化项目、审计安全、验证合规
- **最佳实践库**: 50+代码示例和完整的实现指南
- **持续学习**: 集成Context7和Playwright进行实时更新和验证

---

**现在就开始构建你的支付平台！** 🚀

```bash
# 初始化第一个项目
python scripts/payment-project-init.py --name=my-payment --features=kyc,transfer
```

---

*最后更新: 2024年11月*
*Skill版本: 1.0.0*
*Vue 3 + Nuxt 3专业版*
