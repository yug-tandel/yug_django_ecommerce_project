from django.core import serializers


# class ProductSerializer(serializers.Serializer):
#     def serialize(self, queryset):
#         """Converts a queryset of Product objects to a JSON-formatted string"""
#         return serializers.serialize('json', queryset)

#     def deserialize(self, serialized_data):
#         """Converts a JSON-formatted string to a list of Product objects"""
#         return [serializers.deserialize('json', obj) for obj in serialized_data]
