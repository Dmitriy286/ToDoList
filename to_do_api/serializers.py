from rest_framework import serializers

from to_do.models import ToDoNote

class ToDoNotesAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoNote
        fields = "__all__"
        # exclude = ("public", )
        read_only_fields = ("author",)


# class ToDoNotesAPIViewQuerysetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ToDoNote
#         fields = "__all__"
#         # exclude = ("public", )
#         read_only_fields = ("author",)