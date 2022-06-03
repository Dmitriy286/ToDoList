from datetime import datetime

from rest_framework import serializers

from to_do.models import ToDoNote, Comment


# class ToDoNotesAPIViewQuerysetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ToDoNote
#         fields = "__all__"
#         # exclude = ("public", )
#         read_only_fields = ("author",)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')
    def get_author(self, obj: Comment):
        return {
            'value': obj.author_id,
            'display': f'Author with ID: {obj.author_id}'
        }

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("author",)


class ToDoNotesAPIViewSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    def get_status(self, obj: ToDoNote):
        return {
            'value': obj.status,
            'display': obj.get_status_display()
        }
    todocomments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = ToDoNote
        read_only_fields = ("author",)
        fields = ("title", "task_description", "create_at", "update_at", 'time_point', "public", 'important', 'status',
                  "author", "todocomments")



# class NoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ToDoNote
#         fields = "__all__"
#         read_only_fields = ("author", )


class NoteSerializer(serializers.ModelSerializer):
    # status = serializers.SerializerMethodField('get_status')
    #
    # def get_status(self, obj: ToDoNote):
    #     return {
    #         'value': obj.status,
    #         'display': obj.get_status_display()
    #     }

    class Meta:
        model = ToDoNote
        fields = "__all__"
        read_only_fields = ("author",)

    title = serializers.CharField()
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        str_ = ret['create_at'].strip()
        create_at = datetime.strptime(str_, '%Y-%m-%dT%H:%M:%S.%fZ')
        ret['create_at'] = create_at.strftime('%d %B %Y %H:%M:%S')

        return ret


def serialize_comment_created(comment: Comment) -> dict:
    return {
        "id": comment.id,
        "todonote": comment.todonote_id,
        "message": comment.message,
        "author": comment.author_id
    }


class QueryParamsCommentFilterSerializer(serializers.Serializer):
    status = serializers.ListField(
        child=serializers.ChoiceField(choices=ToDoNote.Status.choices), required=False,
    )

