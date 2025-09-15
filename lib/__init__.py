"""Top-level package for ETL."""
from .clients import FileClient, DatabaseClient
from .processors import TextProcessor
from .utils.logger import logger

__all__ = ['FileClient', 'DatabaseClient', 'TextProcessor', 'logger']
__author__ = """Lavrentiy Naumovich"""
__email__ = 'lavrikyoy@gmail.com'


