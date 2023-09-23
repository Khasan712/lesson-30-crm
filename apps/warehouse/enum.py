from enum import Enum


class RequestStatus(Enum):
    new = 'new'
    acceptep = 'acceptep'
    rejected = 'rejected'
    confirmed = 'confirmed'
    
    
    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]