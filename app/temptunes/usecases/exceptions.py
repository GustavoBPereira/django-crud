class UsecasesBaseException(Exception):
    pass


class CityNotFound(UsecasesBaseException):
    pass


class PlaylistNotFound(UsecasesBaseException):
    pass


class UnknownPartnerError(UsecasesBaseException):
    pass
