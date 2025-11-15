from django.contrib import admin
from .models import User, Client, LoanApplication, Loan, Transaction, AuditLog, Notification

admin.site.register(User)
admin.site.register(Client)
admin.site.register(LoanApplication)
admin.site.register(Loan)
admin.site.register(Transaction)
admin.site.register(AuditLog)
admin.site.register(Notification)