from rest_framework import serializers

class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    role_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )