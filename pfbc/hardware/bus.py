class Bus:
    def __init__(self, value, n=16):
        try:
            self._value = list(value)
        except ValueError:  # TODO: correct exception
            self._value = [value is True] * n

    def __iter__(self):
        pass  # TODO: turn it into a proper sliceable iterator

    # TODO: complete bus example
