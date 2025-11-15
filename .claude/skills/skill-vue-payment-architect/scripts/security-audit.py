#!/usr/bin/env python3
"""
支付平台安全审计脚本

功能：
- 扫描代码中的安全问题
- 检查敏感数据处理
- 验证加密和认证机制
- 生成安全报告

使用：
  python security-audit.py --path=/path/to/project --severity=high
"""

import os
import re
import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Any
from enum import Enum
from datetime import datetime


class Severity(Enum):
    """安全问题严重程度"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SecurityIssue:
    """安全问题"""
    def __init__(
        self,
        severity: Severity,
        title: str,
        description: str,
        file: str,
        line: int,
        code: str,
        fix: str
    ):
        self.severity = severity
        self.title = title
        self.description = description
        self.file = file
        self.line = line
        self.code = code
        self.fix = fix

    def to_dict(self) -> Dict[str, Any]:
        return {
            'severity': self.severity.value,
            'title': self.title,
            'description': self.description,
            'file': str(self.file),
            'line': self.line,
            'code': self.code,
            'fix': self.fix,
        }


class SecurityAuditor:
    """安全审计器"""

    # 不安全的模式
    PATTERNS = {
        # 敏感数据在日志中
        'sensitive_in_log': {
            'patterns': [
                r'console\.log\(["\'].*?(password|token|apiKey|secret|otp|cvv|cardNumber)["\'].*?\)',
                r'console\.warn\(["\'].*?(password|token|apiKey|secret|otp|cvv|cardNumber)["\'].*?\)',
                r'console\.error\(["\'].*?(password|token|apiKey|secret|otp|cvv|cardNumber)["\'].*?\)',
            ],
            'severity': Severity.CRITICAL,
            'title': '敏感数据在日志中暴露',
            'description': '密码、令牌等敏感信息不应该出现在日志中',
        },

        # localStorage中存储敏感数据
        'sensitive_in_storage': {
            'patterns': [
                r'localStorage\.setItem\(["\']?(password|token|apiKey|secret|cvv|cardNumber)["\']?',
                r'sessionStorage\.setItem\(["\']?(password|token|apiKey|secret|cvv|cardNumber)["\']?',
            ],
            'severity': Severity.CRITICAL,
            'title': '敏感数据存储在本地存储中',
            'description': '敏感数据不应该在localStorage/sessionStorage中。使用内存或仅存储加密的token',
        },

        # 使用了eval
        'eval_usage': {
            'patterns': [
                r'\beval\s*\(',
                r'Function\s*\(["\']',
            ],
            'severity': Severity.CRITICAL,
            'title': '使用了eval或Function构造器',
            'description': '动态代码执行是严重的安全风险',
        },

        # 明文API密钥
        'hardcoded_secrets': {
            'patterns': [
                r'apiKey\s*[:=]\s*["\'][a-zA-Z0-9_-]+["\']',
                r'secretKey\s*[:=]\s*["\'][a-zA-Z0-9_-]+["\']',
                r'bearerToken\s*[:=]\s*["\'][a-zA-Z0-9_-]+["\']',
            ],
            'severity': Severity.CRITICAL,
            'title': '硬编码的API密钥或秘密',
            'description': '不要在代码中硬编码敏感信息，使用环境变量',
        },

        # 使用http而非https
        'insecure_http': {
            'patterns': [
                r'http://[\w.-]+\.(com|io|net|org|edu|gov)',
                r'["\']http://api\.',
            ],
            'severity': Severity.HIGH,
            'title': '使用了不安全的HTTP连接',
            'description': '支付相关的所有通信必须使用HTTPS/WSS',
        },

        # SQL注入风险
        'sql_injection': {
            'patterns': [
                r'query\s*\(\s*["\'].*\$\{.*\}',
                r'execute\s*\(\s*["\'].*\+.*id',
            ],
            'severity': Severity.HIGH,
            'title': '潜在的SQL注入风险',
            'description': '使用参数化查询而不是字符串拼接',
        },

        # XSS风险 (v-html)
        'xss_risk': {
            'patterns': [
                r'v-html\s*=',
                r'innerHTML\s*=',
            ],
            'severity': Severity.HIGH,
            'title': '潜在的XSS漏洞',
            'description': '避免使用v-html或innerHTML。Vue会自动转义文本内容',
        },

        # CORS配置过宽
        'overly_permissive_cors': {
            'patterns': [
                r"Access-Control-Allow-Origin.*\*",
                r"origin:\s*\*",
                r'allowOrigin.*\*',
            ],
            'severity': Severity.HIGH,
            'title': 'CORS配置过于宽松',
            'description': '不要允许所有源访问。指定具体的域名',
        },

        # 缺少CSRF保护
        'missing_csrf': {
            'patterns': [
                r'post\s*\(["\'].*["\'].*\{',
                r'put\s*\(["\'].*["\'].*\{',
            ],
            'severity': Severity.MEDIUM,
            'title': '可能缺少CSRF令牌',
            'description': '所有修改操作(POST/PUT/DELETE)都应该包含CSRF令牌',
        },

        # 错误的密码验证
        'weak_password_check': {
            'patterns': [
                r'password\s*===\s*',
                r'password\s*==\s*',
                r'String\(password\)\s*===',
            ],
            'severity': Severity.MEDIUM,
            'title': '在前端进行密码验证',
            'description': '密码验证应该在后端进行。前端只用于UX反馈',
        },

        # console语句未移除
        'console_statements': {
            'patterns': [
                r'console\.log\s*\(',
                r'console\.debug\s*\(',
            ],
            'severity': Severity.LOW,
            'title': '生产环境中保留了console语句',
            'description': '移除所有console.log和console.debug语句，或使用条件编译',
        },

        # 注释中的敏感信息
        'sensitive_in_comments': {
            'patterns': [
                r'//\s*TODO.*password',
                r'//\s*FIXME.*password',
                r'//\s*TODO.*secret',
                r'//\s*FIXME.*key',
            ],
            'severity': Severity.MEDIUM,
            'title': '注释中包含敏感信息',
            'description': '不要在代码注释中记录敏感信息如密码、密钥等',
        },
    }

    def __init__(self, project_path: str, min_severity: Severity = Severity.LOW):
        """
        初始化安全审计器

        Args:
            project_path: 项目路径
            min_severity: 最小严重程度阈值
        """
        self.project_path = Path(project_path)
        self.min_severity = min_severity
        self.issues: List[SecurityIssue] = []

    def run(self) -> bool:
        """执行审计"""
        if not self.project_path.exists():
            print(f"❌ 项目路径不存在: {self.project_path}")
            return False

        print(f"🔍 开始安全审计: {self.project_path}\n")

        # 扫描文件
        self._scan_files()

        # 生成报告
        self._generate_report()

        return len([i for i in self.issues if i.severity == Severity.CRITICAL]) == 0

    def _scan_files(self):
        """扫描项目文件"""
        print("📁 扫描项目文件...")

        # 需要扫描的文件类型
        extensions = {'.ts', '.tsx', '.js', '.jsx', '.vue', '.json'}
        exclude_dirs = {'node_modules', '.git', 'dist', '.nuxt', '.next'}

        for file_path in self.project_path.rglob('*'):
            # 跳过目录
            if file_path.is_dir():
                if file_path.name in exclude_dirs:
                    continue
                continue

            # 检查文件扩展名
            if file_path.suffix not in extensions:
                continue

            try:
                self._scan_file(file_path)
            except Exception as e:
                print(f"  ⚠️  无法扫描 {file_path}: {e}")

    def _scan_file(self, file_path: Path):
        """扫描单个文件"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        lines = content.split('\n')

        # 对每个模式进行检查
        for pattern_name, pattern_config in self.PATTERNS.items():
            patterns = pattern_config['patterns']
            severity = pattern_config['severity']

            if self._should_check_severity(severity):
                for pattern in patterns:
                    try:
                        for match in re.finditer(pattern, content, re.IGNORECASE):
                            # 计算行号
                            line_num = content[:match.start()].count('\n') + 1
                            line_content = lines[line_num - 1] if line_num <= len(lines) else ''

                            issue = SecurityIssue(
                                severity=severity,
                                title=pattern_config['title'],
                                description=pattern_config['description'],
                                file=file_path,
                                line=line_num,
                                code=line_content.strip(),
                                fix=self._get_fix_suggestion(pattern_name),
                            )
                            self.issues.append(issue)
                    except re.error:
                        pass

    def _should_check_severity(self, severity: Severity) -> bool:
        """检查是否应该检查该严重程度"""
        severity_order = {
            Severity.CRITICAL: 5,
            Severity.HIGH: 4,
            Severity.MEDIUM: 3,
            Severity.LOW: 2,
            Severity.INFO: 1,
        }
        return severity_order[severity] >= severity_order[self.min_severity]

    def _get_fix_suggestion(self, pattern_name: str) -> str:
        """获取修复建议"""
        fixes = {
            'sensitive_in_log': '使用日志库，添加日志过滤器来移除敏感数据',
            'sensitive_in_storage': '使用内存变量存储，或只存储加密的令牌',
            'eval_usage': '使用JSON.parse()代替eval，避免动态代码执行',
            'hardcoded_secrets': '将密钥移到环境变量或密钥管理系统',
            'insecure_http': '使用HTTPS和WSS进行所有连接',
            'sql_injection': '使用参数化查询或ORM框架',
            'xss_risk': '让Vue自动转义，或使用DOMPurify库',
            'overly_permissive_cors': '在服务器配置中指定具体的允许源',
            'missing_csrf': '在所有修改请求中包含CSRF令牌',
            'weak_password_check': '在后端验证密码，前端只显示错误提示',
            'console_statements': '使用条件编译或移除console语句',
            'sensitive_in_comments': '从注释中移除敏感信息',
        }
        return fixes.get(pattern_name, '参考代码审查指南')

    def _generate_report(self):
        """生成审计报告"""
        print(f"\n📊 审计结果\n")

        if not self.issues:
            print("✅ 未发现安全问题！")
            return

        # 按严重程度分组
        by_severity = {}
        for issue in self.issues:
            if issue.severity not in by_severity:
                by_severity[issue.severity] = []
            by_severity[issue.severity].append(issue)

        # 显示问题
        severity_order = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]
        total_issues = len(self.issues)

        for severity in severity_order:
            if severity not in by_severity:
                continue

            issues = by_severity[severity]
            emoji = self._get_severity_emoji(severity)
            print(f"{emoji} {severity.value.upper()}: {len(issues)} 问题\n")

            for i, issue in enumerate(issues[:5], 1):  # 每个严重程度最多显示5个
                print(f"   {i}. {issue.title}")
                print(f"      📄 {issue.file}:{issue.line}")
                print(f"      📝 {issue.code}")
                print(f"      💡 {issue.description}")
                print(f"      ✨ {issue.fix}")
                print()

            if len(issues) > 5:
                print(f"   ... 还有 {len(issues) - 5} 个问题\n")

        # 总结
        print(f"\n📈 统计")
        print(f"├─ 总问题数: {total_issues}")
        critical = len(by_severity.get(Severity.CRITICAL, []))
        high = len(by_severity.get(Severity.HIGH, []))
        print(f"├─ 严重: {critical}")
        print(f"├─ 高: {high}")
        print(f"└─ 其他: {total_issues - critical - high}")

        # 保存JSON报告
        self._save_json_report()

        if critical > 0:
            print(f"\n❌ 发现 {critical} 个严重问题，必须修复！")
        elif high > 0:
            print(f"\n⚠️  发现 {high} 个高级问题，建议修复")
        else:
            print(f"\n✅ 安全问题已修复或仅为低级问题")

    def _get_severity_emoji(self, severity: Severity) -> str:
        """获取严重程度的表情符号"""
        emojis = {
            Severity.CRITICAL: '🔴',
            Severity.HIGH: '🟠',
            Severity.MEDIUM: '🟡',
            Severity.LOW: '🟢',
            Severity.INFO: '🔵',
        }
        return emojis.get(severity, '❓')

    def _save_json_report(self):
        """保存JSON格式的报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'project': str(self.project_path),
            'total_issues': len(self.issues),
            'issues': [issue.to_dict() for issue in self.issues],
            'summary': {
                'critical': len([i for i in self.issues if i.severity == Severity.CRITICAL]),
                'high': len([i for i in self.issues if i.severity == Severity.HIGH]),
                'medium': len([i for i in self.issues if i.severity == Severity.MEDIUM]),
                'low': len([i for i in self.issues if i.severity == Severity.LOW]),
            },
        }

        report_path = self.project_path / 'security-audit-report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n💾 报告已保存到: {report_path}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='支付平台安全审计工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python security-audit.py --path=/path/to/project
  python security-audit.py -p . --severity=high
        """
    )

    parser.add_argument(
        '-p', '--path',
        default='.',
        help='项目路径 (默认: 当前目录)',
    )

    parser.add_argument(
        '-s', '--severity',
        default='low',
        choices=['critical', 'high', 'medium', 'low', 'info'],
        help='最小严重程度 (默认: low)',
    )

    args = parser.parse_args()

    try:
        severity = Severity(args.severity)
        auditor = SecurityAuditor(args.path, severity)
        success = auditor.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
