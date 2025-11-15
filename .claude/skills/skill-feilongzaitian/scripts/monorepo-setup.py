#!/usr/bin/env python3
"""
Monorepo 初始化工具 - 快速建立 Turborepo / pnpm 工作空间

用法：
  python monorepo-setup.py --name my-monorepo --manager turborepo --packages 3

生成：
  - 完整的 Monorepo 项目结构
  - turborepo.json 或 nx.json 配置
  - 工作空间 pnpm-workspace.yaml
  - 示例 package.json
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import List

class MonorepoSetup:
    def __init__(self, args):
        self.args = args
        self.root_path = Path(args.name)

    def setup(self):
        """执行 Monorepo 初始化"""
        print(f"🚀 正在初始化 Monorepo: {self.args.name}")
        print("-" * 60)

        # 创建目录结构
        self._create_directory_structure()

        # 生成配置文件
        self._generate_root_package_json()
        self._generate_pnpm_workspace()
        self._generate_monorepo_config()
        self._generate_example_packages()

        print("\n✅ Monorepo 初始化完成！")
        self._print_next_steps()

    def _create_directory_structure(self):
        """创建目录结构"""
        print("\n📁 创建目录结构...")

        dirs = [
            self.root_path / 'packages' / 'ui',
            self.root_path / 'packages' / 'utils',
            self.root_path / 'packages' / 'api',
            self.root_path / 'apps' / 'web',
            self.root_path / 'apps' / 'admin',
            self.root_path / 'apps' / 'mobile',
            self.root_path / '.github' / 'workflows',
            self.root_path / 'tools' / 'eslint-config',
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

        print(f"  ✅ 创建 {len(dirs)} 个目录")

    def _generate_root_package_json(self):
        """生成根 package.json"""
        print("\n📦 生成 package.json...")

        package_json = {
            "name": self.args.name,
            "version": "1.0.0",
            "description": "Enterprise-grade Monorepo",
            "private": True,
            "packageManager": "pnpm@9.0.0",
            "engines": {
                "node": ">=18.17.0",
                "pnpm": ">=9.0.0"
            },
            "scripts": {
                "dev": "turbo run dev",
                "build": "turbo run build",
                "test": "turbo run test",
                "lint": "turbo run lint",
                "format": "turbo run format",
                "type-check": "turbo run type-check"
            },
            "devDependencies": {
                "turbo": "^2.1.0",
                "typescript": "^5.5.0",
                "eslint": "^9.0.0",
                "prettier": "^3.0.0",
                "@types/node": "^20.0.0"
            }
        }

        config_path = self.root_path / 'package.json'
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2, ensure_ascii=False)

        print(f"  ✅ 已生成: {config_path}")

    def _generate_pnpm_workspace(self):
        """生成 pnpm-workspace.yaml"""
        print("\n🔗 生成 pnpm-workspace.yaml...")

        workspace_yaml = """packages:
  - 'packages/*'
  - 'apps/*'
  - 'tools/*'

# pnpm hoisting 策略
shamefully-hoist: true

# 快捷键配置
catalogs:
  default:
    react: ^18.3.0
    react-dom: ^18.3.0
    typescript: ^5.5.0
    vite: ^5.4.0
