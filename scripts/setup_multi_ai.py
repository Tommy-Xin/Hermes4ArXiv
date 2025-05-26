#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai>=1.0.0",
#     "anthropic>=0.7.0",
#     "google-generativeai>=0.3.0",
#     "requests>=2.31.0",
# ]
# ///
"""
多 AI API 支持设置脚本
自动配置和测试多个 AI 提供商
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class AIProviderTester:
    """AI 提供商测试器"""
    
    def __init__(self):
        self.providers = {
            'deepseek': {
                'api_key_env': 'DEEPSEEK_API_KEY',
                'base_url': 'https://api.deepseek.com/v1',
                'model': 'deepseek-chat',
                'test_prompt': '请简单介绍一下深度学习。'
            },
            'openai': {
                'api_key_env': 'OPENAI_API_KEY',
                'base_url': 'https://api.openai.com/v1',
                'model': 'gpt-3.5-turbo',
                'test_prompt': 'Briefly explain deep learning.'
            },
            'claude': {
                'api_key_env': 'CLAUDE_API_KEY',
                'base_url': 'https://api.anthropic.com',
                'model': 'claude-3-haiku-20240307',
                'test_prompt': 'Briefly explain deep learning.'
            },
            'gemini': {
                'api_key_env': 'GEMINI_API_KEY',
                'base_url': 'https://generativelanguage.googleapis.com',
                'model': 'gemini-pro',
                'test_prompt': 'Briefly explain deep learning.'
            }
        }
        
        self.test_results = {}
    
    def check_api_keys(self) -> Dict[str, bool]:
        """检查 API 密钥是否配置"""
        results = {}
        
        print("🔑 检查 API 密钥配置...")
        for provider, config in self.providers.items():
            api_key = os.getenv(config['api_key_env'])
            has_key = bool(api_key and len(api_key) > 10)
            results[provider] = has_key
            
            status = "✅" if has_key else "❌"
            print(f"   {provider}: {status} {config['api_key_env']}")
        
        return results
    
    async def test_deepseek(self) -> bool:
        """测试 DeepSeek API"""
        try:
            import requests
            
            api_key = os.getenv('DEEPSEEK_API_KEY')
            if not api_key:
                return False
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'user', 'content': '请简单介绍一下深度学习。'}
                ],
                'max_tokens': 100
            }
            
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"   DeepSeek 测试失败: {e}")
            return False
    
    async def test_openai(self) -> bool:
        """测试 OpenAI API"""
        try:
            import openai
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                return False
            
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Briefly explain deep learning."}
                ],
                max_tokens=100
            )
            
            return bool(response.choices[0].message.content)
            
        except Exception as e:
            print(f"   OpenAI 测试失败: {e}")
            return False
    
    async def test_claude(self) -> bool:
        """测试 Claude API"""
        try:
            import anthropic
            
            api_key = os.getenv('CLAUDE_API_KEY')
            if not api_key:
                return False
            
            client = anthropic.Anthropic(api_key=api_key)
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=100,
                messages=[
                    {"role": "user", "content": "Briefly explain deep learning."}
                ]
            )
            
            return bool(response.content[0].text)
            
        except Exception as e:
            print(f"   Claude 测试失败: {e}")
            return False
    
    async def test_gemini(self) -> bool:
        """测试 Gemini API"""
        try:
            import google.generativeai as genai
            
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                return False
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content("Briefly explain deep learning.")
            
            return bool(response.text)
            
        except Exception as e:
            print(f"   Gemini 测试失败: {e}")
            return False
    
    async def test_all_providers(self) -> Dict[str, bool]:
        """测试所有 AI 提供商"""
        print("\n🧪 测试 AI 提供商连接...")
        
        test_functions = {
            'deepseek': self.test_deepseek,
            'openai': self.test_openai,
            'claude': self.test_claude,
            'gemini': self.test_gemini
        }
        
        results = {}
        
        for provider, test_func in test_functions.items():
            print(f"   测试 {provider}...")
            try:
                result = await test_func()
                results[provider] = result
                status = "✅ 连接成功" if result else "❌ 连接失败"
                print(f"   {provider}: {status}")
            except Exception as e:
                results[provider] = False
                print(f"   {provider}: ❌ 测试异常 - {e}")
        
        return results
    
    def generate_config_template(self) -> str:
        """生成配置模板"""
        template = """# AI 提供商配置模板
