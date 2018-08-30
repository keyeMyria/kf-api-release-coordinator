from coordinator.api.models import Task, TaskService, Release, Event, Study
from rest_framework import serializers
from coordinator.api.validators import validate_study


class StudySerializer(serializers.HyperlinkedModelSerializer):

    version = serializers.CharField(source='latest_version', allow_blank=True)

    class Meta:
        model = Study
        fields = ('kf_id', 'name', 'version', 'visible',
                  'deleted', 'created_at')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    service_name = serializers.CharField(read_only=True,
                                         source='task_service.name')

    class Meta:
        model = Task
        fields = ('kf_id', 'state', 'progress', 'release', 'task_service',
                  'created_at', 'service_name')
        read_only_fields = ('kf_id', 'created_at')
        extra_kwargs = {
            'release': {'allow_null': False, 'lookup_field': 'kf_id'},
            'task_service': {'allow_null': False, 'lookup_field': 'kf_id'},
        }


class TaskServiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TaskService
        fields = ('kf_id', 'name', 'description', 'last_ok_status', 'author',
                  'health_status', 'url', 'created_at', 'enabled')
        read_only_fields = ('kf_id', 'last_ok_status', 'health_status',
                            'created_at')


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.ListField(
                child=serializers.CharField(max_length=50, allow_blank=False,
                                            validators=[]))

    studies = serializers.PrimaryKeyRelatedField(queryset=Study.objects.all(),
                                                 many=True)

    def validate_studies(self, studies):
        if len(studies) == 0:
            raise serializers.ValidationError('Must have at least one study')
        return studies

    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = Release
        fields = ('kf_id', 'name', 'description', 'state', 'studies',
                  'tasks', 'version', 'created_at', 'tags', 'author',
                  'is_major')
        read_only_fields = ('kf_id', 'state', 'tasks', 'version', 'created_at',
                            'version')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('kf_id', 'event_type', 'message', 'release', 'task_service',
                  'task', 'created_at')
        read_only_fields = ('kf_id', 'created_at')
        extra_kwargs = {
            'release': {'allow_null': True, 'lookup_field': 'kf_id'},
            'task_service': {'allow_null': True, 'lookup_field': 'kf_id'},
            'task': {'allow_null': True, 'lookup_field': 'kf_id'},
        }
