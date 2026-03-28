"""
Fofa 自然语言查询 Skill 主程序
"""

import os
import sys
import argparse
from typing import Optional

from nl_parser import NLParser
from query_builder import QueryBuilder
from fofa_client import FofaClient, FofaResult
from export_manager import ExportManager
from summary_generator import SummaryGenerator


class FofaNLQuerySkill:
    """Fofa 自然语言查询 Skill"""
    
    def __init__(self, email: Optional[str] = None, key: Optional[str] = None):
        """
        初始化 Skill
        
        Args:
            email: Fofa 账号邮箱
            key: Fofa API Key
        """
        self.parser = NLParser()
        self.builder = QueryBuilder()
        self.client = FofaClient(email, key)
        self.exporter = ExportManager()
        self.summarizer = SummaryGenerator()
    
    def execute(self, query: str, output_format: str = 'excel', 
                max_results: int = 100, output_dir: Optional[str] = None) -> dict:
        """
        执行自然语言查询
        
        Args:
            query: 自然语言查询
            output_format: 输出格式 (excel, csv, both)
            max_results: 最大结果数量
            output_dir: 输出目录
            
        Returns:
            dict: 执行结果
        """
        print(f"正在处理查询: {query}")
        print("-" * 60)
        
        # 1. 解析自然语言
        print("步骤 1/5: 解析自然语言...")
        parsed = self.parser.parse(query)
        print(f"  识别到 {len(parsed.entities)} 个实体")
        for entity in parsed.entities:
            print(f"    - {entity.entity_type}: {entity.value}")
        
        # 2. 构建 Fofa 查询
        print("\n步骤 2/5: 构建 Fofa 查询...")
        fofa_query = self.builder.build(parsed, max_results)
        print(f"  查询语句: {fofa_query.query_string}")
        explanation = self.builder.explain_query(fofa_query)
        print(f"  查询解释: {explanation}")
        
        # 3. 调用 Fofa API
        print("\n步骤 3/5: 调用 Fofa API...")
        try:
            result = self.client.search_all(
                fofa_query.query_string,
                fields=fofa_query.fields,
                max_results=max_results
            )
            print(f"  查询成功! 共找到 {result.total} 条结果")
            print(f"  返回 {len(result.results)} 条结果")
        except Exception as e:
            print(f"  查询失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'query': fofa_query.query_string
            }
        
        # 4. 导出结果
        print("\n步骤 4/5: 导出结果...")
        if output_dir:
            self.exporter = ExportManager(output_dir)
        
        exported_files = {}
        
        if output_format in ['excel', 'both']:
            excel_path = self.exporter.export_excel(result)
            exported_files['excel'] = excel_path
            print(f"  Excel 文件: {excel_path}")
        
        if output_format in ['csv', 'both']:
            csv_path = self.exporter.export_csv(result)
            exported_files['csv'] = csv_path
            print(f"  CSV 文件: {csv_path}")
        
        # 5. 生成摘要
        print("\n步骤 5/5: 生成摘要...")
        summary = self.summarizer.generate(result, query)
        
        # 保存摘要到文件
        summary_path = os.path.join(
            self.exporter.output_dir,
            f"summary_{os.path.basename(list(exported_files.values())[0]).split('.')[0]}.txt"
        )
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        exported_files['summary'] = summary_path
        print(f"  摘要文件: {summary_path}")
        
        # 打印摘要
        print("\n" + "=" * 60)
        print(summary)
        print("=" * 60)
        
        return {
            'success': True,
            'query': fofa_query.query_string,
            'total': result.total,
            'returned': len(result.results),
            'files': exported_files,
            'summary': summary
        }
    
    def interactive_mode(self):
        """交互模式"""
        print("=" * 60)
        print("Fofa 自然语言查询 Skill")
        print("输入 'quit' 或 'exit' 退出")
        print("=" * 60)
        print()
        
        while True:
            try:
                query = input("请输入查询 (自然语言): ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("再见!")
                    break
                
                # 询问输出格式
                print("\n选择输出格式:")
                print("  1. Excel (默认)")
                print("  2. CSV")
                print("  3. Excel + CSV")
                format_choice = input("请选择 (1-3): ").strip() or '1'
                
                output_format = {
                    '1': 'excel',
                    '2': 'csv',
                    '3': 'both'
                }.get(format_choice, 'excel')
                
                # 询问最大结果数
                max_results_str = input("最大结果数 (默认 100): ").strip()
                max_results = int(max_results_str) if max_results_str.isdigit() else 100
                
                # 执行查询
                result = self.execute(query, output_format, max_results)
                
                if result['success']:
                    print("\n查询完成!")
                else:
                    print(f"\n查询失败: {result.get('error', '未知错误')}")
                
                print()
                
            except KeyboardInterrupt:
                print("\n再见!")
                break
            except Exception as e:
                print(f"错误: {str(e)}")
                print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Fofa 自然语言查询 Skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "查找广东地区的 OpenClaw 服务"
  %(prog)s "查找中国境内运行 Nginx 的 Web 服务器" --format excel --max 200
  %(prog)s --interactive
        """
    )
    
    parser.add_argument('query', nargs='?', help='自然语言查询语句')
    parser.add_argument('--format', '-f', choices=['excel', 'csv', 'both'],
                       default='excel', help='输出格式 (默认: excel)')
    parser.add_argument('--max', '-m', type=int, default=100,
                       help='最大结果数 (默认: 100)')
    parser.add_argument('--output', '-o', default='./fofa_results',
                       help='输出目录 (默认: ./fofa_results)')
    parser.add_argument('--email', '-e', default=os.getenv('FOFA_EMAIL'),
                       help='Fofa 账号邮箱 (也可通过 FOFA_EMAIL 环境变量设置)')
    parser.add_argument('--key', '-k', default=os.getenv('FOFA_KEY'),
                       help='Fofa API Key (也可通过 FOFA_KEY 环境变量设置)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='交互模式')
    
    args = parser.parse_args()
    
    # 检查认证信息
    if not args.email or not args.key:
        print("错误: 请提供 Fofa 认证信息")
        print("方式 1: 使用 --email 和 --key 参数")
        print("方式 2: 设置 FOFA_EMAIL 和 FOFA_KEY 环境变量")
        sys.exit(1)
    
    # 创建 Skill 实例
    skill = FofaNLQuerySkill(args.email, args.key)
    
    # 检查认证
    print("正在验证 API 认证...")
    if not skill.client.check_auth():
        print("错误: API 认证失败，请检查 email 和 key 是否正确")
        sys.exit(1)
    print("认证成功!")
    print()
    
    # 交互模式
    if args.interactive:
        skill.interactive_mode()
    elif args.query:
        # 执行单次查询
        result = skill.execute(args.query, args.format, args.max, args.output)
        
        if not result['success']:
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
