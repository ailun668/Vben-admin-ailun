#!/usr/bin/env python3
"""
支付平台项目初始化脚本

功能：
- 生成符合支付平台标准的Nuxt 3项目结构
- 自动配置安全相关的依赖和配置
- 创建合规性检查清单
- 生成环境配置模板

使用：
  python payment-project-init.py --name=my-payment-app --features=kyc,transfer,upi
"""

import os
import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class PaymentProjectInit:
    """支付平台项目初始化器"""

    SUPPORTED_FEATURES = {
        'kyc': 'KYC身份验证流程',
        'transfer': '用户转账功能',
        'upi': 'UPI支付集成',
        'wallet': '钱包和余额管理',
        'settlement': '结算和对账',
        'risk-control': '风险控制和反欺诈',
    }

    PROJECT_STRUCTURE = {
        'src': {
            'features': {
                'auth': {
                    'components': ['LoginForm.vue', 'OTPVerify.vue', 'KYCUpload.vue'],
                    'composables': ['useAuth.ts', 'useKYC.ts'],
                    'stores': ['authStore.ts'],
                    'types': ['auth.ts'],
                },
                'wallet': {
                    'components': ['WalletCard.vue', 'BalanceDisplay.vue', 'RechargeModal.vue'],
                    'composables': ['useWallet.ts', 'useBalance.ts'],
                    'stores': ['walletStore.ts'],
                    'types': ['wallet.ts'],
                },
                'transaction': {
                    'components': ['PaymentForm.vue', 'TransactionStatus.vue', 'TransactionHistory.vue'],
                    'composables': ['usePayment.ts', 'useTransactionState.ts'],
                    'stores': ['transactionStore.ts'],
                    'types': ['transaction.ts'],
                },
                'risk-control': {
                    'composables': ['useRiskDetection.ts', 'useAnomalyAlert.ts'],
                    'stores': ['riskStore.ts'],
                },
                'settlement': {
                    'composables': ['useSettlement.ts'],
                    'stores': ['settlementStore.ts'],
                },
            },
            'shared': {
                'security': ['encryption.ts', 'audit.ts', 'validation.ts'],
                'realtime': ['websocket.ts', 'reconnect.ts', 'handlers.ts'],
                'offline': ['sync.ts', 'storage.ts', 'queue.ts'],
                'components': ['ErrorBoundary.vue', 'LoadingSpinner.vue', 'ConfirmDialog.vue'],
                'composables': ['useNetworkStatus.ts', 'useErrorHandler.ts', 'useLocalization.ts'],
            },
            'infrastructure': {
                'state-machine': ['paymentStateMachine.ts', 'transactionFlow.ts'],
                'error-recovery': ['retryStrategy.ts', 'fallback.ts'],
                'api': ['client.ts', 'interceptors.ts', 'types.ts'],
                'i18n': ['en.json', 'hi.json', 'mr.json'],
            },
            'pages': ['index.vue', 'wallet.vue'],
            'layouts': ['default.vue', 'auth.vue'],
        },
        'tests': {
            'unit': {},
            'integration': {},
            'e2e': {},
        },
    }

    def __init__(self, project_name: str, features: List[str]):
        """
        初始化项目生成器

        Args:
            project_name: 项目名称 (会转换为小写+连字符)
            features: 要启用的功能列表
        """
        self.project_name = project_name.lower().replace(' ', '-')
        self.project_path = Path(self.project_name)
        self.features = [f for f in features if f in self.SUPPORTED_FEATURES]
        self.timestamp = datetime.now().isoformat()

    def validate_features(self) -> bool:
        """验证选择的功能"""
        invalid = [f for f in self.features if f not in self.SUPPORTED_FEATURES]
        if invalid:
            print(f"❌ 不支持的功能: {', '.join(invalid)}")
            print(f"支持的功能: {', '.join(self.SUPPORTED_FEATURES.keys())}")
            return False
        return True

    def create_directory_structure(self):
        """创建项目目录结构"""
        print(f"📁 创建项目目录结构: {self.project_name}/")
        self._create_dirs(self.project_path, self.PROJECT_STRUCTURE)

    def _create_dirs(self, base_path: Path, structure: Dict[str, Any]):
        """递归创建目录和文件"""
        for key, value in structure.items():
            current_path = base_path / key

            if isinstance(value, dict):
                # 目录
                current_path.mkdir(parents=True, exist_ok=True)
                self._create_dirs(current_path, value)
            elif isinstance(value, list):
                # 文件列表
                current_path.mkdir(parents=True, exist_ok=True)
                for filename in value:
                    file_path = current_path / filename
                    if not file_path.exists():
                        file_path.touch()
                        print(f"  ✓ {file_path}")

    def create_configuration_files(self):
        """创建配置文件"""
        print("\n⚙️  创建配置文件...")

        # nuxt.config.ts
        nuxt_config = self._generate_nuxt_config()
        self._write_file(self.project_path / 'nuxt.config.ts', nuxt_config)

        # tsconfig.json
        tsconfig = self._generate_tsconfig()
        self._write_file(self.project_path / 'tsconfig.json', tsconfig)

        # vite.config.ts
        vite_config = self._generate_vite_config()
        self._write_file(self.project_path / 'vite.config.ts', vite_config)

        # tailwind.config.ts
        tailwind_config = self._generate_tailwind_config()
        self._write_file(self.project_path / 'tailwind.config.ts', tailwind_config)

        # package.json
        package_json = self._generate_package_json()
        self._write_file(self.project_path / 'package.json', package_json)

    def _generate_nuxt_config(self) -> str:
        """生成Nuxt配置"""
        return """// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  // 模块
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@nuxt/image',
    '@vueuse/nuxt',
  ],

  // TypeScript
  typescript: {
    strict: true,
    shim: false,
  },

  // 路由
  router: {
    options: {
      hashMode: false,
    },
  },

  // 运行时配置
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'https://api.payment.example.com',
      wsBase: process.env.NUXT_PUBLIC_WS_BASE || 'wss://api.payment.example.com',
    },
  },

  // 安全头
  nitro: {
    headers: {
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
      'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    },
  },

  // CSS
  css: ['~/assets/styles/main.css'],

  // 构建优化
  build: {
    transpile: ['crypto-js', '@vueuse/core'],
  },

  // 实验性功能
  experimental: {
    payloadExtraction: false,
    renderJsonPayload: true,
  },

  // 日志
  logLevel: process.env.NODE_ENV === 'production' ? 'warn' : 'info',
})
"""

    def _generate_tsconfig(self) -> str:
        """生成TypeScript配置"""
        return """{
  "extends": "./node_modules/nuxt/dist/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,

    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "esModuleInterop": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,

    "baseUrl": ".",
    "paths": {
      "~/*": ["./*"],
      "@/*": ["./src/*"],
    }
  },
  "include": [".nuxt/dist/app/index.d.ts", "./**/*.ts", "./**/*.d.ts", "./**/*.vue"],
  "exclude": ["node_modules", "dist", ".nuxt"]
}
"""

    def _generate_vite_config(self) -> str:
        """生成Vite配置"""
        return """import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '~': resolve(__dirname, './'),
    },
  },

  build: {
    target: 'ES2022',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
      format: {
        comments: false,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          'vue': ['vue'],
          'crypto': ['crypto-js'],
          'utils': ['date-fns', 'lodash-es'],
        },
      },
    },
    sourcemap: process.env.NODE_ENV === 'production' ? false : true,
    outDir: 'dist',
    assetsDir: 'assets',
  },

  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: process.env.VITE_API_BASE || 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\\/api/, ''),
      },
    },
  },
})
"""

    def _generate_tailwind_config(self) -> str:
        """生成Tailwind配置"""
        return """export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      colors: {
        // 品牌色
        primary: '#007bff',
        success: '#28a745',
        danger: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8',
      },
      spacing: {
        safe: 'max(1rem, env(safe-area-inset-bottom))',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
"""

    def _generate_package_json(self) -> str:
        """生成package.json"""
        dependencies = {
            'vue': '^3.3.4',
            'nuxt': '^3.6.5',
            '@pinia/nuxt': '^0.4.11',
            'pinia': '^2.1.6',
            '@nuxtjs/tailwindcss': '^6.10.0',
            '@nuxt/image': '^1.0.0',
            '@vueuse/nuxt': '^10.6.1',
            '@vueuse/core': '^10.6.1',
            'axios': '^1.6.0',
            'crypto-js': '^4.1.1',
            'date-fns': '^2.30.0',
            'lodash-es': '^4.17.21',
            'tailwindcss': '^3.3.5',
            'typescript': '^5.2.2',
            '@headlessui/vue': '^1.7.15',
            '@heroicons/vue': '^2.0.18',
        }

        devDependencies = {
            '@nuxt/devtools': '^1.0.8',
            '@tailwindcss/forms': '^0.5.6',
            '@tailwindcss/typography': '^0.5.10',
            'vitest': '^0.34.6',
            '@vue/test-utils': '^2.4.1',
            '@playwright/test': '^1.39.0',
            'typescript': '^5.2.2',
            'eslint': '^8.51.0',
            'prettier': '^3.1.0',
            '@typescript-eslint/eslint-plugin': '^6.13.2',
            '@typescript-eslint/parser': '^6.13.2',
            'eslint-plugin-vue': '^9.17.0',
        }

        package = {
            'name': self.project_name,
            'version': '0.1.0',
            'description': f'支付平台 - {datetime.now().year}',
            'private': True,
            'type': 'module',
            'scripts': {
                'dev': 'nuxt dev',
                'build': 'nuxt build',
                'preview': 'nuxt preview',
                'generate': 'nuxt generate',
                'type-check': 'nuxt typecheck',
                'test': 'vitest',
                'test:e2e': 'playwright test',
                'lint': 'eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix --ignore-path .gitignore',
                'format': 'prettier --write \"src/**/*.{ts,tsx,vue,js,jsx,json,css}\"',
            },
            'dependencies': dependencies,
            'devDependencies': devDependencies,
        }

        return json.dumps(package, indent=2, ensure_ascii=False)

    def create_environment_file(self):
        """创建环境配置模板"""
        print("\n🔐 创建环境配置...")

        env_example = """# API配置
NUXT_PUBLIC_API_BASE=https://api.payment.example.com
NUXT_PUBLIC_WS_BASE=wss://api.payment.example.com

# 认证
NUXT_PUBLIC_AUTH_TOKEN_KEY=payment_auth_token

# 加密
NUXT_PUBLIC_ENCRYPTION_KEY=your-encryption-key-here
NUXT_PUBLIC_ENCRYPTION_IV=your-encryption-iv-here

# 日志和分析
NUXT_PUBLIC_ANALYTICS_ID=your-analytics-id
NUXT_PUBLIC_LOG_LEVEL=info

# 特性开关
NUXT_PUBLIC_FEATURE_KYC=true
NUXT_PUBLIC_FEATURE_UPI=true
NUXT_PUBLIC_FEATURE_RISK_CONTROL=true

# RBI合规
NUXT_PUBLIC_RBI_DATA_LOCALIZATION=IN
NUXT_PUBLIC_TRANSACTION_TIMEOUT=300000

# 本地开发
VITE_API_BASE=http://localhost:8000
VITE_HMRE_HOST=localhost
VITE_HMRE_PORT=5173
"""

        self._write_file(self.project_path / '.env.example', env_example)
        self._write_file(self.project_path / '.env.local', env_example)

    def create_compliance_checklist(self):
        """创建合规性检查清单"""
        print("\n✅ 创建合规性检查清单...")

        checklist = {
            'project_name': self.project_name,
            'created_at': self.timestamp,
            'features': self.features,
            'compliance': {
                'security': [
                    '所有API请求都使用HTTPS',
                    '没有敏感数据在localStorage或console中',
                    '有效的CSP (Content Security Policy)',
                    'X-Frame-Options设置为DENY或SAMEORIGIN',
                    'X-Content-Type-Options设置为nosniff',
                    '实施CORS白名单',
                    '依赖包无已知漏洞 (npm audit)',
                    '完整的错误边界处理',
                ],
                'performance': [
                    'Lighthouse性能评分 > 90',
                    'Bundle大小 < 500KB (gzipped)',
                    'LCP < 2.5s',
                    'FID < 100ms',
                    'CLS < 0.1',
                    '启用了Service Worker',
                    '所有关键资源预加载',
                    '图片优化和懒加载',
                ],
                'compliance': [
                    'PCI-DSS合规性审计通过',
                    'RBI数据本地化要求满足',
                    'GDPR隐私政策就位',
                    '服务条款和风险披露',
                    '审计日志系统完整',
                ],
                'testing': [
                    '单元测试覆盖率 ≥ 80%',
                    '关键流程E2E测试',
                    '无障碍测试通过',
                    '跨浏览器兼容性验证',
                ],
            },
            'next_steps': [
                '运行 npm install 安装依赖',
                '配置 .env.local 中的API端点',
                '运行 npm run dev 启动开发服务器',
                '查看 SKILL.md 了解架构详情',
                '运行 npm run type-check 进行类型检查',
                '实施项目级的安全审计',
            ],
        }

        self._write_file(
            self.project_path / 'COMPLIANCE.json',
            json.dumps(checklist, indent=2, ensure_ascii=False)
        )

    def create_readme(self):
        """创建README文件"""
        print("\n📖 创建README...")

        readme = f"""# {self.project_name.title().replace('-', ' ')}

印度支付平台前端应用 - Vue 3 + Nuxt 3

## 功能

{chr(10).join([f'- ✅ {self.SUPPORTED_FEATURES.get(f, f)}' for f in self.features])}

## 快速开始

### 前置要求

- Node.js >= 18.0
- npm >= 9.0

### 安装

```bash
npm install
```

### 开发

```bash
npm run dev
```

访问 http://localhost:3000

### 构建

```bash
npm run build
npm run preview
```

### 类型检查

```bash
npm run type-check
```

### 测试

```bash
# 单元测试
npm run test

# E2E测试
npm run test:e2e
```

### 代码规范

```bash
# 检查
npm run lint

# 格式化
npm run format
```

## 项目结构

```
{self.project_name}/
├── src/
│   ├── features/          # 功能模块
│   ├── shared/           # 共享功能
│   ├── infrastructure/   # 基础设施
│   ├── pages/            # 页面路由
│   └── app.vue
├── tests/                # 测试
├── nuxt.config.ts        # Nuxt配置
└── package.json
```

## 安全性

- PCI-DSS 合规
- 端对端加密
- 敏感数据无日志原则
- XSS/CSRF防护
- 完整的审计日志

## 性能目标

- Lighthouse评分 > 90
- LCP < 2.5s
- FID < 100ms
- Bundle大小 < 500KB (gzipped)

## 合规性

- ✅ RBI数据本地化
- ✅ NPCI UPI标准
- ✅ GDPR隐私保护
- ✅ 服务条款更新

## 文档

- [SKILL.md](../SKILL.md) - 完整开发指南
- [COMPLIANCE.json](./COMPLIANCE.json) - 合规性检查清单
- [.env.example](./.env.example) - 环境变量示例

## 贡献

请遵循项目的编码标准和安全实践。

## 许可证

MIT

---

创建于: {self.timestamp}
项目名称: {self.project_name}
启用功能: {', '.join(self.features)}
"""

        self._write_file(self.project_path / 'README.md', readme)

    def _write_file(self, file_path: Path, content: str):
        """写入文件"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {file_path}")

    def run(self) -> bool:
        """执行初始化"""
        print(f"🚀 初始化支付平台项目: {self.project_name}\n")

        if not self.validate_features():
            return False

        self.create_directory_structure()
        self.create_configuration_files()
        self.create_environment_file()
        self.create_compliance_checklist()
        self.create_readme()

        print(f"\n✨ 项目初始化完成!\n")
        print(f"📂 项目位置: {self.project_path}")
        print(f"📋 启用功能: {', '.join(self.features)}")
        print(f"\n📖 下一步:")
        print(f"   cd {self.project_name}")
        print(f"   npm install")
        print(f"   npm run dev\n")

        return True


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='支付平台项目初始化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python payment-project-init.py --name=my-payment --features=kyc,transfer,upi
  python payment-project-init.py -n payment-app -f kyc,wallet,settlement
        """
    )

    parser.add_argument(
        '-n', '--name',
        required=True,
        help='项目名称',
    )

    parser.add_argument(
        '-f', '--features',
        default='kyc,transfer,wallet',
        help=f'启用的功能 (逗号分隔), 支持: {", ".join(PaymentProjectInit.SUPPORTED_FEATURES.keys())}',
    )

    args = parser.parse_args()

    try:
        features = [f.strip() for f in args.features.split(',')]
        init = PaymentProjectInit(args.name, features)
        success = init.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