"""

        config_path = self.root_path / 'pnpm-workspace.yaml'
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(workspace_yaml)

        print(f"  ✅ 已生成: {config_path}")

    def _generate_monorepo_config(self):
        """生成 Turborepo 或 Nx 配置"""
        print("\n⚙️  生成 Monorepo 配置...")

        if self.args.manager == 'turborepo':
            turbo_config = {
                "$schema": "https://turbo.build/schema.json",
                "globalDependencies": ["**/.env.local", ".eslintrc"],
                "tasks": {
                    "dev": {
                        "cache": False,
                        "inputs": ["src/**/*.tsx", "src/**/*.ts"],
                        "outputs": []
                    },
                    "build": {
                        "outputs": ["dist/**", "build/**", ".next/**"],
                        "cache": True,
                        "dependsOn": ["^build"]
                    },
                    "test": {
                        "cache": False,
                        "inputs": ["src/**", "**/*.test.ts"],
                        "dependsOn": ["^build"]
                    },
                    "lint": {
                        "cache": True,
                        "inputs": ["src/**/*.ts", "src/**/*.tsx"]
                    },
                    "type-check": {
                        "cache": True
                    }
                }
            }

            config_path = self.root_path / 'turbo.json'
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(turbo_config, f, indent=2, ensure_ascii=False)

            print(f"  ✅ 已生成 Turborepo 配置: {config_path}")

    def _generate_example_packages(self):
        """生成示例包的 package.json"""
        print("\n📚 生成示例包...")

        examples = {
            'packages/ui': {
                'name': '@app/ui',
                'description': '共享 UI 组件库',
                'type': 'module',
                'exports': {
                    '.': './dist/index.js',
                    './button': './dist/button.js'
                }
            },
            'packages/utils': {
                'name': '@app/utils',
                'description': '共享工具函数库',
                'exports': {
                    '.': './dist/index.js'
                }
            },
            'apps/web': {
                'name': 'web',
                'description': '主网页应用',
                'private': True,
                'scripts': {
                    'dev': 'vite',
                    'build': 'vite build'
                }
            }
        }

        for package_path, config in examples.items():
            full_path = self.root_path / package_path

            # 创建 package.json
            package_json = {
                'version': '1.0.0',
                **config,
                'devDependencies': {}
            }

            config_path = full_path / 'package.json'
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(package_json, f, indent=2, ensure_ascii=False)

            # 创建 tsconfig.json
            tsconfig = {
                'extends': '../../tsconfig.base.json',
                'include': ['src'],
                'compilerOptions': {
                    'outDir': './dist'
                }
            }

            tsconfig_path = full_path / 'tsconfig.json'
            with open(tsconfig_path, 'w', encoding='utf-8') as f:
                json.dump(tsconfig, f, indent=2, ensure_ascii=False)

            # 创建 src 目录
            (full_path / 'src').mkdir(exist_ok=True)

        print(f"  ✅ 生成 {len(examples)} 个示例包")

    def _print_next_steps(self):
        """打印后续步骤"""
        print("\n" + "=" * 60)
        print("🎯 下一步：")
        print("=" * 60)

        steps = f"""
1️⃣  进入项目目录
   cd {self.args.name}

2️⃣  安装依赖
   pnpm install

3️⃣  启动开发服务器
   pnpm run dev

4️⃣  构建所有包
   pnpm run build

📚 推荐阅读：
   • Turborepo 官方文档：https://turbo.build
   • pnpm 官方文档：https://pnpm.io
   • Monorepo 最佳实践：https://monorepo.tools

💡 关键命令：
   # 只运行指定包的任务
   turbo run build --filter=@app/ui

   # 查看任务执行顺序
   turbo run build --graph

   # 缓存分析
   turbo run build --summarize

✨ Monorepo 的优势：
   ✅ 代码复用：共享组件、工具、类型定义
   ✅ 版本管理：统一依赖版本
   ✅ 构建优化：智能缓存，只构建变更的包
   ✅ 团队协作：清晰的包边界和职责划分
"""

        print(steps)

def main():
    parser = argparse.ArgumentParser(description='初始化 Monorepo 项目')

    parser.add_argument('name', help='项目名称')
    parser.add_argument('--manager', choices=['turborepo', 'nx'], default='turborepo',
                       help='Monorepo 管理工具（turborepo 推荐）')
    parser.add_argument('--packages', type=int, default=3, help='初始包数量')

    args = parser.parse_args()

    if Path(args.name).exists():
        print(f"❌ 目录已存在: {args.name}")
        sys.exit(1)

    setup = MonorepoSetup(args)
    setup.setup()

if __name__ == '__main__':
    main()
