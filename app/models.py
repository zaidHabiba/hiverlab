from django.db import models
import json

import os


def get_upload_path(instance, filename):
    return os.path.join("{}/{}_{}_{}".format("programs", instance.project_name.replace(" ", "_").lower(),
                                             instance.program_name.replace(" ", "_").lower(), filename.replace(".py", "")), filename)


class Project(models.Model):
    project_name = models.CharField(max_length=120)

    @property
    def programs_list(self):
        return self.programs.all()

    def __str__(self):
        return self.project_name


class Program(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    program_name = models.CharField(max_length=120)
    file = models.FileField(upload_to=get_upload_path)
    password = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL,
                                related_name="programs", null=True)
    always_running = models.BooleanField(default=False)
    git = models.TextField(max_length=500, blank=True, null=True)
    custom_args = models.TextField(max_length=255, blank=True, null=True)

    @property
    def project_name(self):
        return self.project.project_name

    def __str__(self):
        return self.program_name


class ProgramAction:
    ACTION_START = 'START'
    ACTION_OUTPUT = 'OUTPUT'
    ACTION_INPUT = 'INPUT'
    ACTION_OUTPUT_ERROR = 'OUTPUT_ERROR'
    ACTION_END = 'END'
    ACTION_PROCESS_RUNNING = 'ACTION_PROCESS_RUNNING'

    def __init__(self, action, data):
        self.action = action
        self.data = data

    def send(self):
        return json.dumps({"action": self.action, "data": self.data})

    @staticmethod
    def received(obj):
        json_data = json.loads(obj)
        return ProgramAction(json_data.get('action', ''), json_data.get('data', ''))
