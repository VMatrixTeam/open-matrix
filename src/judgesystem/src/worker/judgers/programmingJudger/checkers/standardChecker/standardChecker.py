import os
import time
from src.worker.judgers.programmingJudger.checkers.baseChecker import Checker
from src.shareddata.shareddata import g_config, g_logger

class StandardChecker(Checker):
    def __init__(self, t_tag, t_sandbox):
        Checker.__init__(self, t_tag, t_sandbox)

    @staticmethod
    def get_all_input_files(problem_id):
        """
        @detail
            get all standard input files from config
        """
        standardInputFolder = g_config["filePath"]["standardFolder"] + \
                              str(problem_id) + "/standard_input/"
        input_files = []
        for item in os.listdir(standardInputFolder):
            input_files.append(standardInputFolder + item)
        input_files.sort()
        return input_files

    @staticmethod
    def get_all_output_contents(problem_id):
        """
        @detail
            get all standard output file contents from files
        """
        standardOutputFolder = g_config["filePath"]["standardFolder"] + \
                               str(problem_id) + "/standard_output/"
        output_files = []
        output_contents = []
        for item in os.listdir(standardOutputFolder):
            output_files.append(standardOutputFolder + item)
        output_files.sort()
        print output_files
        for item in output_files:
            tmp = open(item)
            output_contents.append(tmp.read())
            tmp.close()
        return output_contents

    def check(self, submission):
        ret = {"continue":False, self.getTag():{}, "grade":0}
        problem_config = submission["problem_config"]
        problem_id = submission["problem_id"]

        #get all standard input files and standard output content
        all_input_files = StandardChecker.get_all_input_files(problem_id)
        all_output_contents = StandardChecker.get_all_output_contents(problem_id)
        all_test_amount = min(len(all_input_files), len(all_output_contents))

        if all_test_amount <= 0:
            ret[self.getTag()]["message"] = "system internal error(no test cases found)"

        #get neccesary information from config
        full_grade = problem_config["grading"]["standard tests"]
        memory_limit = problem_config["limits"]["memory"]
        time_limit = problem_config["limits"]["time"]
        program_name = problem_config["output_program"]
        standard_language = problem_config["standard_language"]

        #record the count of all test cases
        correct_case_count = 0
        wrong_case_count = 0
        abnormal_case_count = 0

        #create the execute command according to the standard_language
        execute_command = ""

        if "python2" == standard_language or "python3" == standard_language or\
            "php5" == standard_language:
            execute_command = execute_command + standard_language + " "
        if "javascript" == standard_language:
            execute_command += "js "
        if "prolog" == standard_language:
            execute_command += "swipl -g halt -t 'halt(1)' -l "

        execute_command = execute_command + self.m_sandbox.getDefaultWorkspace()\
                          + "/" + program_name
        print "the test amount is:" , all_test_amount
        for index in xrange(0, all_test_amount):
            self.m_sandbox.push(all_input_files[index])
            try:
                sandbox_command = {"policy_file":"/policy/" + standard_language + ".json",\
                                   "std_in_file":self.m_sandbox.getDefaultWorkspace() + "/"\
                                    + os.path.basename(all_input_files[index]),\
                                   "time_limit":time_limit, "memory_limit":memory_limit * 1024,\
                                   "program_params":execute_command}
                checker_result = self.m_sandbox.crun(**sandbox_command)
                #if result is ok, the docker execute normal
                if "OK" == checker_result["result"]:
                    if checker_result["stdout"] == all_output_contents[index]:
                        correct_case_count += 1
                    else:
                        wrong_case_count += 1
                        #only record one error report
                        if wrong_case_count <= 1:
                            checker_result["stdout"] = checker_result["stdout"][:1024]
                            checker_result["standard_stdout"] = all_output_contents[index]
                            checker_result["result"] = "WA"
                            ret[self.getTag()].update(checker_result)
                else:
                    abnormal_case_count += 1
                    if abnormal_case_count <= 1:
                        checker_result["stdout"] = checker_result["stdout"][:1024]
                        checker_result["standard_stdout"] = all_output_contents[index]
                        ret[self.getTag()].update(checker_result)
            except:
                ret[self.getTag()] = {"message":"Malicious code detected!",\
                                                "result":"IE"}
                return ret

        ret["grade"] = float(correct_case_count) / float(all_test_amount) * problem_config["grading"][self.getTag()]
        ret["continue"] = True
        return ret
