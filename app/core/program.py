import bisect
from singleton import Singleton


@Singleton
class ProgramStorage:
    program_dict = None

    def __init__(self):
        self.program_dict = {'1': [], '2': []}

    def get_program_list(self, machine_id):
        return self.program_dict[machine_id]

    def add_program(self, machine_id, name):
        list = self.program_dict[machine_id]

        if list is not None:
            if name not in list:
                bisect.insort(list, name)
