from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .views import *
from .serializers import *
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated


# from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class taskpage(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        result = Task.objects.all()
        serializers = TaskSerializer(result, many=True)
        contex = {
            'data': serializers.data,
            'messasge': "Task list loaded",
            'status': True}
        return Response(contex, status=200)


class tasklist(APIView):
    def get(self, request):
        result = Task.objects.all()
        serializers = TaskSerializer(result, many=True)
        updatedata = request.session.get('updatedata', None)
        request.session['updatedata'] = None
        context = {
            'data': serializers.data,
            'message': "Task list loaded",
            'updatedata': updatedata,
            'status': True
        }
        return render(request, 'index.html', context)
        # return Response(context, status=200)


class taskadd(APIView):
    def post(self, request):
        taskTitle = request.POST.get('taskTitle')
        taskDesc = request.POST.get('taskDesc')
        taskStatus = request.POST.get('taskStatus')
        data = {"title": taskTitle, "description": taskDesc, "status": taskStatus}
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'data': serializer.data,
                'message': "Task created successfully",
                'status': True}
            return redirect(reverse('all_tasks'))
            # return render(request, 'index.html', context)
            # return Response(contex, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class taskdetail(APIView):
    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task)
            updatedata = serializer.data
            request.session['updatedata'] = updatedata
            return redirect(reverse('all_tasks'))
            # return Response(context, status=200)
        except Exception as e:
            return {e}
            # return Response({'status': 'error', 'message': f'error : {e}'}, status=status.HTTP_404_NOT_FOUND)


class taskupdate(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            taskTitle = request.POST.get('taskTitle')
            taskDesc = request.POST.get('taskDesc')
            taskStatus = request.POST.get('taskStatus')
            data = {"id": id, "title": taskTitle, "description": taskDesc, "status": taskStatus}
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task, data=data)
            if serializer.is_valid():
                serializer.save()
                context = {
                    'data': serializer.data,
                    'message': 'Task updated successfully',
                    'status': 'success'
                }
                return redirect(reverse('all_tasks'))
                # return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': f'error : {e}'}, status=status.HTTP_404_NOT_FOUND)


class taskdelete(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            result = Task.objects.get(id=id)
            if result:
                result.delete()
                return redirect(reverse('all_tasks'))
                # return Response({"status": "success", "data": "Task is deleted "})
        except Exception as e:
            return Response({'status': 'error', 'message': f'error : {e}'}, status=status.HTTP_404_NOT_FOUND)
