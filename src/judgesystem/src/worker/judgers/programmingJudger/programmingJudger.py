from src.shareddata.shareddata import g_config
from src.worker.judgers.baseJudger import Judger
from src.worker.judgers.ProgrammingJudger.checkers import *


class ProgrammingJudger(Judger):

    def __init__(self, t_tag, t_sandbox):
        """
        @detail
            ProgrammingJudger derived from baseJudger Judger, who has a sandbox
            from worker, the user program will be executed in docker with sandbox
        """
        Judger.__init__(self, t_tag)
        self.m_sandbox = t_sandbox
        self.m_checkers = {0: compileChecker.CompileChecker("compile check", t_sandbox),
                           1: staticChecker.StaticChecker("static check", t_sandbox),
                           2: standardChecker.StandardChecker("standard tests", t_sandbox),
                           3: randomChecker.RandomChecker("random tests", t_sandbox),
                           4: memoryChecker.MemoryChecker("memory check", t_sandbox)
                            }

    def judger(self, submission):
         """
         @param
            submission is the detail of a student submission,
            @structure is as:
                {"submission_id":s_id, "submission_problem_id":p_id,
                 "problem_type":p_type, "submission_type":s_type,
                 "submission_problem_config":config}
             @detail
                submission_id : the id of current submission
                submission_problem_id: the id of problem corresponding to current sub
                problem_type: choice or programming
                submission_type:student submission or teacher design a problem
                submission_config: the config of submission
         """
         submission_id = submission["submission_id"]
         problem_id = submission["problem_id"]
         config = submission["submission_config"]
         # ret is used to store the judge result
         ret["total_grade"] = 0
         ret["submission_id"] = submission_id

         # if missing submission dependency, write the report and return
         if not (check_submission_legal(submission_id, problem_id)):
             ret["error"] = "missing submission dependency"
             ret["write_grade"] = 1
             self.write_result_to_database(submission_id, ret, True)
             return

        self.m_sandbox.clear()
        can_continue = True
        will_check = True
        total_grade = 0
        g_logger.info("[Judger Programming] start to check submission id = " + \
                     str(submission_id))
        for index in xrange(0, 5):
            # continue when this stage not in the config
            if self.m_checkers[index].getTag() not in config["grading"]:
                continue

            will_check = (index == 0) or (config["grading"][self.m_checkers[index]] > 0)
            if can_continue and will_check:
                temp = self.m_checkers[index].check(submission)
                can_continue = temp["result"]["continue"]
                total_grade = total_grade + temp["grade"]
                ret["total_grade"] = total_grade
                ret[self.m_checkers[index].getTag()] = temp["report"]
                self.write_result_to_database(submission_id, ret, False)
                g_logger.info("[Judger Programming] checking submission id={0}, \
                            chekingstage={1}, grading={2}".format(submission_id,\
                            self.m_checkers[index].getTag(), temp["grade"]))
        self.write_result_to_database(submission_id, ret, True)

    @staticmethod
    def check_submission_legal(submission_id, problem_id):
        """
            checker submission and standard files exists or not,
            if missing some of them, return False, else True
        """
        return os.path.exists(g_config["filePath"]["submissionFolder"] + str(submission_id)) \
               os.path.exists(g_config["filePath"]["standardForlder"] + str(problem_id))
