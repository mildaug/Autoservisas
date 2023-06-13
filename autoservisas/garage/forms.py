from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = models.OrderReview
        fields = ('content', 'order', 'reviewer')
        widgets = {
            'order': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }


class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ('car', 'date', 'due_back', 'status')
        widgets = {
            'car': forms.HiddenInput(),
            'date': DateInput(),
            'due_back': DateInput(),
            'status': forms.HiddenInput(),
        }
        