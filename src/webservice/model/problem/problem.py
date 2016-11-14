import model.base
import tornado.gen

class Problem(object):
    @staticmethod
    @tornado.gen.coroutine
    def get_top_problems():
        result = yield model.MatrixDB.query("\
            SELECT p.prob_id, p.title, COUNT(s.sub_id) as submits \
            FROM problem p, submission s \
            where s.prob_id = p.prob_id \
            GROUP BY p.prob_id \
            ORDER BY submits DESC \
            LIMIT 0,10")
        raise tornado.gen.Return(result)


    @staticmethod
    @tornado.gen.coroutine
    def get_problem_list():
        result = yield model.MatrixDB.query("\
        select t1.prob_id, t1.title, t1.passes, t2.submit_sum from \
        (select p.prob_id, p.title, COUNT(s.sub_id) as passes \
            FROM problem p, submission s \
            where p.prob_id = s.prob_id and s.grade = 100 \
            group by p.prob_id) as t1 \
            LEFT JOIN \
        (select p.prob_id, COUNT(s.sub_id) as submit_sum \
            FROM problem p, submission s \
            where p.prob_id = s.prob_id \
            GROUP BY p.prob_id) as t2 \
            on t1.prob_id = t2.prob_id")

        raise tornado.gen.Return(result)
