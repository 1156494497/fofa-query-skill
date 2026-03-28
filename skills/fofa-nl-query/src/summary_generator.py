"""
摘要生成器
生成查询结果的文本摘要报告
"""

from typing import Dict, List, Any, Optional
from collections import Counter
from datetime import datetime

from .fofa_client import FofaResult


class SummaryGenerator:
    """摘要生成器"""
    
    def __init__(self):
        """初始化摘要生成器"""
        pass
    
    def generate(self, result: FofaResult, natural_query: str = "") -> str:
        """
        生成查询结果摘要
        
        Args:
            result: Fofa 查询结果
            natural_query: 原始自然语言查询
            
        Returns:
            str: 格式化的摘要文本
        """
        lines = []
        
        # 标题
        lines.append("=" * 60)
        lines.append("Fofa 查询结果摘要报告")
        lines.append("=" * 60)
        lines.append("")
        
        # 查询信息
        lines.append("【查询信息】")
        if natural_query:
            lines.append(f"原始查询: {natural_query}")
        lines.append(f"Fofa 语句: {result.query}")
        lines.append(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 统计概览
        lines.append("【统计概览】")
        lines.append(f"总结果数: {result.total}")
        lines.append(f"返回数量: {len(result.results)}")
        if result.total > 0:
            coverage = len(result.results) / result.total * 100
            lines.append(f"覆盖率: {coverage:.1f}%")
        lines.append("")
        
        if not result.results:
            lines.append("【数据详情】")
            lines.append("未找到匹配结果")
            return "\n".join(lines)
        
        # 地理分布
        lines.append("【地理分布】")
        lines.extend(self._generate_geo_stats(result))
        lines.append("")
        
        # 服务分布
        lines.append("【服务分布】")
        lines.extend(self._generate_service_stats(result))
        lines.append("")
        
        # 端口分布
        lines.append("【端口分布】")
        lines.extend(self._generate_port_stats(result))
        lines.append("")
        
        # 协议分布
        lines.append("【协议分布】")
        lines.extend(self._generate_protocol_stats(result))
        lines.append("")
        
        # Top 资产
        lines.append("【Top 资产】")
        lines.extend(self._generate_top_assets(result))
        lines.append("")
        
        # 安全提示
        lines.append("【安全提示】")
        lines.extend(self._generate_security_tips(result))
        
        return "\n".join(lines)
    
    def _generate_geo_stats(self, result: FofaResult) -> List[str]:
        """生成地理分布统计"""
        lines = []
        
        # 国家分布
        if 'country' in result.fields:
            countries = [item.get('country', '未知') for item in result.results if item.get('country')]
            if countries:
                country_counts = Counter(countries)
                lines.append("  国家分布:")
                for country, count in country_counts.most_common(5):
                    percentage = count / len(result.results) * 100
                    lines.append(f"    - {country}: {count} ({percentage:.1f}%)")
        
        # 省份分布
        if 'region' in result.fields:
            regions = [item.get('region', '未知') for item in result.results if item.get('region')]
            if regions:
                region_counts = Counter(regions)
                lines.append("  省份/地区分布:")
                for region, count in region_counts.most_common(5):
                    percentage = count / len(result.results) * 100
                    lines.append(f"    - {region}: {count} ({percentage:.1f}%)")
        
        # 城市分布
        if 'city' in result.fields:
            cities = [item.get('city', '未知') for item in result.results if item.get('city')]
            if cities:
                city_counts = Counter(cities)
                lines.append("  城市分布:")
                for city, count in city_counts.most_common(5):
                    percentage = count / len(result.results) * 100
                    lines.append(f"    - {city}: {count} ({percentage:.1f}%)")
        
        if len(lines) == 0:
            lines.append("  无地理分布数据")
        
        return lines
    
    def _generate_service_stats(self, result: FofaResult) -> List[str]:
        """生成服务分布统计"""
        lines = []
        
        # 服务器类型
        if 'server' in result.fields:
            servers = [item.get('server', '未知') for item in result.results if item.get('server')]
            if servers:
                server_counts = Counter(servers)
                lines.append("  服务器类型:")
                for server, count in server_counts.most_common(5):
                    percentage = count / len(result.results) * 100
                    lines.append(f"    - {server}: {count} ({percentage:.1f}%)")
        
        # 应用/服务
        if 'app' in result.fields:
            apps = [item.get('app', '未知') for item in result.results if item.get('app')]
            if apps:
                app_counts = Counter(apps)
                lines.append("  应用类型:")
                for app, count in app_counts.most_common(5):
                    percentage = count / len(result.results) * 100
                    lines.append(f"    - {app}: {count} ({percentage:.1f}%)")
        
        if len(lines) == 0:
            lines.append("  无服务分布数据")
        
        return lines
    
    def _generate_port_stats(self, result: FofaResult) -> List[str]:
        """生成端口分布统计"""
        lines = []
        
        if 'port' in result.fields:
            ports = [item.get('port', '未知') for item in result.results if item.get('port')]
            if ports:
                port_counts = Counter(ports)
                lines.append("  端口分布:")
                for port, count in port_counts.most_common(10):
                    percentage = count / len(result.results) * 100
                    lines.append(f"    - {port}: {count} ({percentage:.1f}%)")
            else:
                lines.append("  无端口分布数据")
        else:
            lines.append("  无端口字段数据")
        
        return lines
    
    def _generate_protocol_stats(self, result: FofaResult) -> List[str]:
        """生成协议分布统计"""
        lines = []
        
        if 'protocol' in result.fields:
            protocols = [item.get('protocol', '未知') for item in result.results if item.get('protocol')]
            if protocols:
                protocol_counts = Counter(protocols)
                lines.append("  协议分布:")
                for protocol, count in protocol_counts.most_common(5):
                    percentage = count / len(result.results) * 100
                    lines.append(f"    - {protocol}: {count} ({percentage:.1f}%)")
            else:
                lines.append("  无协议分布数据")
        else:
            lines.append("  无协议字段数据")
        
        return lines
    
    def _generate_top_assets(self, result: FofaResult) -> List[str]:
        """生成 Top 资产列表"""
        lines = []
        
        if not result.results:
            lines.append("  无资产数据")
            return lines
        
        lines.append("  Top 10 资产:")
        lines.append("")
        
        for i, item in enumerate(result.results[:10], 1):
            lines.append(f"  [{i}] {self._format_asset(item)}")
        
        return lines
    
    def _format_asset(self, item: Dict[str, Any]) -> str:
        """格式化资产信息"""
        parts = []
        
        # IP 和端口
        ip = item.get('ip', '')
        port = item.get('port', '')
        if ip and port:
            parts.append(f"{ip}:{port}")
        elif ip:
            parts.append(ip)
        
        # 标题
        title = item.get('title', '')
        if title:
            parts.append(f"[{title}]")
        
        # 位置
        location_parts = []
        if item.get('country'):
            location_parts.append(item['country'])
        if item.get('region'):
            location_parts.append(item['region'])
        if item.get('city'):
            location_parts.append(item['city'])
        if location_parts:
            parts.append(f"({', '.join(location_parts)})")
        
        # 服务器
        server = item.get('server', '')
        if server:
            parts.append(f"Server: {server}")
        
        return " | ".join(parts) if parts else "未知资产"
    
    def _generate_security_tips(self, result: FofaResult) -> List[str]:
        """生成安全提示"""
        lines = []
        
        # 检查是否有常见的高危端口
        high_risk_ports = {'22': 'SSH', '23': 'Telnet', '3389': 'RDP', 
                          '3306': 'MySQL', '1433': 'MSSQL', '6379': 'Redis',
                          '27017': 'MongoDB', '9200': 'Elasticsearch'}
        
        if 'port' in result.fields:
            found_ports = set()
            for item in result.results:
                port = item.get('port', '')
                if port in high_risk_ports:
                    found_ports.add(port)
            
            if found_ports:
                lines.append("  发现以下可能的高危端口暴露:")
                for port in sorted(found_ports):
                    service = high_risk_ports.get(port, '未知服务')
                    lines.append(f"    - {port} ({service})")
                lines.append("  建议: 请确保这些服务已配置适当的安全防护措施")
        
        # 检查 HTTP 服务
        if 'protocol' in result.fields:
            http_count = sum(1 for item in result.results 
                           if item.get('protocol', '').lower() in ['http', 'https'])
            if http_count > 0:
                lines.append(f"  发现 {http_count} 个 Web 服务")
                lines.append("  建议: 请检查 Web 服务是否存在已知漏洞")
        
        if len(lines) == 0:
            lines.append("  未发现明显的安全风险")
        
        return lines
    
    def generate_markdown(self, result: FofaResult, natural_query: str = "") -> str:
        """
        生成 Markdown 格式的摘要
        
        Args:
            result: Fofa 查询结果
            natural_query: 原始自然语言查询
            
        Returns:
            str: Markdown 格式的摘要
        """
        lines = []
        
        # 标题
        lines.append("# Fofa 查询结果摘要报告")
        lines.append("")
        
        # 查询信息
        lines.append("## 查询信息")
        if natural_query:
            lines.append(f"- **原始查询**: {natural_query}")
        lines.append(f"- **Fofa 语句**: `{result.query}`")
        lines.append(f"- **查询时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # 统计概览
        lines.append("## 统计概览")
        lines.append(f"- **总结果数**: {result.total}")
        lines.append(f"- **返回数量**: {len(result.results)}")
        if result.total > 0:
            coverage = len(result.results) / result.total * 100
            lines.append(f"- **覆盖率**: {coverage:.1f}%")
        lines.append("")
        
        if not result.results:
            lines.append("## 数据详情")
            lines.append("未找到匹配结果")
            return "\n".join(lines)
        
        # 地理分布
        lines.append("## 地理分布")
        lines.extend(self._generate_markdown_geo_stats(result))
        lines.append("")
        
        # 服务分布
        lines.append("## 服务分布")
        lines.extend(self._generate_markdown_service_stats(result))
        lines.append("")
        
        # Top 资产
        lines.append("## Top 10 资产")
        lines.append("")
        lines.append("| # | 资产信息 |")
        lines.append("|---|----------|")
        for i, item in enumerate(result.results[:10], 1):
            asset_info = self._format_asset(item)
            lines.append(f"| {i} | {asset_info} |")
        lines.append("")
        
        # 安全提示
        lines.append("## 安全提示")
        lines.extend(self._generate_security_tips(result))
        
        return "\n".join(lines)
    
    def _generate_markdown_geo_stats(self, result: FofaResult) -> List[str]:
        """生成 Markdown 格式的地理分布统计"""
        lines = []
        
        if 'country' in result.fields:
            countries = [item.get('country', '未知') for item in result.results if item.get('country')]
            if countries:
                country_counts = Counter(countries)
                lines.append("### 国家分布")
                lines.append("")
                lines.append("| 国家 | 数量 | 占比 |")
                lines.append("|------|------|------|")
                for country, count in country_counts.most_common(5):
                    percentage = count / len(result.results) * 100
                    lines.append(f"| {country} | {count} | {percentage:.1f}% |")
                lines.append("")
        
        return lines
    
    def _generate_markdown_service_stats(self, result: FofaResult) -> List[str]:
        """生成 Markdown 格式的服务分布统计"""
        lines = []
        
        if 'server' in result.fields:
            servers = [item.get('server', '未知') for item in result.results if item.get('server')]
            if servers:
                server_counts = Counter(servers)
                lines.append("### 服务器类型")
                lines.append("")
                lines.append("| 服务器 | 数量 | 占比 |")
                lines.append("|--------|------|------|")
                for server, count in server_counts.most_common(5):
                    percentage = count / len(result.results) * 100
                    lines.append(f"| {server} | {count} | {percentage:.1f}% |")
                lines.append("")
        
        return lines


# 测试代码
if __name__ == "__main__":
    from fofa_client import FofaResult
    
    # 创建测试数据
    test_result = FofaResult(
        mode='normal',
        page=1,
        size=5,
        total=100,
        results=[
            {
                'ip': '192.168.1.1',
                'port': '80',
                'protocol': 'http',
                'country': 'CN',
                'region': 'Beijing',
                'city': 'Beijing',
                'title': 'Test Server',
                'server': 'nginx',
            },
            {
                'ip': '192.168.1.2',
                'port': '443',
                'protocol': 'https',
                'country': 'CN',
                'region': 'Shanghai',
                'city': 'Shanghai',
                'title': 'Secure Server',
                'server': 'apache',
            },
            {
                'ip': '192.168.1.3',
                'port': '3306',
                'protocol': 'mysql',
                'country': 'CN',
                'region': 'Guangdong',
                'city': 'Guangzhou',
                'title': '',
                'server': '',
            },
        ],
        fields=['ip', 'port', 'protocol', 'country', 'region', 'city', 'title', 'server'],
        query='port="80" || port="443" || port="3306"'
    )
    
    # 测试生成摘要
    generator = SummaryGenerator()
    
    print("测试生成文本摘要...")
    summary = generator.generate(test_result, "查找中国境内的 Web 和数据库服务")
    print(summary)
    
    print("\n" + "="*60 + "\n")
    
    print("测试生成 Markdown 摘要...")
    markdown_summary = generator.generate_markdown(test_result, "查找中国境内的 Web 和数据库服务")
    print(markdown_summary)
