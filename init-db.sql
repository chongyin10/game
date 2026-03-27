-- 游戏管理系统数据库初始化脚本

-- 创建扩展（如果不存在）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建 userinfo 表
CREATE TABLE IF NOT EXISTS userinfo (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_userinfo_email ON userinfo(email);
CREATE INDEX IF NOT EXISTS idx_userinfo_phone ON userinfo(phone);
CREATE INDEX IF NOT EXISTS idx_userinfo_username ON userinfo(username);
