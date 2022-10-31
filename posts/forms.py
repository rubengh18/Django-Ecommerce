from ckeditor.widgets import CKEditorWidget
from posts.models import Article
from django import forms
from django.forms.fields import ImageField
from ckeditor.fields import RichTextField, RichTextFormField
from django.forms.models import ModelForm



class FormArticle(forms.ModelForm):
    class Meta:
        model= Article
        fields=["titulo", "descripcion", "image","image2","image3", "categories", "talla", "precio", "clase", "tipo"]
        widgets={
            
            'titulo':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Título'
                }
            ),
            'descripcion':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Descripción'
                }
            ),
            
            'categories':forms.Select(
               attrs={
                    'class':'form-select', 
                    "selected":""
                }
            ),
            'talla':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'talla'
                }
            ),
            'precio':forms.TextInput(
               attrs={
                    'class':'form-control',
                    'placeholder': 'Precio',
                    'type': 'tel',
                    'input': 'mode'
                }
            ),
            'tipo':forms.Select(
               attrs={
                    'class':'form-select', 
                    "list":"inputGroupSelect01",
                    "placeholder":"Escoja"
                }
            ),
            'clase':forms.Select(
               attrs={
                    'class':'form-select', 
                    "list":"inputGroupSelect02"
                }
            ),

        }

class FormEdit(forms.ModelForm):
    class Meta:
        model= Article
        fields=["image","image2","image3","titulo", "descripcion",  "categories", "talla", "precio", "clase", "tipo"]
        widgets={
            
            'image':forms.FileInput(
                attrs={
                    'class':'btn-file',
                   
                }
            ),
            'image2':forms.FileInput(
                attrs={
                    'class':'btn-file',
                    
                }
            ),
            'image3':forms.FileInput(
                attrs={
                    'class':'btn-file',
                    
                }
            ),
            'titulo':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Título'
                }
            ),
            'descripcion':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Descripción'
                }
            ),
            
            'categories':forms.Select(
               attrs={
                    'class':'form-select', 
                    "selected":""
                }
            ),
            'talla':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'talla'
                }
            ),
            'precio':forms.TextInput(
               attrs={
                    'class':'form-control',
                    'placeholder': 'Precio',
                    'type': 'tel',
                    'input': 'mode'
                }
            ),
            'tipo':forms.Select(
               attrs={
                    'class':'form-select', 
                    "list":"inputGroupSelect01",
                    "placeholder":"Escoja"
                }
            ),
            'clase':forms.Select(
               attrs={
                    'class':'form-select', 
                    "list":"inputGroupSelect02"
                }
            ),

        }