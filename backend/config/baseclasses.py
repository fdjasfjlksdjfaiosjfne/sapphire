import dataclasses

class CustomDataclass:
    def __new__(cls, dataclass):
        if not dataclasses.is_dataclass(dataclass):
            dataclass = dataclasses.dataclass(dataclass, frozen = True)
        def __init__(self, *args, **kwargs):
            for i in dataclasses.fields(self):
                pass
        return dataclass