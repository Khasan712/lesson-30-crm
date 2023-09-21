from enum import Enum


class RequestStatus(Enum):
    new = 'new'
    accepted = 'accepted'
    rejected = 'rejected'
    confirmed = 'confirmed'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]
