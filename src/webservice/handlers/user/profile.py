# coding=utf-8

from handlers.base import BaseController
from tornado.web import gen

from model.user import User

class ProfileHandler(BaseController):
    @gen.coroutine
    def get(self, user_id):
      if not user_id.isdigit():
        self.finish({
          'result': False,
          'msg': "参数错误"
        });
        raise gen.Return(None)

      user = yield User.get_user_by_id(user_id)
      timeline_recs = yield self.process_timeline_data(user_id)

      self.render("user/profile.jade", profile_user=user, current_user=self.current_user, records=timeline_recs)

    @gen.coroutine
    def process_timeline_data(self, user_id):
      q_records = yield User.get_question_records_by_user_id(user_id)
      a_records = yield User.get_answer_records_by_user_id(user_id)
      c_record = yield User.get_oldest_comment_record_by_user_id(user_id)
      print 'q_records: ',q_records
      records = self.add_attrs(q_records, 'Question') + self.add_attrs(a_records, 'Answer') + self.add_attrs(c_record, 'Comment')

      sort_recs = self.sort_by_time(records)
      print 'sort_recs: ', sort_recs
      raise gen.Return(sort_recs)

    ##
    ## @brief      Add status,category,date for records
    ##
    ## @param      self       The object
    ## @param      records    The question,answer or comment records which
    ##                        must be in ASCENDING order by 'createAt'
    ## @param      category   To determine which category it is
    ##
    ## @return     format records
    ##
    def add_attrs(self, records, category):
      if len(records) == 0:
        return records
      # if len(records) == 1:
      #   records['status'] = 'first'
      else:
        records[0]['status'] = 'first'
        records[0]['category'] = category
        records[0]['date'] = records[0]['createAt'].strftime("%d / %m")
      for i in range(1, len(records)):
        records[i]['category'] = category
        records[i]['status'] = 'common'
        records[i]['date'] = records[i]['createAt'].strftime("%d / %m")

      return records


    ##
    ## @brief      sort record list by 'createAt' in DESCENDING order and
    ##             add month attr for dividing month interval
    ##
    ## @param      self     The object
    ## @param      records  The record list
    ##
    ## @return     format list
    ##
    def sort_by_time(self, records):
      sort_recs = sorted(records, key=lambda x:x['createAt'], reverse=True)
      sort_recs[0]['month'] = d_flag = sort_recs[0]['createAt'].strftime('%m / %Y')
      for rec in sort_recs:
        date = rec['createAt'].strftime('%m / %Y')
        if d_flag != date:
          d_flag = rec['month'] = date
        else:
          pass

      return sort_recs
