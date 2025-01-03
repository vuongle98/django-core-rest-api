
from enum import Enum

class MessageType(Enum):
    CHECK_STATUS = 'check_status'
    UPDATE_ONLINE_STATUS = 'update_online_state'
    ERROR = 'error'