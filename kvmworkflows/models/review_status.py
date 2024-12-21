from enum import StrEnum


class ReviewStatus(StrEnum):
    """
    * created = initial status of each revision * confirmed/rejected = after positive/negative review * archived = final status 
    """

    """
    allowed enum values
    """
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    ARCHIVED = 'archived'