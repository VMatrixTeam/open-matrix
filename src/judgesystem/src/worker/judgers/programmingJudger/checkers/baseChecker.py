from abc import abstractmethod

class Checker(object):
    """
    @param
        tag is the name of the checkerStage
    """
    def __init__(self, t_tag):
        self.tag = t_tag

    @abstractmethod
    def check(t_submission):
        """
        @detail
            this is an abstract method
        """
        print "this is the abstract method"

    def getTag(self):
        return self.tag
