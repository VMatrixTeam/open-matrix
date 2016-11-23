from src.worker.judgers.programmingJudger.checkers.baseChecker import Checker

class StaticChecker(Checker):
    """
    @detail
        this is the checker which check the static style
    """
    def __init__(self, t_tag):
        Checker.__init__(self, t_tag)

    def check(t_submission):
        
