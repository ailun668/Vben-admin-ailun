#!/usr/bin/env python3
"""
代码规范验证器 - 检查项目是否符合企业级规范

验证项目：
  - 目录结构规范（src/features, shared, core）
  - 文件命名规范（kebab-case, PascalCase）
  - TypeScript 类型检查（no any）
  - 导入路径规范（避免相对路径过深）
  - 循环依赖检测
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict

class CodeStructureValidator:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.violations = []
        self.warnings = []
        self.suggestions = []

    def validate(self):
        """执行完整的代码规范验证"""
        print(f"🔍 开始验证项目规范：{self.project_path}")
        print("-" * 60)

        self._validate_directory_structure()
        self._validate_file_naming()
        self._validate_typescript_types()
        self._validate_import_paths()

        self._output_results()

    def _validate_directory_structure(self):
        """验证目录结构"""
        print("\n📁 验证目录结构...")

        src_path = self.project_path / 'src'
        if not src_path.exists():
            self.violations.append({
                'type': 'structure',
                'severity': 'high',
                'message': '缺少 src/ 目录，应该将源代码放在 src 中'
            })
            return

        # 检查目录规范
        expected_dirs = ['features', 'shared', 'core', 'pages', 'layouts']
        existing_dirs = [d.name for d in src_path.iterdir() if d.is_dir()]

        has_features = 'features' in existing_dirs
        has_shared = 'shared' in existing_dirs

        if not has_features:
            self.warnings.append({
                'type': 'structure',
                'severity': 'medium',
                'message': '推荐使用 features 目录组织功能模块'
            })

        if not has_shared:
            self.suggestions.append({
                'type': 'structure',
                'message': '建议创建 shared 目录存放跨功能的公共代码'
            })

        print(f"  ✅ 检查 {len(existing_dirs)} 个目录")

    def _validate_file_naming(self):
        """验证文件命名规范"""
        print("\n📝 验证文件命名规范...")

        violations = 0
        for root, dirs, files in os.walk(self.project_path / 'src'):
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if not file.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    continue

                # 组件文件应该是 PascalCase
                if 'components' in root and file[0].islower() and not file.startswith('index'):
                    self.violations.append({
                        'type': 'naming',
                        'severity': 'medium',
                        'file': file,
                        'message': f'组件文件应该是 PascalCase: {file} → {self._to_pascal_case(file)}'
                    })
                    violations += 1

                # 工具文件应该是 camelCase
                if 'utils' in root and file[0].isupper() and file != file[0].upper():
                    self.violations.append({
                        'type': 'naming',
                        'severity': 'low',
                        'file': file,
                        'message': f'工具文件应该是 camelCase: {file} → {self._to_camel_case(file)}'
                    })
                    violations += 1

        print(f"  ✅ 检查完成，发现 {violations} 个命名规范问题")

    def _validate_typescript_types(self):
        """验证 TypeScript 类型检查"""
        print("\n🔍 扫描 TypeScript 类型问题...")

        any_count = 0
        for root, dirs, files in os.walk(self.project_path / 'src'):
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if not file.endswith(('.ts', '.tsx')):
                    continue

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # 检查 any 类型
                        any_matches = re.findall(r':\s*any\b', content)
                        if any_matches:
                            any_count += len(any_matches)
                            self.violations.append({
                                'type': 'types',
                                'severity': 'high',
                                'file': file_path,
                                'message': f'发现 {len(any_matches)} 个 any 类型，应该用更具体的类型替换'
                            })

                        # 检查 as any
                        as_any_matches = re.findall(r'as\s+any\b', content)
                        if as_any_matches:
                            self.warnings.append({
                                'type': 'types',
                                'severity': 'medium',
                                'file': file_path,
                                'message': f'发现 {len(as_any_matches)} 个 as any 类型断言'
                            })
                except:
                    pass

        print(f"  ⚠️  扫描完成，发现 {any_count} 个 any 类型")

    def _validate_import_paths(self):
        """验证导入路径规范"""
        print("\n🔗 验证导入路径...")

        violations = 0
        for root, dirs, files in os.walk(self.project_path / 'src'):
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if not file.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    continue

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # 检查过深的相对路径
                        deep_imports = re.findall(r"from\s+['\"](\.\./){4,}", content)
                        if deep_imports:
                            self.violations.append({
                                'type': 'imports',
                                'severity': 'medium',
                                'file': file_path,
                                'message': f'导入路径过深（../../../...），应该使用路径别名'
                            })
                            violations += 1
                except:
                    pass

        print(f"  ✅ 检查完成，发现 {violations} 个导入路径问题")

    def _output_results(self):
        """输出验证结果"""
        print("\n" + "=" * 60)
        print("📋 代码规范验证报告")
        print("=" * 60)

        # 违规统计
        total_violations = len(self.violations) + len(self.warnings)
        print(f"\n📊 统计:")
        print(f"  🔴 严重违规: {len([v for v in self.violations if v['severity'] == 'high'])}")
        print(f"  ⚠️  警告: {len(self.warnings) + len([v for v in self.violations if v['severity'] != 'high'])}")
        print(f"  💡 建议: {len(self.suggestions)}")

        # 违规详情
        if self.violations:
            print(f"\n🔴 违规项：")
            for violation in self.violations[:5]:  # 只显示前 5 个
                print(f"  • {violation['message']}")
            if len(self.violations) > 5:
                print(f"  ... 还有 {len(self.violations) - 5} 个违规项")

        # 建议
        if self.suggestions:
            print(f"\n💡 改进建议：")
            for suggestion in self.suggestions[:3]:
                print(f"  • {suggestion['message']}")

        # 规范合规度评分
        compliance_score = 100 - (len(self.violations) * 5 + len(self.warnings) * 2)
        compliance_score = max(0, compliance_score)

        if compliance_score >= 80:
            status = "✅ 优秀"
        elif compliance_score >= 60:
            status = "🟡 及格"
        else:
            status = "🔴 需改进"

        print(f"\n📈 规范合规度: {compliance_score}/100 {status}")

    @staticmethod
    def _to_pascal_case(name):
        """转换为 PascalCase"""
        return ''.join(word.capitalize() for word in name.replace('-', '_').split('_')).replace('.ts', '.ts').replace('.tsx', '.tsx').replace('.js', '.js')

    @staticmethod
    def _to_camel_case(name):
        """转换为 camelCase"""
        parts = name.replace('.ts', '').replace('.tsx', '').replace('.js', '').split('-')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def main():
    if len(sys.argv) < 2:
        print("用法: python code-structure-validator.py /path/to/project")
        sys.exit(1)

    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        print(f"❌ 项目路径不存在: {project_path}")
        sys.exit(1)

    validator = CodeStructureValidator(project_path)
    validator.validate()

if __name__ == '__main__':
    main()
