"""
自然语言解析器
将用户的自然语言查询转换为结构化查询参数
"""

import re
import jieba
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class QueryEntity:
    """查询实体"""
    entity_type: str  # location, service, port, protocol, technology, etc.
    value: str
    raw_text: str
    confidence: float = 1.0


@dataclass
class ParsedQuery:
    """解析后的查询"""
    raw_query: str
    entities: List[QueryEntity]
    intent: str  # search, analyze, export
    constraints: Dict[str, Any]


class NLParser:
    """自然语言查询解析器"""
    
    # 地理位置关键词映射
    LOCATION_MAP = {
        # 中国省份
        '北京': 'Beijing',
        '天津': 'Tianjin',
        '河北': 'Hebei',
        '山西': 'Shanxi',
        '内蒙古': 'Inner Mongolia',
        '辽宁': 'Liaoning',
        '吉林': 'Jilin',
        '黑龙江': 'Heilongjiang',
        '上海': 'Shanghai',
        '江苏': 'Jiangsu',
        '浙江': 'Zhejiang',
        '安徽': 'Anhui',
        '福建': 'Fujian',
        '江西': 'Jiangxi',
        '山东': 'Shandong',
        '河南': 'Henan',
        '湖北': 'Hubei',
        '湖南': 'Hunan',
        '广东': 'Guangdong',
        '广西': 'Guangxi',
        '海南': 'Hainan',
        '重庆': 'Chongqing',
        '四川': 'Sichuan',
        '贵州': 'Guizhou',
        '云南': 'Yunnan',
        '西藏': 'Tibet',
        '陕西': 'Shaanxi',
        '甘肃': 'Gansu',
        '青海': 'Qinghai',
        '宁夏': 'Ningxia',
        '新疆': 'Xinjiang',
        '台湾': 'Taiwan',
        '香港': 'Hong Kong',
        '澳门': 'Macao',
        # 国家
        '中国': 'CN',
        '美国': 'US',
        '日本': 'JP',
        '韩国': 'KR',
        '英国': 'GB',
        '德国': 'DE',
        '法国': 'FR',
        '俄罗斯': 'RU',
        '印度': 'IN',
        '巴西': 'BR',
        # 区域
        '亚洲': 'Asia',
        '欧洲': 'Europe',
        '北美洲': 'North America',
        '南美洲': 'South America',
        '非洲': 'Africa',
        '大洋洲': 'Oceania',
    }
    
    # 服务类型关键词映射
    SERVICE_MAP = {
        # Web 服务器
        'nginx': 'nginx',
        'apache': 'Apache',
        'iis': 'IIS',
        'tomcat': 'Tomcat',
        'weblogic': 'WebLogic',
        'jboss': 'JBoss',
        'websphere': 'WebSphere',
        # 数据库
        'mysql': 'MySQL',
        'mariadb': 'MariaDB',
        'postgresql': 'PostgreSQL',
        'oracle': 'Oracle',
        'mongodb': 'MongoDB',
        'redis': 'Redis',
        'elasticsearch': 'Elasticsearch',
        'memcached': 'Memcached',
        # 中间件
        'php': 'PHP',
        'java': 'Java',
        'python': 'Python',
        'nodejs': 'Node.js',
        'dotnet': '.NET',
        # CMS
        'wordpress': 'WordPress',
        'drupal': 'Drupal',
        'joomla': 'Joomla',
        'dedecms': 'DedeCMS',
        'discuz': 'Discuz!',
        'phpwind': 'PHPWind',
        'phpcms': 'PHPCMS',
        'empirecms': 'EmpireCMS',
        # 框架
        'spring': 'Spring',
        'django': 'Django',
        'flask': 'Flask',
        'laravel': 'Laravel',
        'thinkphp': 'ThinkPHP',
        'struts': 'Struts',
        'jquery': 'jQuery',
        'bootstrap': 'Bootstrap',
        'vue': 'Vue.js',
        'react': 'React',
        'angular': 'Angular',
    }
    
    # 端口关键词映射
    PORT_MAP = {
        '80': '80',
        '443': '443',
        '22': '22',
        '21': '21',
        '23': '23',
        '25': '25',
        '53': '53',
        '110': '110',
        '143': '143',
        '3306': '3306',
        '3389': '3389',
        '5432': '5432',
        '6379': '6379',
        '8080': '8080',
        '8443': '8443',
        '8888': '8888',
        '9000': '9000',
        '9200': '9200',
        '27017': '27017',
    }
    
    # 协议关键词映射
    PROTOCOL_MAP = {
        'http': 'http',
        'https': 'https',
        'ssh': 'ssh',
        'ftp': 'ftp',
        'smtp': 'smtp',
        'pop3': 'pop3',
        'imap': 'imap',
        'dns': 'dns',
        'telnet': 'telnet',
        'rdp': 'rdp',
        'vnc': 'vnc',
        'redis': 'redis',
        'mongodb': 'mongodb',
        'mysql': 'mysql',
        'postgresql': 'postgresql',
        'oracle': 'oracle',
    }
    
    def __init__(self):
        """初始化解析器"""
        # 加载自定义词典（如果有）
        pass
    
    def parse(self, query: str) -> ParsedQuery:
        """
        解析自然语言查询
        
        Args:
            query: 用户的自然语言查询
            
        Returns:
            ParsedQuery: 解析后的查询对象
        """
        entities = []
        constraints = {}
        
        # 提取地理位置
        location_entities = self._extract_locations(query)
        entities.extend(location_entities)
        
        # 提取服务类型
        service_entities = self._extract_services(query)
        entities.extend(service_entities)
        
        # 提取端口信息
        port_entities = self._extract_ports(query)
        entities.extend(port_entities)
        
        # 提取协议信息
        protocol_entities = self._extract_protocols(query)
        entities.extend(protocol_entities)
        
        # 提取技术/指纹信息
        tech_entities = self._extract_technologies(query)
        entities.extend(tech_entities)
        
        # 提取数量限制
        limit = self._extract_limit(query)
        if limit:
            constraints['limit'] = limit
        
        # 提取意图
        intent = self._extract_intent(query)
        
        return ParsedQuery(
            raw_query=query,
            entities=entities,
            intent=intent,
            constraints=constraints
        )
    
    def _extract_locations(self, query: str) -> List[QueryEntity]:
        """提取地理位置实体"""
        entities = []
        
        for cn_name, en_name in self.LOCATION_MAP.items():
            if cn_name in query:
                # 判断是省份还是国家
                if cn_name in ['中国', '美国', '日本', '韩国', '英国', '德国', '法国', '俄罗斯', '印度', '巴西']:
                    entity_type = 'country'
                elif cn_name in ['亚洲', '欧洲', '北美洲', '南美洲', '非洲', '大洋洲']:
                    entity_type = 'region'
                else:
                    entity_type = 'region'  # 使用 region 表示省份
                
                entities.append(QueryEntity(
                    entity_type=entity_type,
                    value=en_name,
                    raw_text=cn_name
                ))
        
        return entities
    
    def _extract_services(self, query: str) -> List[QueryEntity]:
        """提取服务类型实体"""
        entities = []
        query_lower = query.lower()
        
        for keyword, service_name in self.SERVICE_MAP.items():
            if keyword in query_lower:
                entities.append(QueryEntity(
                    entity_type='service',
                    value=service_name,
                    raw_text=keyword
                ))
        
        return entities
    
    def _extract_ports(self, query: str) -> List[QueryEntity]:
        """提取端口信息"""
        entities = []
        
        # 匹配"xxx端口"或"port xxx"模式
        port_patterns = [
            r'(\d+)\s*端口',
            r'端口\s*(\d+)',
            r'port\s*(\d+)',
        ]
        
        for pattern in port_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                if match in self.PORT_MAP:
                    entities.append(QueryEntity(
                        entity_type='port',
                        value=match,
                        raw_text=f"{match}端口"
                    ))
        
        return entities
    
    def _extract_protocols(self, query: str) -> List[QueryEntity]:
        """提取协议信息"""
        entities = []
        query_lower = query.lower()
        
        for keyword, protocol in self.PROTOCOL_MAP.items():
            if keyword in query_lower:
                entities.append(QueryEntity(
                    entity_type='protocol',
                    value=protocol,
                    raw_text=keyword
                ))
        
        return entities
    
    def _extract_technologies(self, query: str) -> List[QueryEntity]:
        """提取技术/指纹信息"""
        entities = []
        
        # 这里可以扩展更多的技术指纹识别
        # 例如：特定组件、CMS、框架等
        
        return entities
    
    def _extract_limit(self, query: str) -> Optional[int]:
        """提取数量限制"""
        # 匹配"前xxx条"、"xxx个结果"、"limit xxx"等模式
        limit_patterns = [
            r'前\s*(\d+)\s*条',
            r'(\d+)\s*个结果',
            r'limit\s*(\d+)',
            r'最多\s*(\d+)',
        ]
        
        for pattern in limit_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_intent(self, query: str) -> str:
        """提取查询意图"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['分析', '统计', '汇总', '总结']):
            return 'analyze'
        elif any(word in query_lower for word in ['导出', '保存', '下载', '生成']):
            return 'export'
        else:
            return 'search'


# 测试代码
if __name__ == "__main__":
    parser = NLParser()
    
    test_queries = [
        "查找广东地区的 OpenClaw 服务",
        "查找中国境内运行 Nginx 的 Web 服务器，端口为 80 或 443",
        "查找暴露的 Redis 服务",
        "查找使用 WordPress 的网站，前100条结果",
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        result = parser.parse(query)
        print(f"意图: {result.intent}")
        print(f"实体: {[(e.entity_type, e.value) for e in result.entities]}")
        print(f"约束: {result.constraints}")
