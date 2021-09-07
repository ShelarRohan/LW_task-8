
from django import forms
from .models import Image

# forms.py
from django import forms
from .models import *

class CarForm(forms.ModelForm):

	class Meta:
		model = Image
		fields = ['Name', 'image']
		widgets = {
                'Name':forms.TextInput(attrs={'class':'input1',"type": "text","placeholder": "Enter Your Name "})
		}
