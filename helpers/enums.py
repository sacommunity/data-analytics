"""list of enums"""
from enum import Enum

class JobStatus(Enum):
    """job status"""
    DEFAULT = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    FAILED = 3


class DataFrequency(Enum):
    """data frequency in which data are transformed / aggregated"""
    DEFAULT = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4


class DataModule(Enum):
    """Different data modules found in google analytics"""
    DEFAULT = 0
    AGE = 1
    GENDER = 2
    LANDING_PAGE = 3
    DEVICE_CATEGORY = 4
    SOURCE_MEDIUM = 5

class GoogleAuthenticationMethod(Enum):
    """Authentication methods"""
    DEFAULT = 0
    OAUTH = 1
    SERVICE_ACCOUNT = 2
