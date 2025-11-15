#!/usr/bin/env python3
"""
TypeScript 配置生成器 - 根据项目特征生成最优的 tsconfig.json

用法：
  python typescript-config-generator.py --react --nextjs --strict

生成：
  - 推荐的 tsconfig.json
  - 解释每个配置项的含义
"""

import json
import sys
import argparse
from pathlib import Path

class TypeScriptConfigGenerator:
    def __init__(self, args):
        self.args = args
        self.config = self._generate_config()

    def _generate_config(self):
        """生成推荐的 TypeScript 配置"""
        base_config = {
            "compilerOptions": {
                # 目标和模块
                "target": "ES2022",
                "lib": ["ES2022", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "moduleResolution": "bundler",

                # 严格性设置
                "strict": self.args.strict,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noImplicitReturns": True,
                "noImplicitAny": True,
                "exactOptionalPropertyTypes": True,

                # 模块解析
                "baseUrl": ".",
                "paths": {
                    "@/*": ["./src/*"],
                    "@components/*": ["./src/components/*"],
                    "@features/*": ["./src/features/*"],
                    "@hooks/*": ["./src/hooks/*"],
                    "@utils/*": ["./src/utils/*"],
                    "@types/*": ["./src/types/*"]
                },

                # JSX 配置
                "jsx": "react-jsx" if self.args.react else "preserve",
                "jsxImportSource": self.args.react_import if self.args.react else None,

                # 输出配置
                "outDir": "./dist",
                "declaration": True,
                "declarationMap": True,
                "sourceMap": True,
                "removeComments": False,

                # 互操作性
                "esModuleInterop": True,
                "allowSyntheticDefaultImports": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True,

                # 实验性特性（如果 Next.js）
                "experimentalDecorators": self.args.nextjs or self.args.decorators,
                "useDefineForClassFields": True,

                # 增量编译
                "incremental": True,
                "tsBuildInfoFile": "./node_modules/.cache/.tsbuildinfo"
            },
            "include": [
                "src/**/*",
                "*.config.ts",
                ".eslintrc.ts"
            ],
            "exclude": [
                "node_modules",
                "dist",
                "build",
                ".next"
            ]
        }

        # 移除 None 值
        base_config["compilerOptions"] = {k: v for k, v in base_config["compilerOptions"].items() if v is not None}

        return base_config

    def generate(self):
        """生成配置文件"""
        output_path = Path(self.args.output) if self.args.output else Path('tsconfig.json')

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

        print(f"✅ TypeScript 配置已生成: {output_path}")
        self._print_explanation()

    def _print_explanation(self):
        """打印配置解释"""
        print("\n" + "=" * 60)
        print("📖 配置解释")
        print("=" * 60)

        explanations = {
            "target": "编译目标（ES2022 支持最新特性，但需要现代浏览器）",
            "strict": "严格模式（开启所有严格检查，推荐总是开启）",
            "noUnusedLocals": "检查未使用的本地变量，帮助清理死代码",
            "noImplicitAny": "不允许隐式 any 类型，强制显式类型声明",
            "baseUrl": "模块解析的基础路径，与 paths 配合使用",
            "paths": "路径别名（@/* 替代 ../../../）",
            "jsx": "JSX 编译方式（react-jsx 是新方式，不需要 import React）",
            "declaration": "生成 .d.ts 类型定义文件",
            "sourceMap": "生成 source map，便于调试",
            "esModuleInterop": "允许 CommonJS 和 ES6 模块互操作"
        }

        print("\n🔑 关键配置项：")
        for key, explanation in explanations.items():
            print(f"  • {key}: {explanation}")

        print("\n✨ 最佳实践：")
        print("  1. 总是开启 strict 模式（即使初期成本高）")
        print("  2. 使用路径别名避免深层相对路径")
        print("  3. 定期运行 tsc --noEmit 检查类型")
        print("  4. 在 CI/CD 中检查 TypeScript 编译错误")

def main():
    parser = argparse.ArgumentParser(description='生成推荐的 TypeScript 配置')

    parser.add_argument('--react', action='store_true', help='项目使用 React')
    parser.add_argument('--nextjs', action='store_true', help='项目使用 Next.js')
    parser.add_argument('--vue', action='store_true', help='项目使用 Vue')
    parser.add_argument('--strict', action='store_true', default=True, help='启用严格模式（默认开启）')
    parser.add_argument('--decorators', action='store_true', help='使用装饰器')
    parser.add_argument('--react-import', default='react', help='React import source')
    parser.add_argument('--output', '-o', help='输出文件路径')

    args = parser.parse_args()

    print("🔧 正在生成 TypeScript 配置...")
    print("-" * 60)

    generator = TypeScriptConfigGenerator(args)
    generator.generate()

if __name__ == '__main__':
    main()
