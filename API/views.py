from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import MyModel
from .serializers import MyModelSerializer


@api_view(['GET', 'POST'])
def students_list(request):
    if request.method == 'GET':
        data = MyModel.objects.all()

        serializer = MyModelSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MyModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
