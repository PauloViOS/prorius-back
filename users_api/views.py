from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileRegisterSerializer, ProfileLoginSerializer, ProfileSerializer
from rest_framework import permissions, status


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


class ProfileDelete(APIView):
	permission_classes = (permissions.IsAuthenticated, )
	authentication_classes = (SessionAuthentication,)

	def delete(self, request):
		profile_email = request.data.get('email', None)
		profile = Profile.objects.get(email=profile_email)

		profile.is_deleted = True
		profile.save()

		return Response({'status': status.HTTP_204_NO_CONTENT})


class ProfileUpdate(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def put(self, request):
		try:
			profile_email = request.query_params.get('email', None)
			profile_instance = Profile.objects.get(email=profile_email)

			name = request.data.get('name', None)
			if name:
				profile_instance.name = name
				profile_instance.save()

			username = request.data.get('username', None)
			if username:
				profile_instance.username = username
				profile_instance.save()

			email = request.data.get('email', None)
			if email:
				profile_instance.email = email
				profile_instance.save()

			password = request.data.get('password', None)
			if password:
				profile_instance.password = password
				profile_instance.save()

			return Response({'status': status.HTTP_200_OK})
		except Exception as e:
			return Response({'message': e, 'status': status.HTTP_400_BAD_REQUEST})

