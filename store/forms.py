from django import forms
from . models import Product

#for add and edit product forms
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','image']
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            
        }