# 将此内容添加到 .env 文件中

# DeepSeek API (推荐，性价比高)
DEEPSEEK_API_KEY=sk-your-deepseek-api-key

# OpenAI API (可选)
OPENAI_API_KEY=sk-your-openai-api-key

# Claude API (可选)
CLAUDE_API_KEY=sk-ant-your-claude-api-key

# Gemini API (可选)
GEMINI_API_KEY=your-gemini-api-key

# AI 分析策略配置
ANALYSIS_STRATEGY=fallback  # fallback, parallel, consensus
AI_FALLBACK_ORDER=deepseek,openai,claude,gemini
"""
        return template
    
    def create_multi_ai_analyzer(self):
        """创建多 AI 分析器示例代码"""
        code = '''# src/ai_analyzer_v2.py - 多 AI 分析器实现
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    CLAUDE = "claude"
    GEMINI = "gemini"

class BaseAIAnalyzer(ABC):
    """AI 分析器基类"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.is_available_flag = bool(api_key)
    
    @abstractmethod
    async def analyze_paper(self, paper) -> Dict:
        """分析论文"""
        pass
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.is_available_flag
    
    @abstractmethod
    def get_provider_info(self) -> Dict:
        """获取提供商信息"""
        pass

class MultiAIAnalyzer:
    """多 AI 分析器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.analyzers = {}
        self.fallback_order = self._parse_fallback_order()
        self._initialize_analyzers()
    
    def _parse_fallback_order(self) -> List[AIProvider]:
        """解析降级顺序"""
        order_str = self.config.get('AI_FALLBACK_ORDER', 'deepseek,openai,claude,gemini')
        order = []
        for provider_name in order_str.split(','):
            try:
                provider = AIProvider(provider_name.strip())
                order.append(provider)
            except ValueError:
                logger.warning(f"未知的 AI 提供商: {provider_name}")
        return order
    
    def _initialize_analyzers(self):
        """初始化分析器"""
        # 这里会根据配置初始化各个分析器
        # 具体实现会在后续添加
        pass
    
    async def analyze_with_fallback(self, paper) -> Dict:
        """使用降级策略分析论文"""
        last_error = None
        
        for provider in self.fallback_order:
            analyzer = self.analyzers.get(provider)
            if not analyzer or not analyzer.is_available():
                continue
            
            try:
                logger.info(f"使用 {provider.value} 分析论文: {paper.title[:50]}...")
                result = await analyzer.analyze_paper(paper)
                result['provider'] = provider.value
                return result
                
            except Exception as e:
                last_error = e
                logger.warning(f"{provider.value} 分析失败: {e}")
                continue
        
        raise Exception(f"所有 AI 提供商都不可用。最后错误: {last_error}")
    
    async def analyze_with_consensus(self, paper, min_consensus: int = 2) -> Dict:
        """使用共识策略分析论文"""
        results = []
        
        # 并行调用多个 AI
        tasks = []
        for provider in self.fallback_order[:3]:  # 最多使用前3个
            analyzer = self.analyzers.get(provider)
            if analyzer and analyzer.is_available():
                task = analyzer.analyze_paper(paper)
                tasks.append((provider, task))
        
        # 等待结果
        for provider, task in tasks:
            try:
                result = await task
                result['provider'] = provider.value
                results.append(result)
            except Exception as e:
                logger.warning(f"{provider.value} 分析失败: {e}")
        
        if len(results) < min_consensus:
            raise Exception(f"无法达成共识，只有 {len(results)} 个结果")
        
        # 合并结果（简化版本）
        return self._merge_results(results)
    
    def _merge_results(self, results: List[Dict]) -> Dict:
        """合并多个分析结果"""
        # 这里实现结果合并逻辑
        # 可以基于投票、平均分等策略
        merged = {
            'providers': [r['provider'] for r in results],
            'consensus_count': len(results),
            'analysis': {}
        }
        
        # 简单合并策略：取第一个结果作为主要结果
        if results:
            merged['analysis'] = results[0].get('analysis', {})
        
        return merged
'''
        
        # 写入文件
        output_file = Path(__file__).parent.parent / "src" / "ai_analyzer_v2.py"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"✅ 创建多 AI 分析器: {output_file}")
    
    def generate_usage_examples(self) -> str:
        """生成使用示例"""
        examples = """
