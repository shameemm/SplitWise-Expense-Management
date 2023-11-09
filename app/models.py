from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10)
    split_type = models.CharField(max_length=10)
    participants = models.ManyToManyField(User, related_name='particiants')
    
    def __str__(self):
        return f'Expense of {self.amount} by {self.user}'
    
class Balance(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance_from')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance_to')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.user1} owes {self.user2}: {self.amount}'