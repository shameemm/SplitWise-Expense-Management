from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Balance, Expense
from .serializers import BalanceSerializer,ExpenseSerializer,UserSerializer
from rest_framework import status
from .task import send_mail_task
from rest_framework.response import Response
# Create your views here.

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
class ExpenseListView(APIView):
    def post(self, request):
        user_id = request.data.get('user')
        amount = request.data.get('amount')
        expense_type = request.data.get('type')
        split_type = request.data.get('split_type')
        participants_ids = request.data.get('participants', [])
        
        try:
            payer = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        participants = []
        for participant_id in participants_ids:
            try:
                participant = User.objects.get(id=participant_id)
                participants.append(participant)
            except User.DoesNotExist:
                return Response({'error': f'User with ID {participant_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        expense = Expense.objects.create(user_id=user_id,amount=amount,type = expense_type,split_type=split_type)  
        expense.save()
        for participant in participants:
            expense.participants.add(participant)  

        
        serializer = ExpenseSerializer(expense)
        if split_type == 'EQUAL':
            share = amount / (len(participants) + 1)
            for participant in participants:
                Balance.objects.create(user1=participant, user2=payer, amount=share)
                send_mail_task('Splitwise Remainder',f'you have to pay amount of {share} to {payer}.',[participant.email] )
        elif split_type == 'EXACT':
            for participant in participants:
                owes = request.data['owes'].get(str(participant.id), 0)
                Balance.objects.create(user1=participant, user2=payer, amount=owes)
                send_mail_task('Splitwise Remainder',f'you have to pay amount of {owes} to {payer}.',[participant.email] )
        elif split_type == 'PERCENT':
            total_percent = sum(request.data['percent'].values())
            if total_percent != 100:
                return Response({'error': 'Total percent must be 100'}, status=status.HTTP_400_BAD_REQUEST)

            for participant in participants:
                percent = request.data['percent'].get(str(participant.id), 0)
                owes = (percent / 100) * amount
                Balance.objects.create(user1=participant, user2=payer, amount=owes)
                send_mail_task('Splitwise Remainder',f'you have to pay amount of {owes} to {payer}.',[participant.email] )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
class BalanceListView(APIView):
    def get(self, request):
        balances = Balance.objects.filter(amount__gt=0)
        serializer = BalanceSerializer(balances, many=True)
        return Response(serializer.data)