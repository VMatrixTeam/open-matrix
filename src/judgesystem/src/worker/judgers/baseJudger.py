import json
from abc import abstractmethod
from src.utils.mysqller.mysqller import *
from src.shareddata.shareddata import g_config

class Judger(object):
    def __init__(self, t_tag):
        self.m_tag = t_tag

    @abstractmethod
    def judge(self, submission):
        print "this is the abstractmethod of the judge"

    @staticmethod
    def write_result_to_database(submission_id, result, write_grade):
        """
        @detail
            write the judge result to database
        """
        if True == write_grade:
            sql = "update submission set grade = {0}, report = {1} where sub_id \
                  = {2}".format(result["grade"], json.dumps(result["report"]), submission_id)
        else:
            sql = "update submission set report = {0} where sub_id = \
                    {1}".format(result["report"], submission_id)
        #get the config of database
        mysql_config = {"db":g_config["mysql"]["db"], "host":g_config["host"], \
                        "user":g_config["mysql"]["user"], "passwd":g_config["mysql"]["passwd"]}
        #excute the mysql
        Mysqller.execute(mysql, "update", **mysql_config)
