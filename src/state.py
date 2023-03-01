class State:

    _instance = None

    def __new__(cls):
        """Returns class instance if it exists."""
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Live and ready parameters initialization."""
        self.__live = False
        self.__ready = False

    def get_live_status(self):
        """Liveness status retrieval."""
        return self.__live

    def get_ready_status(self):
        """Readiness status retrieval."""
        return self.__ready

    def set_live_status(self, status: bool):
        """Liveness status setter."""
        self.__live = status

    def set_ready_status(self, status: bool):
        """Readiness status setter."""
        self.__ready = status
