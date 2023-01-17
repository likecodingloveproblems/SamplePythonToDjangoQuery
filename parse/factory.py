import ast
from dataclasses import dataclass
from .op import BaseOp, RootOp


@dataclass
class Parser:
    """Factory for Parser

    It will validate user_query string and replace chars if needed
    """

    parser: BaseOp = RootOp

    def parse(self, user_query, *args, **kwargs) -> BaseOp:
        """Return Parser instance

        validated user_query
        modify it as needed
        """
        self.validate()
        self.modify()
        return ast.parse(user_query, *args, **kwargs)

    def validate(self):
        """Validate user query

        for example check for especial characters like % or $
        """

    def modify(self):
        """Simple modification of user string

        for example replace = with ==
        """
