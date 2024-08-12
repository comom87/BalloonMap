from enum import Enum


class ProcessingState(str, Enum):
    PENDING = "발견"
    COMPLETED = "처리 완료"
