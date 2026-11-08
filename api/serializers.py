from rest_framework import serializers


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = "__all__"
