import os

from src.worker.judgers.programmingJudger.checkers.baseChecker import Checker
from src.shareddata.shareddata import g_config, g_logger
class CompileChecker(Checker):
    def __init__(self, t_tag, t_sandbox):
        """
        @detail
            initial the checker with its tag and sandbox
        """
        Checker.__init__(self, t_tag, t_sandbox)

    @staticmethod
    def get_all_files(submission):
        """
        @detail
            get all related files of current submission, including answer files,
            support files and hidden support files
        """
        all_related_files = []

        standardFolder = g_config["filePath"]["standardFolder"] + str(submission["problem_id"])
        submissionFolder = g_config["filePath"]["submissionFolder"] + str(submission["submission_id"])
        problem_config = submission["problem_config"]
        #get all submission files
        if "submission" in problem_config:
            for item in problem_config["submission"]:
                all_related_files.append(submissionFolder + "/" + item)
        #get all support files
        if "standard" in problem_config and "support" in problem_config["standard"]:
            for item in problem_config["standard"]["support"]:
                all_related_files.append(standardFolder + "/support/" + item)
        #get all hidden support files
        if "standard" in problem_config and "hidden_support" in problem_config["standard"]:
            for item in problem_config["standard"]["hidden_support"]:
                all_related_files.append(standardFolder + "/support/" + item)
        return all_related_files

    @staticmethod
    def check_file_exists(all_related_files):
        """
        @detail
            checke if all related files exists
        """
        for item in all_related_files:
            if not os.path.exists(item):
                return False
        return True

    @staticmethod
    def create_compile_command(problem_config):
        """
        @detail
            create the compile command, replace code files to predefined command
        @example
            the c compile command:gcc CODE_FILES -g -w -lm -o OUTPUT_PROGRAM
            we will replace CODE_FILES with all code file names and OUTPUT_PROGRAM
            with outputgrame name
        """
        #get predefined compile command,
        if "standard_language" in problem_config and\
            "compilers" in problem_config and \
            problem_config["standard_language"] in problem_config["compilers"]:
            compile_command = problem_config["compilers"][problem_config["standard_language"]]\
                                    ["command"]
        code_files = ""
        #get all file names and padding in the compile command
        if "submission" in problem_config:
            for item in problem_config["submission"]:
                code_files = code_files + " " + item

        if "standard" in problem_config and "support" in problem_config["standard"]:
            for item in problem_config["standard"]["support"]:
                code_files = code_files + " " + item

        if "standard" in problem_config and "hidden_support" in problem_config["standard"]:
            for item in problem_config["standard"]["hidden_support"]:
                code_files = code_files + " " + item

        #get the output program name
        if "output_program" in problem_config:
            output_program = problem_config["output_program"]

        #repalce the code_files and output_program
        compile_command = compile_command.replace("CODE_FILES", code_files)
        compile_command = compile_command.replace("OUTPUT_PROGRAM", output_program)
        compile_command = "timeout --signal=KILL 10 " + compile_command
        print compile_command
        return compile_command

    def check(self, submission):
        """
        @detail
            compile the current submission in docker with sandbox
        """
        #define the report of compileChecker
        ret = {"continue":False, self.getTag():"pass", "grade":0}

        problem_config = submission["problem_config"]
        try:
            all_related_files = CompileChecker.get_all_files(submission)
            if not CompileChecker.check_file_exists(all_related_files):
                ret[self.getTag()] = "missing compile file"
                return ret
            #put all the related files to docker
            for item in all_related_files:
                self.m_sandbox.push(item)
            #get compile_command
            command = CompileChecker.create_compile_command(problem_config)
            compile_result = self.m_sandbox.pipe_exec("cd /tmp && " + command + " 2>&1")
            #nothing indicates no warning or errors
            if "" == compile_result:
                ret["continue"] = True
                ret["grade"] = problem_config["grading"]["compile check"]
            else:
                if "Killed" == compile_result:
                    ret[self.getTag()] = {"message":"Malicious \
                                                code detected", "result":"IE"}
                else:
                    ret[self.getTag()] = compile_result[:1024]
        except:
            ret[self.getTag()] = "compile system error happend"
        return ret
