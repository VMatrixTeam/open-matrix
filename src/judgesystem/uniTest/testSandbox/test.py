import sandbox
#test function constructor, start and reset and destructor
s = sandbox.Sandbox("sandbox1")

#test function getDefaultWorkspace
print s.getDefaultWorkspace()

#test function push
s.push("config.json")

#test function pipe_exec
print s.pipe_exec("cat /tmp/config.json")
#test function pull
s.pull("/tmp/config.json", "config1.json")
#test function clear
s.clear()
print "clear complete"
print s.pipe_exec("cat /tmp/config.json")

#test function crun
s.push("main.cpp")
s.push("input")

#test the pipe_exec(compile the code)
print s.pipe_exec("cd tmp && g++ main.cpp 2>&1")

data = {"policy_file":"/policy/c++.json", "std_in_file":"/tmp/input",
        "time_limit":1000, "memory_limit":100000, "program_params":"/tmp/a.out"}

print s.crun(**data)
