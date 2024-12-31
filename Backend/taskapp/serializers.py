from .models import Task,Team,Project,Invitation,Notification
from rest_framework import serializers
from accounts.serializers import UserSerializer



class TeamSerializer(serializers.ModelSerializer):
    leader = UserSerializer()
    members = UserSerializer(many=True)
    class Meta:
        model = Team
        fields = ['id','leader','members']

class ProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    assigned_members  = UserSerializer(many=True,read_only=True)
    task = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id','user','name','assigned_members','status','created_at','task','percentage']

    def get_task(self,obj):
        task = Task.objects.filter(project=obj)
        serializer = TaskSerializer(task,many=True)
        return serializer.data
    
    def get_percentage(self,obj):
        task = Task.objects.filter(project=obj)
        completed = Task.objects.filter(project=obj,completed=True)
        try:
            percentage = round((completed.count()/task.count())*100,1)
            if percentage == 100:
                obj.status = 'Completed'
                obj.save()
            elif percentage < 100:
                obj.status = 'In Progress'
                obj.save()
        except ZeroDivisionError:
            percentage = 0
        return percentage 

class TaskSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField()
    assigned_members = UserSerializer(many=True,read_only=True)
    

    class Meta:
        model = Task
        fields = ['id','user','title','due_date','created_at','priority','status','assigned_members','project','completed']

class InvitationSerializer(serializers.ModelSerializer):
    time_since_created = serializers.SerializerMethodField()
    sender = UserSerializer(read_only=True) 
    receiver = UserSerializer(read_only=True) 
    class Meta:
        model = Invitation
        fields = ['id','sender','receiver','responded','status','time_since_created']

    def get_time_since_created(self,obj):
        return obj.time_since_created()    
    
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    class Meta:
        model = Notification
        fields = ['id','user','message','read','date_created']    