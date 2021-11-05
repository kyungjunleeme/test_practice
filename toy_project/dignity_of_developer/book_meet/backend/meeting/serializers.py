from .models import Meeting, Room
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ValidationError

# current user 관련 마지막 확인
# https://stackoverflow.com/questions/51940976/django-rest-framework-currentuserdefault-with-serializer


# class AttrPKField(serializers.PrimaryKeyRelatedField):
#     default_error_messages = {"does_not_exist": "본인의 계좌 id 값을 입력해주시기 바랍니다."}

#     def get_queryset(self):
#         user = self.context["request"].user
#         queryset = Account.objects.filter(user=user)
#         return queryset

# # option#1
# class MeetingCreateSerializer(serializers.ModelSerializer):
#     owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     # account = AttrPKField()

#     def create(self, validated_data):
#         owner = validated_data.get("owner", "")
#         validated_data["user"] = owner
#         validated_data.pop("owner", None)
#         meeting = Meeting.objects.create(**validated_data)
#         return meeting

#     class Meta:
#         model = Meeting
#         fields = [
#             "title",
#             "meeting_date",
#             "meeting_starttime",
#             "meeting_end_time",
#             "owner",
#         ]


# option#2
class MeetingCreateSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        """1. Override ``create`` to provide a user via request.user by default.
        This is required since the read_only ``user`` field is not included by
        default anymore since
        https://github.com/encode/django-rest-framework/issues/6031
        https://github.com/encode/django-rest-framework/pull/5886.

        2.read_only
        Read-only fields are included in the API output, but should not be included in the input during create or update operations. Any 'read_only' fields that are incorrectly included in the serializer input will be ignored.
        Set this to True to ensure that the field is used when serializing a representation, but is not used when creating or updating an instance during deserialization.
        Defaults to False
        """
        if "user" not in validated_data:
            validated_data["user"] = self.context["request"].user
        meeting = Meeting.objects.create(**validated_data)
        return meeting

    class Meta:
        model = Meeting
        fields = [
            "title",
            "meeting_date",
            "meeting_starttime",
            "meeting_end_time",
        ]

        # fields = ["title", "meeting_date", "meeting_starttime", "meeting_end_time", "owner"]

        """Override ``create`` to provide a user via request.user by default.
        This is required since the read_only ``user`` field is not included by
        default anymore since
        https://github.com/encode/django-rest-framework/pull/5886.
        """
        # if "user" not in validated_data:
        #     validated_data["user"] = self.context["request"].user

        # title = validated_data.get("account", "")  # <Account: 777777>

    # account_id = account.id
    # account_instance = Account.objects.get(id=account_id)
    # amount = validated_data.get("amount", "")
    # notes = validated_data.get("notes", "")
    # if "deposit" in self.context["request"].path:
    #     account_instance.deposit(id=account_id, amount=amount)
    #     version = account.version
    #     new_version = int(version) + 1
    #     account_new = Account.objects.get(id=account_id, version=new_version)
    #     asof_balance = account_new.balance
    #     print("입금")
    #     action = Action.objects.create(
    #         account=account,
    #         type="deposit",
    #         amount=amount,
    #         notes=notes,
    #         asof_balance=asof_balance,
    #     )
    #     return action

    # def validate(self, attrs):
    #     if attrs["owner"].pk != attrs["account"].user.pk:
    #         raise ValidationError("계좌의 소유자만 해당 작업을 수행할 수 있습니다.")
    #     return attrs

    # fields = ["owner", "title", "meeting_date", "room_set", "meeting_starttime", "meeting_end_time"]


# class Meeting(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="host"
#     )
#     # host = models.CharField(max_length=50)  # null=False, blank=False, 필수 값
#     # token 값 활용해서-> 변환해서 저장 ## 창성님이 알려주신 방법대로
#     # 1) https://han-py.tistory.com/353 , #2) request.user # 요지는 forntend, 자동적으로 값 가져오도록
#     title = models.CharField(max_length=100)
#     meeting_date = models.DateField()
#     room_set = models.ManyToManyField(Room)  # 선택한 회의실
#     user_set = models.ManyToManyField(
#         settings.AUTH_USER_MODEL, related_name="guest"
#     )  # 회의 참석자들 [1, 2, 3]
#     meeting_starttime = models.DateTimeField()  # 14:00
#     meeting_end_time = models.DateTimeField()  # 10:00

#     def __str__(self):
#         return str(self.pk)
