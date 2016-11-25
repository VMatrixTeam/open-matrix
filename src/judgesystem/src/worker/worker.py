#_*_coding=utf-8_*_
from multiprocessing import Process, Queue

from src.worker.judgers import *
from src.worker.judgers.programmingJudger.programmingJudger import *
from src.shareddata.shareddata import *
from src.utils.sandbox.sandbox import Sandbox
class Worker(Process):
    """
    @detail
        there are two judger in the Worker(choiceJudger and programmingJudger)
    """
    def __init__(self, t_worker_id):
        Process.__init__(self)
        self.m_sandbox = Sandbox("sandbox" + str(t_worker_id))
        self.m_worker_id =t_worker_id
        self.m_judgers = {0:ProgrammingJudger("programming",self.m_sandbox)}

    def deal_with_task(self, submission):
        """
         deal with the submission task
        """
        submission_id = submission["submission_id"]
        g_logger.info("[Worker] start to checking submission: ID=" + str(submission_id))

        #problem_type: 0->programing, 1->choice
        if submission["problem_type"] > 1:
            g_logger("[Worker] no such Judger to judge submission: ID=" + str(submission_id))
            return
        print "ready to judge"
        self.m_judgers[submission["problem_type"]].judge(submission)
        g_logger.info("[Worker] finished checking submission: ID=" + str(submission_id))


    def run(self):
        while True:
            g_logger.info("[worker]Current queue size is " + str(g_queue.qsize()))
            current_submission = g_queue.get()
            self.deal_with_task(current_submission)
