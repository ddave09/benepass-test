from tutorial.quickstart.models import Machine, Commands, Result
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MachineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ['url', 'user', 'address', 'password']

class CommandsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Commands
        fields = ['url', 'command']

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Result
        fields = ['url', 'machine', 'command', 'output', 'error']
