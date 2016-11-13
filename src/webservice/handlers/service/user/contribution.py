# coding=utf-8

from handlers.base import BaseController
from tornado.web import gen

import json
import datetime
import time

from model.user import User

class ContributionHandler(BaseController):
  @gen.coroutine
  def get(self):
    datetimes = yield self.get_key_item_datetimes()
    data = yield self.calculate_contribution(datetimes)
    self.finish({
      'result': True,
      'msg': "成功获取活跃图信息",
      'data': json.dumps(data)
    })

  @gen.coroutine
  def get_key_item_datetimes(self):
    user_id = self.get_argument('user_id')
    datetimes = yield User.get_heat_datetimes_by_user_id(user_id)
    raise gen.Return(datetimes)


  @gen.coroutine
  def calculate_contribution(self, datetimes):
    contribution = {}
    for each in datetimes:

        date_string = each.createAt.strftime("%Y-%m-%d")
        date_datetime = time.strptime(date_string, '%Y-%m-%d')
        date_timestamp = int(time.mktime(date_datetime))

        if date_timestamp not in contribution:
            contribution[date_timestamp] = 1
        else:
            contribution[date_timestamp] += 1

    raise gen.Return(contribution)
