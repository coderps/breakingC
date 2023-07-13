from rest_framework import serializers
from django.contrib.auth.models import User
from bc.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class StuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stuff
        fields = '__all__'


class StuffRecordSerializer(serializers.ModelSerializer):
    where = serializers.CharField(source='record.where')
    record = serializers.CharField(source='record.name')
    player = serializers.CharField(source='player.username')
    done_on = serializers.DateField(format='%Y-%m-%d', required=False)
    added_on = serializers.DateField(format='%Y-%m-%d', required=False)
    aggregated_value = serializers.SerializerMethodField()

    def get_aggregated_value(self, instance):
        player1_value = instance.value if instance.player.username == 'airin' else 0
        player2_value = instance.value if instance.player.username == 'prax' else 0
        return (player1_value, player2_value)

    class Meta:
        model = StuffRecord
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ShopRecordSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format='%Y-%m-%d', required=False)
    updated_at = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = ShopRecord
        fields = '__all__'


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'


class VacationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacationRecord
        fields = '__all__'
