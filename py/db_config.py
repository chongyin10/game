import os
from typing import Any, Optional
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.extensions import connection, cursor

# 加载环境变量
load_dotenv()

class Database:
    def __init__(self) -> None:
        self.conn: Optional[connection] = None
        self.cursor: Optional[cursor] = None
        
    def connect(self):
        """连接到PostgreSQL数据库"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("成功连接到PostgreSQL数据库")
            return True
        except Exception as e:
            print(f"连接数据库失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("数据库连接已关闭")
    
    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None) -> Optional[list[RealDictRow]]:
        """执行查询语句"""
        # 诊断日志：检查连接状态
        print(f"[DEBUG] execute_query 被调用")
        print(f"[DEBUG] conn 状态: {self.conn is not None}")
        print(f"[DEBUG] cursor 状态: {self.cursor is not None}")
        
        if self.conn:
            print(f"[DEBUG] conn closed: {self.conn.closed}")
        
        try:
            if not self.conn or self.conn.closed:
                print("[DEBUG] 警告: 数据库连接未建立或已关闭")
                return None
                
            if not self.cursor:
                print("[DEBUG] 警告: cursor 为 None")
                return None
            
            print(f"[DEBUG] 执行查询: {query[:100]}...")
            print(f"[DEBUG] 参数: {params}")
            
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            
            print(f"[DEBUG] 查询成功，返回 {len(result)} 条记录")
            return result
            
        except psycopg2.InterfaceError as e:
            print(f"[DEBUG] InterfaceError - 数据库接口错误: {e}")
            return None
        except psycopg2.OperationalError as e:
            print(f"[DEBUG] OperationalError - 数据库操作错误: {e}")
            return None
        except psycopg2.ProgrammingError as e:
            print(f"[DEBUG] ProgrammingError - SQL语法错误: {e}")
            return None
        except Exception as e:
            print(f"[DEBUG] 未知异常类型 {type(e).__name__}: {e}")
            return None
    
    def execute_update(self, query: str, params: Optional[tuple[Any, ...]] = None) -> bool:
        """执行更新/插入/删除语句"""
        # 诊断日志
        print(f"[DEBUG] execute_update 被调用")
        print(f"[DEBUG] conn 状态: {self.conn is not None}")
        print(f"[DEBUG] cursor 状态: {self.cursor is not None}")
        
        if self.conn:
            print(f"[DEBUG] conn closed: {self.conn.closed}")
        
        if not self.conn or self.conn.closed:
            print("[DEBUG] 错误: 数据库连接未建立或已关闭")
            return False
            
        if not self.cursor:
            print("[DEBUG] 错误: cursor 为 None")
            return False
        
        try:
            print(f"[DEBUG] 执行更新: {query[:100]}...")
            print(f"[DEBUG] 参数: {params}")
            
            self.cursor.execute(query, params)
            self.conn.commit()
            print("[DEBUG] 更新执行成功")
            return True
        except psycopg2.InterfaceError as e:
            print(f"[DEBUG] InterfaceError - 数据库接口错误: {e}")
            if self.conn:
                self.conn.rollback()
        except psycopg2.OperationalError as e:
            print(f"[DEBUG] OperationalError - 数据库操作错误: {e}")
            if self.conn:
                self.conn.rollback()
        except psycopg2.ProgrammingError as e:
            print(f"[DEBUG] ProgrammingError - SQL语法错误: {e}")
            if self.conn:
                self.conn.rollback()
        except Exception as e:
            print(f"[DEBUG] 未知异常类型 {type(e).__name__}: {e}")
            if self.conn:
                self.conn.rollback()
        return False
    
    def __enter__(self) -> "Database":
        self.connect()
        return self
    
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        self.disconnect()


# 使用示例
if __name__ == "__main__":
    # 示例：连接数据库并查询
    with Database() as db:
        # 查询当前版本
        result = db.execute_query("SELECT version();")
        if result:
            print(f"PostgreSQL版本: {result[0]['version']}")
