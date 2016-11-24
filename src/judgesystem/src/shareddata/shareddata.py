import json
from multiprocessing import Process, Queue
from src.utils.logger.logger import Logger
"""
g_config is the global config of this judge Server
g_queue is the workerQueue of the judgeServer
"""
g_config = json.load(open("config/config.json"))
g_queue = Queue(10000)
g_logger = Logger(g_config["log_position"])
