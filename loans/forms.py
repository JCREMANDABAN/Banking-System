from django import forms
from .models import Loan

class LoanApplyForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ('account', 'amount', 'interest_rate', 'term_months')
        widgets = {
            'account': forms.Select(attrs={'class': 'form-select'}),
            'term_months': forms.NumberInput(attrs={'min': 1}),
        }
