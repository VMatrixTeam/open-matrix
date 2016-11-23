import json
from multiprocessing import Process, Queue
import src.utils.logger.logger
"""
g_config is the global config of this judge Server
g_queue is the workerQueue of the judgeServer
"""
g_config = json.load(open(config/config.py))
g_queue = Queue(10000)
g_logger = logger.Logger(g_config["log_position"])
