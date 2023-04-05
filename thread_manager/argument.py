class ThreadArgument:
    __slots__ = ("thread_name", "args", "kwargs",)

    def __init__(self, thread_name: str, args: tuple, kwargs: dict):
        """
        Constructor
        :param thread_name: Thread Name
        :type thread_name: str
        :param args: Thread arguments
        :type args: tuple
        :param kwargs: Thread keyword arguments
        :type kwargs: dict
        """
        self.thread_name = thread_name
        self.args = args
        self.kwargs = kwargs
