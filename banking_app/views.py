from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from twilio.rest import Client as TwilioClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
from .models import User, Client, LoanApplication, Loan, Transaction, AuditLog, Notification
from .forms import LoanApplicationForm, TransactionForm

# Helper: Check roles
def is_admin(user):
    return user.role == 'admin'

def is_staff(user):
    return user.role == 'staff'

# Authentication
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            AuditLog.objects.create(user=user, action='Logged in')
            return redirect('profile')
        messages.error(request, 'Invalid credentials')
    return render(request, 'banking_app/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        User.objects.create_user(username=username, password=password, role=role)
        messages.success(request, 'User registered')
        return redirect('login')
    return render(request, 'banking_app/register.html')

@login_required
def logout_view(request):
    AuditLog.objects.create(user=request.user, action='Logged out')
    logout(request)
    return redirect('login')

# Client Profile
@login_required
def profile_view(request):
    client = get_object_or_404(Client, user=request.user)
    transactions = Transaction.objects.filter(client=client)
    return render(request, 'banking_app/client_profile.html', {'client': client, 'transactions': transactions})

# Loan Application
@login_required
def loan_application_view(request):
    client = get_object_or_404(Client, user=request.user)
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.client = client
            # Eligibility: Income > 2x amount, credit > 600
            if client.income > 2 * app.amount and client.credit_score > 600:
                app.status = 'pending'
                app.save()
                AuditLog.objects.create(user=request.user, action=f'Applied for loan: {app.amount}')
                messages.success(request, 'Application submitted')
            else:
                messages.error(request, 'Not eligible')
    else:
        form = LoanApplicationForm()
    return render(request, 'banking_app/loan_application.html', {'form': form})

# Loan Approval (Staff)
@user_passes_test(is_staff)
def loan_approval_view(request, app_id):
    app = get_object_or_404(LoanApplication, id=app_id)
    if request.method == 'POST':
        if 'approve' in request.POST:
            app.status = 'approved'
            app.approval_date = timezone.now()
            app.save()
            Loan.objects.create(application=app, amortization_schedule=json.dumps({'schedule': 'Generated'}))  # Simplified
            Notification.objects.create(client=app.client, type='approval', message='Loan approved')
            AuditLog.objects.create(user=request.user, action=f'Approved loan for {app.client.name}')
        else:
            app.status = 'rejected'
            app.save()
    return render(request, 'banking_app/loan_approval.html', {'app': app})

# Disbursement/Repayment
@login_required
def disbursement_view(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    # Simulate disbursement
    messages.success(request, 'Funds disbursed')
    return render(request, 'banking_app/loan_disbursement.html', {'loan': loan})

@login_required
def repayment_view(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        Transaction.objects.create(client=loan.application.client, type='payment', amount=amount, balance=0)  # Update balance
        Notification.objects.create(client=loan.application.client, type='reminder', message='Payment received')
        AuditLog.objects.create(user=request.user, action=f'Payment made: {amount}')
    return render(request, 'banking_app/repayment.html', {'loan': loan})

# Savings
@login_required
def savings_view(request):
    client = get_object_or_404(Client, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.client = client
            txn.balance = client.income + txn.amount if txn.type == 'deposit' else client.income - txn.amount  # Simplified
            txn.save()
            AuditLog.objects.create(user=request.user, action=f'{txn.type}: {txn.amount}')
    else:
        form = TransactionForm()
    return render(request, 'banking_app/savings.html', {'form': form, 'balance': client.income})

# Reports
@user_passes_test(is_admin)
def reports_view(request):
    loans = Loan.objects.all()
    if 'export_pdf' in request.GET:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 750, 'Loan Report')
        for loan in loans:
            p.drawString(100, 730, f'Loan ID: {loan.id}')
        p.showPage()
        p.save()
        return response
    return render(request, 'banking_app/reports.html', {'loans': loans})

# Audit Logs
@user_passes_test(is_admin)
def audit_logs_view(request):
    logs = AuditLog.objects.all()
    return render(request, 'banking_app/audit_logs.html', {'logs': logs})