# 使用示例

## 1. 基本配置
```bash
# 设置环境变量
export DEEPSEEK_API_KEY="sk-your-key"
export OPENAI_API_KEY="sk-your-key"
export ANALYSIS_STRATEGY="fallback"
```

## 2. 测试 AI 连接
```bash
# 运行测试脚本
uv run scripts/setup_multi_ai.py
```

## 3. 在代码中使用
```python
from ai_analyzer_v2 import MultiAIAnalyzer
from config import Config

# 初始化多 AI 分析器
config = Config()
analyzer = MultiAIAnalyzer(config.__dict__)

# 分析论文
result = await analyzer.analyze_with_fallback(paper)
print(f"分析结果来自: {result['provider']}")
```

## 4. 不同策略
- **fallback**: 按顺序尝试，第一个成功的结果
- **parallel**: 并行调用多个 AI
- **consensus**: 需要多个 AI 达成共识
"""
        return examples


async def main():
    """主函数"""
    print("🚀 多 AI API 支持设置向导")
    print("=" * 50)
    
    tester = AIProviderTester()
    
    # 1. 检查 API 密钥
    key_results = tester.check_api_keys()
    available_count = sum(key_results.values())
    
    print(f"\n📊 API 密钥状态: {available_count}/{len(key_results)} 个已配置")
    
    if available_count == 0:
        print("\n⚠️  没有配置任何 API 密钥！")
        print("\n📝 配置模板:")
        print(tester.generate_config_template())
        return
    
    # 2. 测试 API 连接
    test_results = await tester.test_all_providers()
    working_count = sum(test_results.values())
    
    print(f"\n📊 API 连接状态: {working_count}/{len(test_results)} 个可用")
    
    # 3. 生成配置建议
    print("\n💡 配置建议:")
    
    working_providers = [p for p, working in test_results.items() if working]
    if working_providers:
        print(f"   ✅ 可用的 AI 提供商: {', '.join(working_providers)}")
        print(f"   🔄 建议降级顺序: {','.join(working_providers)}")
        
        # 更新环境变量建议
        print(f"\n   建议在 .env 中设置:")
        print(f"   AI_FALLBACK_ORDER={','.join(working_providers)}")
        
        if len(working_providers) >= 2:
            print(f"   ANALYSIS_STRATEGY=consensus  # 使用共识策略")
        else:
            print(f"   ANALYSIS_STRATEGY=fallback   # 使用降级策略")
    
    # 4. 创建示例代码
    print("\n🔧 创建多 AI 分析器代码...")
    tester.create_multi_ai_analyzer()
    
    # 5. 显示使用示例
    print("\n📖 使用示例:")
    print(tester.generate_usage_examples())
    
    print("\n🎉 多 AI API 支持设置完成！")
    print("\n下一步:")
    print("1. 根据建议配置环境变量")
    print("2. 更新 src/config.py 添加多 AI 配置")
    print("3. 在 src/main.py 中集成新的分析器")
    print("4. 运行测试验证功能")


if __name__ == "__main__":
    asyncio.run(main()) 