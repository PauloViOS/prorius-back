from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileRegisterSerializer, ProfileLoginSerializer, ProfileSerializer, ProfileUpdateSerializer
from rest_framework import permissions, status


class ProfileRegister(APIView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		clean_data = request.data
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
		serializer = ProfileLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			profile = serializer.check_profile(data)
			if profile.is_deleted:
				return Response(status=status.HTTP_404_NOT_FOUND)
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
	permission_classes = (permissions.IsAuthenticated,)
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
		serializer = ProfileUpdateSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		validated_data = serializer.validated_data

		try:
			profile_instance = Profile.objects.get(email=validated_data['current_email'])

			if validated_data.get('name'):
				profile_instance.name = validated_data['name']

			if validated_data.get('username'):
				username_already_exists = Profile.objects.filter(username=validated_data['username']).exists()
				if username_already_exists:
					raise Exception('Nome de usuário não disponível')
				profile_instance.username = validated_data['username']

			if validated_data.get('email'):
				email_already_exists = Profile.objects.filter(email=validated_data['email']).exists()
				if email_already_exists:
					raise Exception('Email não disponível')
				profile_instance.email = validated_data['email']

			profile_instance.save()

			return Response({'status': status.HTTP_200_OK})
		except Exception as e:
			return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
