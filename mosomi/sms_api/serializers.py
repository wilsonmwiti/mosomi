from rest_framework import serializers

from sms.models import OutgoingApi, OutgoingApiNew, OutgoingNew


class OutgoingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutgoingNew
        fields = ['access_code', 'phone_number', 'text_message']