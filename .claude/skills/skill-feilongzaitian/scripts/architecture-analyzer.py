#!/usr/bin/env python3
"""
架构分析工具 - 诊断前端项目的架构质量

用法：
  python architecture-analyzer.py /path/to/project

输出：
  - 项目规模评估
  - 架构问题诊断
  - 改进建议（优先级排序）
"""

import os
import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class ArchitectureAnalyzer:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'project_path': str(project_path),
            'metrics': {},
            'issues': [],
            'recommendations': []
        }

    def analyze(self):
        """执行完整的架构分析"""
        print(f"🔍 开始分析项目：{self.project_path}")
        print("-" * 60)

        # 1. 收集基础指标
        self._collect_metrics()

        # 2. 诊断架构问题
        self._diagnose_issues()

        # 3. 生成建议
        self._generate_recommendations()

        # 4. 输出结果
        self._output_results()

    def _collect_metrics(self):
        """收集项目指标"""
        print("\n📊 收集项目指标...")

        metrics = {
            'total_files': 0,
            'total_lines': 0,
            'file_types': defaultdict(int),
            'directories': [],
            'has_package_json': False,
            'has_tsconfig': False,
            'has_eslint': False,
            'has_prettier': False,
            'has_tests': False,
            'framework_detected': None
        }

        # 扫描文件
        for root, dirs, files in os.walk(self.project_path):
            # 跳过 node_modules 等
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', 'build']]

            for file in files:
                metrics['total_files'] += 1
                ext = Path(file).suffix
                metrics['file_types'][ext] += 1

                # 计算代码行数
                if ext in ['.js', '.jsx', '.ts', '.tsx', '.vue']:
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            metrics['total_lines'] += len(f.readlines())
                    except:
                        pass

            # 检测关键文件
            if 'package.json' in files:
                metrics['has_package_json'] = True
            if 'tsconfig.json' in files:
                metrics['has_tsconfig'] = True
            if any(f in files for f in ['.eslintrc.js', '.eslintrc.json', 'eslint.config.mjs']):
                metrics['has_eslint'] = True
            if any(f in files for f in ['.prettierrc', '.prettierrc.json', 'prettier.config.js']):
                metrics['has_prettier'] = True
            if 'test' in root or '__tests__' in root or '.test.' in ''.join(files) or '.spec.' in ''.join(files):
                metrics['has_tests'] = True

        # 检测框架
        package_json_path = self.project_path / 'package.json'
        if package_json_path.exists():
            try:
                with open(package_json_path) as f:
                    package_json = json.load(f)
                    deps = {**package_json.get('dependencies', {}), **package_json.get('devDependencies', {})}

                    if 'react' in deps:
                        metrics['framework_detected'] = 'React'
                    elif 'vue' in deps:
                        metrics['framework_detected'] = 'Vue'
                    elif 'next' in deps:
                        metrics['framework_detected'] = 'Next.js'
                    elif 'nuxt' in deps:
                        metrics['framework_detected'] = 'Nuxt'
            except:
                pass

        self.results['metrics'] = {k: v if not isinstance(v, defaultdict) else dict(v) for k, v in metrics.items()}

        # 打印指标
        print(f"  ✅ 总文件数: {metrics['total_files']}")
        print(f"  ✅ 代码行数: {metrics['total_lines']}")
        print(f"  ✅ 框架: {metrics['framework_detected'] or '未检测'}")
        print(f"  ✅ TypeScript: {'✓' if metrics['has_tsconfig'] else '✗'}")
        print(f"  ✅ ESLint: {'✓' if metrics['has_eslint'] else '✗'}")
        print(f"  ✅ Prettier: {'✓' if metrics['has_prettier'] else '✗'}")
        print(f"  ✅ 测试: {'✓' if metrics['has_tests'] else '✗'}")

    def _diagnose_issues(self):
        """诊断架构问题"""
        print("\n⚠️  诊断架构问题...")

        metrics = self.results['metrics']

        # 问题 1: 缺少 TypeScript
        if not metrics['has_tsconfig']:
            self.results['issues'].append({
                'severity': 'high',
                'title': '❌ 缺少 TypeScript',
                'description': '项目未使用 TypeScript，类型安全无保障',
                'impact': '容易在生产环境中出现类型错误'
            })

        # 问题 2: 缺少代码规范工具
        if not metrics['has_eslint']:
            self.results['issues'].append({
                'severity': 'medium',
                'title': '⚠️  缺少 ESLint',
                'description': '无统一的代码风格检查',
                'impact': '团队协作中代码风格不一致'
            })

        # 问题 3: 缺少测试
        if not metrics['has_tests']:
            self.results['issues'].append({
                'severity': 'high',
                'title': '❌ 缺少测试',
                'description': '项目无自动化测试覆盖',
                'impact': '重构和升级时容易引入 bug'
            })

        # 问题 4: 项目规模大但缺少规范
        if metrics['total_lines'] > 50000 and not metrics['has_tsconfig']:
            self.results['issues'].append({
                'severity': 'critical',
                'title': '🔴 大型项目未使用 TypeScript',
                'description': f'项目规模 {metrics["total_lines"]} 行代码，严重缺乏类型保障',
                'impact': '维护难度指数增长，技术债快速累积'
            })

        for issue in self.results['issues']:
            severity_icon = '🔴' if issue['severity'] == 'critical' else '❌' if issue['severity'] == 'high' else '⚠️ '
            print(f"  {severity_icon} {issue['title']}")

    def _generate_recommendations(self):
        """生成优化建议"""
        print("\n💡 生成优化建议...")

        metrics = self.results['metrics']

        recommendations = [
            {
                'priority': 1,
                'title': '🎯 启用 TypeScript',
                'steps': [
                    '1. npm install --save-dev typescript',
                    '2. npx tsc --init',
                    '3. 将现有 .js 文件逐步迁移为 .ts',
                    '4. 配置严格模式（tsconfig.json 中设置 "strict": true）',
                    '预计耗时：中型项目 2-4 周'
                ],
                'impact': '在编译期发现 70% 以上的 bug'
            }
        ]

        if not metrics['has_eslint']:
            recommendations.append({
                'priority': 2,
                'title': '📋 配置 ESLint',
                'steps': [
                    '1. npm install --save-dev eslint eslint-plugin-react',
                    '2. npm init @eslint/config',
                    '3. 添加到 CI/CD 流程中',
                    '预计耗时：1-2 天'
                ],
                'impact': '统一代码风格，提升代码质量'
            })

        if not metrics['has_prettier']:
            recommendations.append({
                'priority': 2,
                'title': '✨ 配置 Prettier',
                'steps': [
                    '1. npm install --save-dev prettier',
                    '2. 创建 .prettierrc 配置文件',
                    '3. 配置编辑器自动格式化',
                    '预计耗时：1 天'
                ],
                'impact': '完全自动化的代码格式化'
            })

        if not metrics['has_tests']:
            recommendations.append({
                'priority': 3,
                'title': '🧪 建立测试体系',
                'steps': [
                    '1. 安装测试框架（推荐 Vitest）',
                    '2. 编写关键业务逻辑的单元测试',
                    '3. 添加集成测试（推荐 Playwright）',
                    '4. 配置 CI/CD 中的测试流程',
                    '预计耗时：中型项目 4-6 周'
                ],
                'impact': '提高重构安全性，减少线上 bug'
            })

        self.results['recommendations'] = recommendations

        for rec in recommendations:
            print(f"  {rec['priority']}. {rec['title']}")

    def _output_results(self):
        """输出分析结果"""
        print("\n" + "=" * 60)
        print("📈 分析报告")
        print("=" * 60)

        # 项目规模评估
        lines = self.results['metrics']['total_lines']
        if lines < 10000:
            scale = "🟢 小型项目（可以没有 Monorepo）"
        elif lines < 100000:
            scale = "🟡 中型项目（考虑 Monorepo）"
        else:
            scale = "🔴 大型项目（强烈建议 Monorepo + 微前端）"

        print(f"\n项目规模：{scale}")

        if self.results['issues']:
            print(f"\n发现 {len(self.results['issues'])} 个问题：")
            for issue in self.results['issues']:
                print(f"  • {issue['title']}")

        print(f"\n建议采取 {len(self.results['recommendations'])} 项改进：")
        for rec in self.results['recommendations']:
            print(f"  优先级 {rec['priority']}: {rec['title']}")

        # 保存 JSON 报告
        report_path = self.project_path / 'architecture-analysis-report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 详细报告已保存到: {report_path}")

def main():
    if len(sys.argv) < 2:
        print("用法: python architecture-analyzer.py /path/to/project")
        sys.exit(1)

    project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print(f"❌ 项目路径不存在: {project_path}")
        sys.exit(1)

    analyzer = ArchitectureAnalyzer(project_path)
    analyzer.analyze()

if __name__ == '__main__':
    main()
