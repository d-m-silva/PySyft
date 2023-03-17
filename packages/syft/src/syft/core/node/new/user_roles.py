# stdlib
from enum import Enum
from typing import Any
from typing import List
from typing import Tuple
from typing import Union

# third party
from typing_extensions import Self

# relative
from .serializable import serializable


class ServiceRoleCapability(Enum):
    CAN_MAKE_DATA_REQUESTS = 1
    CAN_TRIAGE_DATA_REQUESTS = 2
    CAN_MANAGE_PRIVACY_BUDGET = 4
    CAN_CREATE_USERS = 8
    CAN_MANAGE_USERS = 16
    CAN_EDIT_ROLES = 32
    CAN_MANAGE_INFRASTRUCTURE = 64
    CAN_UPLOAD_DATA = 128
    CAN_UPLOAD_LEGAL_DOCUMENT = 256
    CAN_EDIT_DOMAIN_SETTINGS = 512


@serializable(recursive_serde=True)
class ServiceRole(Enum):
    NONE = 0
    GUEST = 1
    DATA_SCIENTIST = 2
    DATA_OWNER = 32
    ADMIN = 128

    @classmethod
    @property
    def roles_descending(cls) -> List[Tuple[int, Self]]:
        tuples = []
        for x in cls:
            tuples.append((x.value, x))
        return list(reversed(sorted(tuples)))

    @staticmethod
    def roles_for_level(level: Union[int, Self]) -> List[Self]:
        if isinstance(level, ServiceRole):
            level = level.value
        roles = []
        level_float = float(level)
        service_roles = ServiceRole.roles_descending
        for role in service_roles:
            role_num = role[0]
            if role_num == 0:
                continue
            role_enum = role[1]
            if level_float / role_num >= 1:
                roles.append(role_enum)
                level_float = level_float % role_num
        return roles

    def __add__(self, other: Any) -> int:
        if isinstance(other, ServiceRole):
            return self.value + other.value
        return self.value + other

    def __radd__(self, other: Any) -> int:
        return self.__add__(other)


GUEST_ROLE_LEVEL = ServiceRole.roles_for_level(
    ServiceRole.GUEST
    + ServiceRole.DATA_SCIENTIST
    + ServiceRole.DATA_OWNER
    + ServiceRole.ADMIN
)

DATA_SCIENTIST_ROLE_LEVEL = ServiceRole.roles_for_level(
    ServiceRole.DATA_SCIENTIST + ServiceRole.DATA_OWNER + ServiceRole.ADMIN
)

DATA_OWNER_ROLE_LEVEL = ServiceRole.roles_for_level(
    ServiceRole.DATA_OWNER + ServiceRole.ADMIN
)

ADMIN_ROLE_LEVEL = ServiceRole.roles_for_level(ServiceRole.ADMIN)
