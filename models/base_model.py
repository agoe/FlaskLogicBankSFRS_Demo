import safrs
from safrs import SAFRSBase

db = safrs.DB
SAFRSBase.db_commit = False


class BaseModel(SAFRSBase):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    #__abstract__ = True
    # Enables us to handle db session ourselves

    # Override SAFRS __str__ with custom repr
    '''
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "<{}: id={}{}>".format(
            self.__class__.__name__,
            self.id,
            f" name={self.name}" if hasattr(self, "name") else "",
        )
    '''