import os

from src.worker.programmingJudger.checkers.baseChecker import Checker
from src.shareddata.shareddata import g_config, g_logger
class RandomChecker(Checker):
    def __init__(self, t_tag, t_sandbox):
        """
        @detail
            initial the checker with its tag and sandbox
        """
        Checker.__init__(self, t_tag, t_sandbox)

    @staticmethod
    def get_random_folder(problem_id):
        return g_config["filePath"]["standardFolder"] + str(problem_id) + "/random_source"

    def generate_random_exe(self, submission):
        """
        @detail
            if there is no random program, generate the random program;
            1.generate random program compile command
            2.push random source files to docker
            3.pipe_exec compile the file generate random
            4.pull random file to local folder
        """
        #get the random program compile command
        problem_config = submission["problem_config"]
        random_command = problem_config["random"]["compile_command"]
        random_command = random_command.replace("SOURCE", \
                                problem_config["standard"]["random_source"][0])
        random_program_folder = get_random_folder(submission["problem_id"])
        #get random program fiepath
        random_program = random_program_folder + problem_config["standard"]["random_source"][0]
        #push the random program to docker
        self.m_sandbox.push(random_program)
        try:
            temp_result = self.m_sandbox.pipe_exec("cd /tmp && " + random_command + "2>&1")
            if "" != temp_result:
                return False
            #copy the random execute file to local folder
            if True == self.m_sandbox.pull("/tmp/random", random_program_folder):
                return True
        except:
            return False
        return False

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
        if "standard_language" in problem_config and
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
        if "entry_point" in problem_config:
            output_program = problem_config["entry_point"]

        #repalce the code_files and output_program
        compile_command = compile_command.replace("CODE_FILES", code_files)
        compile_command = compile_command.replace("OUTPUT_PROGRAM", output_program)
        compile_command = "timeout --signal=KILL 10 " + compile_command
        print compile_command
        return compile_command

    @staticmethod
    def get_standard_program_folder(problem_id):
        return g_config["filePath"]["standardFolder"] + str(problem_id) + "standard_main.exe"

    def generate_standard_exe(self, submission):
        """
        @detail
            if there is no standard exe, generate it and put it to local
            1.get the compile command
            2.push all the standard files to docker
            3.execuet the compile_command and generate the standard exe
            4.pull the standard exe to local folder
        """
        problem_config = submission["problem_config"]
        #get all support files,push to docker and rename support->standard_main.exe
        standard_supprt_files = g_config["filePath"]["standardForlder"] + \
                            str(submission["submission_id"]) + "/support"
        self.m_sandbox.push(standard_supprt_files)
        self.m_sandbox.pipe_exec("cd /tmp && mv support standard_main.exe")

        #get the language of current_submission
        standard_language = problem_config["standard_language"]

        #if C，C++，pascal, generate exe file and pull it to local folder
        if "c" == standard_language or "c++" == standard_language or "pascal" ==\
                standard_language:
            #generate compile_command
            command = create_compile_command(problem_config)
            try:
                compile_result = self.m_sandbox.pipe_exec("cd /tmp/standard_main.exe/ \
                                 && " + command + "2>&1")
                innerfile = "/tmp/standard_main.exe/standard_main.exe"
                standard_program_folder = get_standard_program_folder(submission["problem_id"])
                if False == self.m_sandbox.pull(innerfile, standard_program_folder)
                    return False
            except:
                return False
        return True

    def check(self, submission):
        """
        @detail
            if there is not standard exe program, generate first,
            else no need to generate
        """
        ret = {"grade":0, "report":{"continue":False, self.getTag():{}, "grade":0}}

        #get neccesary information from config
        full_grade = problem_config["grading"]["random tests"]
        memory_limit = problem_config["limits"]["memory"]
        time_limit = problem_config["limits"]["time"]
        program_name = problem_config["output_program"]
        standard_language = problem_config["standard_language"]
        entry_point = problem_config["entry_point"]
        random_time = problem_config["random"]["run_times"]

        #record the count of all test cases
        correct_case_count = 0
        wrong_case_count = 0
        abnormal_case_count = 0

        #create the execute command according to the standard_language
        execute_command = ""
        standard_execute_command = ""
        if "python2" == standard_language or "python3" == standard_language or\
            "php5" == standard_language:
            execute_command = execute_command + standard_language + " "
            standard_execute_command = standard_execute_command + standard_language + " "
        if "javascript" == standard_language:
            execute_command += "js "
            standard_execute_command += "js "
        if "prolog" == standard_language:
            execute_command += "swipl -g halt -t 'halt(1)' -l "
            standard_execute_command += "swipl -g halt -t 'halt(1)' -l "

        execute_command = execute_command + self.m_sandbox.getDefaultWorkspace()\
                          + "/" + program_name
        standard_execute_command = standard_execute_command + \
            self.m_sandbox.getDefaultWorkspace() + "/" + entry_point + "/" + entry_point

        random_program = get_random_folder(submission["problem_id"]) + "/random"
        #check whether the random exe program exists, if not generate
        if not os.path.exists(random_program):
            if not generate_random_exe(submission):
                ret["report"][self.geTag()] = {"message":"no random generator found!"}
        else:
            self.m_sandbox.push(random_program)

        standard_program = get_standard_program_folder(submission["problem_id"])

        #check whether the standard exe program exists, if not, generate it
        if not os.path.exists()
