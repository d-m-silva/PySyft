# stdlib
from typing import Any

# third party
from sqlalchemy import String
from sqlalchemy.engine import Engine

# relative
from ..node_table.ledger import Ledger

# from ..exceptions import SetupNotFoundError
from .database_manager import DatabaseManager


class LedgerManager(DatabaseManager):

    schema = Ledger

    def __init__(self, database: Engine) -> None:
        super().__init__(db=database, schema=LedgerManager.schema)

    def __setitem__(self, key: String(256), value: String(256)) -> None:
        if super().contain(entity_name=key):
            super().delete(entity_name=key)
        super().register(value)

    def __getitem__(self, key: String(256)) -> Any:
        if super().contain(entity_name=key):
            super().first(entity_name=key)
        else:
            return None
