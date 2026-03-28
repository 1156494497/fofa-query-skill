"""
Fofa 查询构建器
将解析后的查询实体转换为 Fofa 查询语法
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from .nl_parser import ParsedQuery, QueryEntity


@dataclass
class FofaQuery:
    """Fofa 查询对象"""
    query_string: str
    fields: List[str]
    page: int
    size: int
    full: bool
    
    def to_api_params(self) -> Dict[str, Any]:
        """转换为 API 请求参数"""
        return {
            'qbase64': self._encode_query(),
            'fields': ','.join(self.fields),
            'page': self.page,
            'size': self.size,
            'full': str(self.full).lower(),
        }
    
    def _encode_query(self) -> str:
        """Base64 编码查询语句"""
        import base64
        return base64.b64encode(self.query_string.encode()).decode()


class QueryBuilder:
    """Fofa 查询构建器"""
    
    # 默认查询字段
    DEFAULT_FIELDS = [
        'ip', 'port', 'protocol', 'country', 'region', 'city',
        'longitude', 'latitude', 'as_number', 'as_organization',
        'host', 'domain', 'os', 'server', 'icp', 'title', 'jarm',
        'header', 'banner', 'cert', 'base_protocol'
    ]
    
    def __init__(self):
        """初始化查询构建器"""
        pass
    
    def build(self, parsed_query: ParsedQuery, max_results: int = 100) -> FofaQuery:
        """
        构建 Fofa 查询
        
        Args:
            parsed_query: 解析后的查询对象
            max_results: 最大结果数量
            
        Returns:
            FofaQuery: Fofa 查询对象
        """
        conditions = []
        
        # 处理地理位置
        location_conditions = self._build_location_conditions(parsed_query.entities)
        if location_conditions:
            conditions.extend(location_conditions)
        
        # 处理服务类型
        service_conditions = self._build_service_conditions(parsed_query.entities)
        if service_conditions:
            conditions.extend(service_conditions)
        
        # 处理端口
        port_conditions = self._build_port_conditions(parsed_query.entities)
        if port_conditions:
            conditions.extend(port_conditions)
        
        # 处理协议
        protocol_conditions = self._build_protocol_conditions(parsed_query.entities)
        if protocol_conditions:
            conditions.extend(protocol_conditions)
        
        # 组合查询条件
        if conditions:
            query_string = ' && '.join(conditions)
        else:
            # 如果没有识别到任何条件，使用原始查询作为全文搜索
            query_string = parsed_query.raw_query
        
        # 获取限制数量
        limit = parsed_query.constraints.get('limit', max_results)
        
        return FofaQuery(
            query_string=query_string,
            fields=self.DEFAULT_FIELDS,
            page=1,
            size=min(limit, 10000),  # Fofa API 限制
            full=False
        )
    
    def _build_location_conditions(self, entities: List[QueryEntity]) -> List[str]:
        """构建地理位置查询条件"""
        conditions = []
        
        countries = [e for e in entities if e.entity_type == 'country']
        regions = [e for e in entities if e.entity_type == 'region']
        
        # 国家条件
        for country in countries:
            conditions.append(f'country="{country.value}"')
        
        # 省份/地区条件
        for region in regions:
            conditions.append(f'region="{region.value}"')
        
        return conditions
    
    def _build_service_conditions(self, entities: List[QueryEntity]) -> List[str]:
        """构建服务类型查询条件"""
        conditions = []
        
        services = [e for e in entities if e.entity_type == 'service']
        
        for service in services:
            # 根据服务类型选择合适的字段
            service_value = service.value.lower()
            
            # Web 服务器和中间件通常使用 server 字段
            if service_value in ['nginx', 'apache', 'iis', 'tomcat', 'weblogic', 'jboss', 'websphere']:
                conditions.append(f'server="{service.value}"')
            # 数据库使用 app 字段
            elif service_value in ['mysql', 'mariadb', 'postgresql', 'oracle', 'mongodb', 'redis', 'elasticsearch', 'memcached']:
                conditions.append(f'app="{service.value}"')
            # CMS 和框架使用 app 字段
            elif service_value in ['wordpress', 'drupal', 'joomla', 'dedecms', 'discuz', 'phpwind', 
                                  'phpcms', 'empirecms', 'spring', 'django', 'flask', 'laravel', 
                                  'thinkphp', 'struts']:
                conditions.append(f'app="{service.value}"')
            # 其他使用 app 字段
            else:
                conditions.append(f'app="{service.value}"')
        
        return conditions
    
    def _build_port_conditions(self, entities: List[QueryEntity]) -> List[str]:
        """构建端口查询条件"""
        conditions = []
        
        ports = [e for e in entities if e.entity_type == 'port']
        
        if len(ports) == 1:
            conditions.append(f'port="{ports[0].value}"')
        elif len(ports) > 1:
            # 多个端口使用 OR 连接
            port_conditions = [f'port="{p.value}"' for p in ports]
            conditions.append(f'({" || ".join(port_conditions)})')
        
        return conditions
    
    def _build_protocol_conditions(self, entities: List[QueryEntity]) -> List[str]:
        """构建协议查询条件"""
        conditions = []
        
        protocols = [e for e in entities if e.entity_type == 'protocol']
        
        for protocol in protocols:
            conditions.append(f'protocol="{protocol.value}"')
        
        return conditions
    
    def explain_query(self, fofa_query: FofaQuery) -> str:
        """
        解释查询语句的含义
        
        Args:
            fofa_query: Fofa 查询对象
            
        Returns:
            str: 查询语句的自然语言解释
        """
        query = fofa_query.query_string
        explanations = []
        
        # 解析各个条件
        if 'country=' in query:
            country = self._extract_value(query, 'country')
            explanations.append(f"国家/地区: {country}")
        
        if 'region=' in query:
            region = self._extract_value(query, 'region')
            explanations.append(f"省份/区域: {region}")
        
        if 'city=' in query:
            city = self._extract_value(query, 'city')
            explanations.append(f"城市: {city}")
        
        if 'port=' in query:
            port = self._extract_value(query, 'port')
            explanations.append(f"端口: {port}")
        
        if 'protocol=' in query:
            protocol = self._extract_value(query, 'protocol')
            explanations.append(f"协议: {protocol}")
        
        if 'server=' in query:
            server = self._extract_value(query, 'server')
            explanations.append(f"服务器: {server}")
        
        if 'app=' in query:
            app = self._extract_value(query, 'app')
            explanations.append(f"应用/服务: {app}")
        
        if 'title=' in query:
            title = self._extract_value(query, 'title')
            explanations.append(f"页面标题包含: {title}")
        
        if 'body=' in query:
            body = self._extract_value(query, 'body')
            explanations.append(f"页面内容包含: {body}")
        
        if 'header=' in query:
            header = self._extract_value(query, 'header')
            explanations.append(f"HTTP 头包含: {header}")
        
        if 'banner=' in query:
            banner = self._extract_value(query, 'banner')
            explanations.append(f"Banner 包含: {banner}")
        
        if not explanations:
            return f"全文搜索: {query}"
        
        return "; ".join(explanations)
    
    def _extract_value(self, query: str, field: str) -> str:
        """从查询语句中提取字段值"""
        import re
        pattern = rf'{field}="([^"]+)"'
        match = re.search(pattern, query)
        if match:
            return match.group(1)
        return "未知"


# 测试代码
if __name__ == "__main__":
    from nl_parser import NLParser
    
    parser = NLParser()
    builder = QueryBuilder()
    
    test_queries = [
        "查找广东地区的 OpenClaw 服务",
        "查找中国境内运行 Nginx 的 Web 服务器，端口为 80 或 443",
        "查找暴露的 Redis 服务",
        "查找使用 WordPress 的网站，前100条结果",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"原始查询: {query}")
        
        parsed = parser.parse(query)
        fofa_query = builder.build(parsed)
        
        print(f"Fofa 查询语句: {fofa_query.query_string}")
        print(f"解释: {builder.explain_query(fofa_query)}")
        print(f"API 参数: {fofa_query.to_api_params()}")
