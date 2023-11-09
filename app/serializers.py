from rest_framework import serializers
from .models import User, Expense, Balance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','mobile_number']
        
class ExpenseSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    
    class Meta:
        model = Expense
        fields = ['id','user','amount','type','split_type', 'participants']
        
class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id','user1','user2','amount']