import time
import json
from multiprocessing import Process

from src.shareddata.shareddata import *
from src.utils.mysqller.mysqller import Mysqller
class Producer(Process):
    """
    @detail
        this is a easy version of producer,produce job from roll polling the database
    """
    def __init__(self):
        Process.__init__(self)

    def run(self):
        """
            rewrite the run function of Process
            in this function, we will fetch submission which not judged to queue
        """
        #get the config of database
        mysql_config = {"db":g_config["mysql"]["db"], "host":g_config["mysql"]["host"],\
                        "user":g_config["mysql"]["user"], "passwd":g_config["mysql"]["passwd"]}
        mysql = "select s.sub_id, p.prob_id, p.config, p.ptype_id from submission as s \
                left join library_problem as p on s.prob_id = p.prob_id where \
                s.grade is null and (p.ptype_id = 0 or p.ptype_id = 1)"
        while True:
            result = Mysqller.execute(mysql, "query", **mysql_config)
            #there may be multiple submission that wating to be judged
            if None == result:
                continue
            submission = {}
            for item in result:
                submission["submission_id"] = item[0]
                submission["problem_id"] = item[1]
                submission["problem_config"] = json.loads(item[2])
                submission["problem_type"] = item[3]
                g_queue.put(submission)

                #put job finished, update database set grade = -1 indicates this\
                # submission is being judged
                update_sql = "update submission set grade = -1 where sub_id="+str(item[0])
                Mysqller.execute(update_sql, "update", **mysql_config)
            time.sleep(1)
