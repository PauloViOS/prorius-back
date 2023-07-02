from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError

ProfileModel = get_user_model()


class ProfileRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProfileModel
		fields = '__all__'

	def create(self, clean_data):
		profile_obj = ProfileModel.objects.create_user(
			email=clean_data['email'],
			username=clean_data['username'],
			name=clean_data['name'],
			password=clean_data['password']
		)
		profile_obj.save()
		return profile_obj


class ProfileLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()

	def check_profile(self, clean_data):
		profile = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not profile:
			raise ValidationError('User not found')
		return profile


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProfileModel
		fields = ('email', 'username', 'name')
