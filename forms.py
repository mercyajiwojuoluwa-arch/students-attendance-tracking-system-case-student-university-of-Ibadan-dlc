from django import forms
from .models import Session
class SessionForm(forms.ModelForm):
 class Meta:
  model=Session
  fields=['course','date','topic']
  widgets={'date':forms.DateInput(attrs={'type':'date'})}
 def __init__(self,*args,user=None,**kwargs):
  super().__init__(*args,**kwargs)
  if user and not user.is_superuser: self.fields['course'].queryset=self.fields['course'].queryset.filter(lecturer=user)
