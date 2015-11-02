__author__ = 'xueqing'
from rest_framework import serializers
from company.models import Company

class CompanySerializer(serializers.ModelSerializer):
    create_user_username = serializers.StringRelatedField(source='create_user')
    class Meta:
        model = Company
        fields =('id','create_time','create_user','write_time','write_user','name','create_user_username','address',
                 'website','inside_description','is_customer','is_supplier','is_available')
