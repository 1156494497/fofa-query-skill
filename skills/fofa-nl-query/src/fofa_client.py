"""
Fofa API 客户端
处理与 Fofa API 的通信
"""

import os
import base64
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from urllib.parse import urlencode


@dataclass
class FofaResult:
    """Fofa 查询结果"""
    mode: str
    page: int
    size: int
    total: int
    results: List[Dict[str, Any]]
    fields: List[str]
    query: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'mode': self.mode,
            'page': self.page,
            'size': self.size,
            'total': self.total,
            'results': self.results,
            'fields': self.fields,
            'query': self.query
        }


class FofaClient:
    """Fofa API 客户端"""
    
    BASE_URL = "https://fofa.info/api/v1"
    
    def __init__(self, email: Optional[str] = None, key: Optional[str] = None):
        """
        初始化 Fofa 客户端
        
        Args:
            email: Fofa 账号邮箱，如果不提供则从环境变量读取
            key: Fofa API Key，如果不提供则从环境变量读取
        """
        self.email = email or os.getenv('FOFA_EMAIL')
        self.key = key or os.getenv('FOFA_KEY')
        
        if not self.email or not self.key:
            raise ValueError(
                "Fofa API 认证信息不完整。请设置 FOFA_EMAIL 和 FOFA_KEY 环境变量，"
                "或在初始化时提供 email 和 key 参数。"
            )
    
    def search(self, query: str, fields: Optional[List[str]] = None, 
               page: int = 1, size: int = 100, full: bool = False) -> FofaResult:
        """
        执行 Fofa 搜索查询
        
        Args:
            query: Fofa 查询语句
            fields: 返回字段列表，默认返回所有常用字段
            page: 页码，从 1 开始
            size: 每页结果数量，最大 10000
            full: 是否获取完整数据
            
        Returns:
            FofaResult: 查询结果对象
            
        Raises:
            requests.RequestException: 网络请求异常
            ValueError: API 返回错误
        """
        # 构建请求参数
        params = {
            'email': self.email,
            'key': self.key,
            'qbase64': base64.b64encode(query.encode()).decode(),
            'page': page,
            'size': min(size, 10000),  # API 限制
            'full': str(full).lower(),
        }
        
        if fields:
            params['fields'] = ','.join(fields)
        
        # 发送请求
        url = f"{self.BASE_URL}/search/all"
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # 检查 API 错误
            if data.get('error'):
                raise ValueError(f"Fofa API 错误: {data.get('errmsg', '未知错误')}")
            
            # 解析结果
            return FofaResult(
                mode=data.get('mode', ''),
                page=data.get('page', page),
                size=data.get('size', size),
                total=int(data.get('size', 0)),  # Fofa 返回的 size 实际上是总数
                results=data.get('results', []),
                fields=data.get('fields', []),
                query=query
            )
            
        except requests.Timeout:
            raise requests.Timeout("请求超时，请检查网络连接或稍后重试")
        except requests.RequestException as e:
            raise requests.RequestException(f"网络请求失败: {str(e)}")
    
    def search_all(self, query: str, fields: Optional[List[str]] = None,
                   max_results: int = 1000, full: bool = False) -> FofaResult:
        """
        获取所有查询结果（自动分页）
        
        Args:
            query: Fofa 查询语句
            fields: 返回字段列表
            max_results: 最大结果数量
            full: 是否获取完整数据
            
        Returns:
            FofaResult: 合并后的查询结果
        """
        all_results = []
        page = 1
        page_size = min(1000, max_results)  # 每页最多 1000 条
        
        while len(all_results) < max_results:
            result = self.search(query, fields, page, page_size, full)
            
            if not result.results:
                break
            
            all_results.extend(result.results)
            
            # 检查是否还有更多结果
            if len(result.results) < page_size:
                break
            
            page += 1
            
            # 防止请求过于频繁
            import time
            time.sleep(0.5)
        
        # 截断到最大结果数
        all_results = all_results[:max_results]
        
        return FofaResult(
            mode='extended',
            page=1,
            size=len(all_results),
            total=len(all_results),
            results=all_results,
            fields=fields or [],
            query=query
        )
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        获取账号信息
        
        Returns:
            Dict: 账号信息字典
        """
        url = f"{self.BASE_URL}/info/my"
        params = {
            'email': self.email,
            'key': self.key,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('error'):
                raise ValueError(f"Fofa API 错误: {data.get('errmsg', '未知错误')}")
            
            return data
            
        except requests.RequestException as e:
            raise requests.RequestException(f"获取账号信息失败: {str(e)}")
    
    def check_auth(self) -> bool:
        """
        检查认证信息是否有效
        
        Returns:
            bool: 认证是否有效
        """
        try:
            self.get_account_info()
            return True
        except Exception:
            return False


# 测试代码
if __name__ == "__main__":
    import os
    
    # 测试需要有效的 API 密钥
    email = os.getenv('FOFA_EMAIL')
    key = os.getenv('FOFA_KEY')
    
    if not email or not key:
        print("请设置 FOFA_EMAIL 和 FOFA_KEY 环境变量进行测试")
        exit(1)
    
    client = FofaClient(email, key)
    
    # 测试账号信息
    print("测试账号信息...")
    try:
        info = client.get_account_info()
        print(f"账号信息: {info}")
    except Exception as e:
        print(f"获取账号信息失败: {e}")
    
    # 测试搜索
    print("\n测试搜索...")
    try:
        result = client.search('port="80"', size=5)
        print(f"查询结果数: {result.total}")
        print(f"返回结果数: {len(result.results)}")
        if result.results:
            print(f"第一条结果: {result.results[0]}")
    except Exception as e:
        print(f"搜索失败: {e}")
