from rest_framework import serializers
from apps.inventory.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "price")

    def validate(self, attrs):
        name: str = attrs["name"]
        flag = False
        for c in name:
            if c.isnumeric():
                flag = True
                break
        if flag:
            raise serializers.ValidationError({
                "name": "invalid name."
            })
        return attrs