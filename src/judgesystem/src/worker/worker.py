#_*_coding=utf-8_*_
from multiprocessing import Process, Queue
from worker.judgers import *
class Worker(Process):
    """
    @detail
        there are two judger in the Worker(choiceJudger and programmingJudger)
    """
    def __init__(self, t_task_queue):
        Process.__init__(self)
        self.m_judger = {0:programmingJudger.ProgrammingJudger(), \
                         1:choiceJudger.ChoiceJudger()}
    def deal_with_task(self, task):
        """
         deal with the submission task
        """

    def run(self):
        while True:
            task = self.task_queue.get()
            result = deal_with_task(task)
            write_result_to_database(result)
