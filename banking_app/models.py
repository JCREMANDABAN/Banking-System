from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('staff', 'Loan Officer'),
        ('borrower', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='borrower')
    is_active = models.BooleanField(default=True)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    address = models.TextField()
    income = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.IntegerField()
    doc_uploads = models.FileField(upload_to='docs/', blank=True)

class LoanApplication(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_months = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    submitted_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)

class Loan(models.Model):
    application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE)
    disbursement_date = models.DateTimeField(auto_now_add=True)
    amortization_schedule = models.JSONField()  # Store as JSON

class Transaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('payment', 'Loan Payment')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)