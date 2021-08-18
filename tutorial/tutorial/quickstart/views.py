from django.contrib.auth import models
from django.forms.models import model_to_dict
from django.db.models import query
from rest_framework import decorators
from rest_framework.decorators import action, api_view, permission_classes
from tutorial.quickstart.models import Machine, Commands, Result
from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer, MachineSerializer, CommandsSerializer, ResultSerializer

import paramiko

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommandsViewSet(viewsets.ModelViewSet):
    queryset = Commands.objects.all()
    serializer_class = CommandsSerializer
    permission_classes = [permissions.IsAuthenticated]

    '''
    API format: /commands/<command_id>/execute/?machines=<comma_separated_machine_ids>
    This code can be refactored to take the business logic to another module.
    '''
    @action(detail=True)
    def execute(self, request, pk=None):
        command = Commands.objects.all().filter(pk=int(pk)).first()
        results = []

        if command:
            machines = request.query_params.getlist('machines')
            if len(machines) == 0:
                response = {
                    'status': 400,
                    'message': 'Malformed request.  Machines not provided.',
                    'results': results
                }

                return Response(response, 400)

            if len(machines) > 1:
                response = {
                    'status': 400,
                    'message': 'Malformed request.'+
                                '  Expected query: ?machine=command_separated_machines'
                                '  Potential provided query: ?machine=machine&machine=machine',
                    'results': results
                }

                return Response(response, 400)

            machines = machines[0].split(',')

            '''
            All or nothing.
            First checks if all the machines provided are valid.
            Only then exectute command on the given machines.
            '''
            for machine in machines:
                if not machine.isnumeric():
                    response = {
                        'status': 400,
                        'message': 'Malformed request. Each machine is ought be an integer.',
                        'results': results
                    }

                    return Response(response, 400)

            for machine in machines:
                machineDetails = Machine.objects.all().filter(pk=machine).first()

                if machineDetails:
                    ssh = paramiko.SSHClient()
                    ssh.load_system_host_keys()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(machineDetails.address, username=machineDetails.user, password=machineDetails.password)
                    _, ssh_out, ssh_error = ssh.exec_command(command.command)
                    error = ssh_error.readlines()
                    out = ssh_out.readlines()
                    ssh.close()
                    result = Result(machine=machine
                                    , command=command.command
                                    , output=out
                                    , error=error)
                    result.save()
                    results.append(model_to_dict(result))

        response = {
            'status': 200,
            'message': 'Success',
            'results': results
        }

        return Response(response, 200)

class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

