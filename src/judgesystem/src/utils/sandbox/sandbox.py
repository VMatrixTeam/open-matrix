import os
import json
from shareddata.shareddata import g_config

class Sandbox(object):
    def __init__(self, t_name, t_default_work_space = "/tmp"):
        """
        @para
            m_name:the name of the sandbox
            m_default_work_space: the workspace of current sandbox
            m_is_running: the status of the current sandbox
        """
        self.m_name = t_name
        self.m_default_work_space = t_default_work_space
        if not self.start():
            if not self.reset():
                raise NameError
        self.m_is_running = True

    def __del__(self):
        """
        destructor
        """
        self.stop()

    def getDefaultWorkspace(self):
        """
        get default workspace
        @return the name of workspace
        """
        return self.m_default_work_space

    def clear(self):
        """
        clear temp files in the sandbox
        @return bool indicates clear success or not
        """
        clear_command = "rm -r " + self.m_default_work_space + "/*"
        return self.execute(clear_command)
    def start(self):
        """
        Start the container
        @return bool indicates start success or not
        """
        start_command = "docker run -i -d --name=" + self.m_name + " " +\
                        g_config["sandbox"]["imagename"] + \
                        " 2>/dev/null 1>/dev/null"
        print start_command
        return not os.system(start_command)

    def stop(self):
        """
        stop the container
        @return bool indicates stop success or not
        """
        stop_command = "docker stop "+self.m_name + " 2>/dev/null 1>/dev/null"
        clear_command = "docker rm "+ self.m_name + " 2>/dev/null 1>/dev/null"
        return (not os.system(stop_command)) and (not os.system(clear_command))

    def reset(self):
        """
        reset the whole sandbox
        @return bool indicates success or not
        """
        return self.stop() and self.start()

    def push(self, outer_file, inner_file = ""):
        """
        push the outterfile to inner file
        @return bool indicates success or not
        """
        if "" == inner_file:
            inner_file = self.m_default_work_space
        push_command = "docker cp "+ outer_file + " " + self.m_name + ":"+inner_file
        return not os.system(push_command)

    def pull(self, inner_file, outer_file):
        """
        pull the inner_file to the outter
        """
        pull_command = "docker cp "+ self.m_name + ":" + inner_file + " " + outer_file
        return not os.system(pull_command)

    def execute(self, command):
        """
        excute the bash command in the container use system(blocking)
        @para
            the command which will be execute
        """
        exec_command = "docker exec " + self.m_name + " bash -c \"" + \
                        command + "\""
        return not os.system(exec_command)

    def pipe_exec(self, command):
        """
        execute the command and return the output result use popen(nonBlocking)
        @return
            return the standardOutput of the powershell
        """
        exec_command = "docker exec " + self.m_name + " bash -c \"" + \
                        command + "\""
        output = os.popen(exec_command, "r")
        return output.read()


    def crun(self, **kwargs):
        """
        @detail
            the api of execute a program in a sandbox mode inside docker.
            this function will limit the time and memory of program executing
        @para
            kwargs["policy_file"] : the policy file, which include white list of
                                system invoke number and some files
            kwargs["std_in_file"] : the standardInput of the executed program
            kwargs["time_limit"]: the time_limit of program executing
            kwargs["memory_limit"]: the memory limit of program executing
            kwargs["program_params"]: the command of execute the program
        """
        #timeout limit the excute time
        command = "timeout --signal=HUP 10 /crun.py " + kwargs["policy_file"] +\
                  " " + kwargs["std_in_file"] + " " + str(kwargs["time_limit"]) +\
                  " " + str(kwargs["memory_limit"]) + " " + kwargs["program_params"]
        result = self.pipe_exec(command)
        return json.loads(result)
