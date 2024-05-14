from rest_framework import serializers


class UserProfileInsertSerializer(serializers.Serializer):
    FirstName = serializers.CharField(required=True)
    LastName = serializers.CharField(required=True )
    Email = serializers.CharField(required=True )
    Password = serializers.CharField(required=True )
    Phone = serializers.CharField(required=True )
    Address = serializers.CharField(required=False, allow_null=True, allow_blank=True )
    City = serializers.CharField(required=True )
    Country = serializers.CharField(required=True )
    Pincode = serializers.CharField(required=True )
    class Meta:
        fields = '__all__'
