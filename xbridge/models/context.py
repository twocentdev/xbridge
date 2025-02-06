class Context:

    def __init__(self,
                 id_=None,
                 entity=None,
                 period=None,
                 scenario=None
                 ):
        self.__id = id_
        self.__entity = entity
        self.__period = period
        self.__scenario = scenario

    @property
    def id(self):
        return self.__id

    @property
    def entity(self):
        return self.__entity

    @property
    def period(self):
        return self.__period

    @property
    def scenario(self):
        return self.__scenario

    def __repr__(self) -> str:
        return (
            f"Context(id={self.id}, entity={self.entity}, "
            f"period={self.period}, scenario={self.scenario})"
        )

    def __dict__(self):
        result = {"entity": self.entity, "period": self.period}

        for key, value in self.scenario.dimensions.items():
            result[key] = value

        return result
