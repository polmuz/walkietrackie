from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Walk
from .serializers import WalkSerializer

@login_required
def main(request):
    walks = Walk.objects.filter(user=request.user)
    return render(request, "walks/main.html", {'walks': walks})


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def walk_list_api(request):
    """
    List walks, or create a new walks.
    """

    if request.method == 'GET':
        walks = Walk.objects.filter(user=request.user).order_by("-date")
        serializer = WalkSerializer(walks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WalkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
