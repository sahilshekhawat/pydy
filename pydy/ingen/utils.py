__all__ = ['AssignName']


class AssignName(object):
    def __init__(self):
        self.q = 0
        self.u = 0
        self.body = 0

    def increment_q(self):
        self.q += 1

    def increment_body(self):
        self.body += 1

    def increment_u(self):
        self.u += 1

    def get_next_q(self):
        return 'q' + str(self.q)

    def get_next_u(self):
        return 'u' + str(self.u)

    def get_next_body_name(self):
        return 'body' + str(self.body)