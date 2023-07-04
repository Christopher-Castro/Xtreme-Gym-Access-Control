import os
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, ListAttribute
)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

class ViewIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """
    class Meta:
        # index_name is optional, but can be provided to override the default name
        index_name = 'FullName-index'
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        read_capacity_units = 1
        write_capacity_units = 1
        # All attributes are projected
        projection = AllProjection()

    # This attribute is the hash key for the index
    # Note that this attribute must also exist
    # in the model
    FullName = UnicodeAttribute(hash_key=True)

class User(Model):
    class Meta:
        table_name = 'facerecognition'
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        projection = AllProjection()

    RekognitionId = UnicodeAttribute(hash_key=True)
    FullName = UnicodeAttribute()
    FullName_index = ViewIndex()
    email = UnicodeAttribute()
    phone = UnicodeAttribute()
    location = UnicodeAttribute()
    access_history = ListAttribute(default=list)
    suscription_start = UnicodeAttribute()
    suscription_end = UnicodeAttribute()