from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileRegisterSerializer, ProfileLoginSerializer, ProfileSerializer
from rest_framework import permissions, status
# TODO: from .validations import custom_validations


class ProfileRegister(APIView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		clean_data = request.data  # TODO: custom validation
		serializer = ProfileRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			profile = serializer.create(clean_data)
			if profile:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)

	def post(self, request):
		data = request.data
		# validate_email(data)
		# validate_password(password)
		serializer = ProfileLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			profile = serializer.check_profile(data)
			login(request, profile)
			return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileLogout(APIView):
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		serializer = ProfileSerializer(request.user)
		return Response({'profile': serializer.data, 'status': status.HTTP_200_OK})
