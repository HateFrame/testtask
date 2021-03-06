from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers
from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=63, min_length=6, write_only=True)
    location = PointField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'image', 'gender', 'password', 'location']
        extra_kwargs = {
            "username": {
                "error_messages": {
                    'null': 'User should have a username',
                    'blank': 'User should have a username'
                }
            },
            "email": {
                "error_messages": {
                    'null': 'User should have a email',
                    'blank': 'User should have a email'
                }
            }
        }

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'Username should contains only nums or letters'
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MatchSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    partner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    def create(self, validated_data):
        user = validated_data.get('user')
        partner = validated_data.get('partner')
        user.likes.add(partner)
        return user

    def validate(self, attrs):
        user = attrs.get('user')
        partner = attrs.get('partner')

        if user == partner:
            raise serializers.ValidationError('You can not like or yourself')
        if user.likes.filter(pk=partner.pk).exists():
            raise serializers.ValidationError('You liked this user already')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'location']
