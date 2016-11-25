"""
from src.worker.worker import *
from src.producer.producer import *
p = Producer()
w = Worker(1)
p.start()
w.start()
w.join()
p.join()
"""

"""
# test baseJudger
from src.worker.judgers.baseJudger import *
bj = Judger("testJudger")
bj.judge("haha")
result = {"total_grade":80, "compile:":"missing submission dependency..."}
bj.write_result_to_database(19291, result, True)
bj.write_result_to_database(19292, result, False)
"""

"""
#test Checker
from src.worker.judgers.programmingJudger.checkers.baseChecker import *
from src.utils.sandbox.sandbox import *

s = Sandbox("test_sandbox")
c = Checker("test_checker", s)
c.check("submission")
print c.getTag()
"""
#test ProgrammingJudger
from src.worker.judgers.programmingJudger.programmingJudger import *
from src.utils.sandbox.sandbox import *
s = Sandbox("test_sandbox")
pj = ProgrammingJudger("test_programmingJudger", s)

print pj.checke_submission_legal(100, 100)
print pj.checke_submission_legal(200,200)
