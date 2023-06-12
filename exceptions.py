class CustomExceptions:
    class IllegalProbabilityException(Exception):
        pass

    class InvalidGameType(Exception):
        pass

    class PositiveWDL(Exception):
        pass