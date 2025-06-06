#!/usr/bin/env python3
"""
日志管理模块
提供统一的日志记录功能
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
import os


def setup_logger(name: str = "arxiv_tracker") -> logging.Logger:
    """
    设置日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 从环境变量读取日志级别，默认为 INFO
    default_log_level = "INFO"
    log_level_str = os.environ.get("LOG_LEVEL", default_log_level).upper()
    
    # 确保转换后的日志级别是有效的logging级别，否则回退到INFO
    log_level = getattr(logging, log_level_str, None)
    if not isinstance(log_level, int):
        print(f"Warning: Invalid LOG_LEVEL '{log_level_str}'. Defaulting to INFO.", file=sys.stderr)
        log_level = logging.INFO
        
    logger.setLevel(log_level)

    # 创建格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件处理器（可选）
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(
        log_dir / f"arxiv_tracker_{datetime.now().strftime('%Y%m%d')}.log",
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# 创建默认日志记录器
logger = setup_logger()
