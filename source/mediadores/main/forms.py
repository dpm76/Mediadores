# -*- coding: utf-8 -*-
'''
Created on 06/02/2013

@author: David
'''
from django import forms
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.forms.models import ModelForm, modelformset_factory
from mediadores.emailusernames.utils import user_exists, get_user
from mediadores.main.image_widget import AdminImageWidget
from mediadores.main.models import Request, Degree, ExpertiseArea, Institution, \
    Mediator, InsuranceEntity
from mediadores.main.search import FilterParams

class RequestForm(ModelForm):    
    required_css_class="required"
    
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['amount'].localize = True
    
    class Meta:
        model=Request
        widgets={
                    'mediator': forms.HiddenInput,
                    'institution': forms.HiddenInput,
                    'requester_address_street': forms.Textarea(attrs={'cols': 80, 'rows':2}),
                 }

class InstitutionSelectForm(Form):
    
    institution=forms.ModelChoiceField(label=u"Institución", queryset=Institution.objects.order_by("name"), required=True)

class ContactForm(Form):
    
    required_css_class="required"
    
    name=forms.CharField(label=u"Nombre", required=True)
    surname=forms.CharField(label=u"Apellidos", required=True)
    senderEMail = forms.EmailField(label=u"e-Mail", required=True)
    subject = forms.CharField(label=u"Asunto", required=True)
    content = forms.CharField(label=u"Texto", widget=forms.Textarea, required=True)

class SelectAndContactForm(Form):
    required_css_class = "required"
    
    institution=forms.ModelChoiceField(label=u"Institución", required=True, queryset=None)
    subject = forms.CharField(label=u"Asunto", required=True)
    content = forms.CharField(label=u"Texto", widget=forms.Textarea, required=True)        

class SearchForm(Form):

    required_css_class="required"
    
    nif=forms.CharField(label=u"NIF o DNI", required=False)
    name=forms.CharField(label=u"Nombre y Apellidos", required=False, help_text=u"Si conoce el nombre y apellidos de un mediador, puede introducirlos aquí.")
    expertiseKeywords=forms.CharField(label=u"Etiquetas", required=False, help_text=u"Introducza palabras de búsqueda relacionadas con el mediador buscado.<br>Por ejemplo: \"relaciones laborales\"")
    expertiseAreas=forms.ModelMultipleChoiceField(label=u"Área de experiencia", required=False, queryset=ExpertiseArea.objects.all().order_by("name"), help_text=u"Se buscarán los mediadores que tengan al menos una de las áreas seleccionadas")
    degree=forms.ModelMultipleChoiceField(label=u"Titulación académica", required=False, queryset=Degree.objects.all().order_by("name"), help_text=u"Se buscarán los mediadores que tengan al menos una de las titulaciones seleccionadas")

    def getSearchParams(self, institution):
        
        if self.is_valid():        
            params = FilterParams()
            params.institution = institution
            params.nif = self.cleaned_data["nif"]
            params.degrees = self.cleaned_data["degree"]
            params.expertiseAreas=self.cleaned_data["expertiseAreas"]
            params.name=self.cleaned_data["name"]
            params.expertiseKeywords=self.cleaned_data["expertiseKeywords"]
            
        else:
            params=None
            
        return params

class MediatorForm(ModelForm):
    required_css_class="required"

    class Meta:
        model=Mediator
        fields = ('nif', 'institution', 'isCompany', 'name', 'surname', 'image', 'email', 'address',
                   'postalCode', 'city', 'province', 'phoneNumber', 'mobileNumber', 
                   'faxNumber', 'website', 'expertiseArea', 'degree',
                   'expertiseDescription', 'description', 'insuranceEntity',
                   'insuranceContract', 'insuranceExpiration')
        exclude=('institution')
        widgets={
                 'image':AdminImageWidget, 
                 }
        
    def clean(self):
        cleaned_data = super(MediatorForm, self).clean()
        phoneNumber = cleaned_data.get("phoneNumber")
        mobileNumber = cleaned_data.get("mobileNumber")
        if not phoneNumber and not mobileNumber:
            raise forms.ValidationError(u"No se ha proporcionado número de teléfono fijo ni número de teléfono móvil. Se debe proporcionar uno por lo menos.")
        
        if cleaned_data.get('isCompany'):
            cleaned_data['surname'] = ""            
        
        return cleaned_data
            

def getMediatorForm(instance=None, post=None, files=None, hideNif=True):
    
    form = MediatorForm(post, files, instance=instance)
    
    form.fields['degree'].queryset=Degree.objects.order_by('name')
    form.fields['degree'].help_text=""
    form.fields['expertiseArea'].queryset=ExpertiseArea.objects.order_by('name')
    form.fields['expertiseArea'].help_text=""
    form.fields['insuranceEntity'].queryset=InsuranceEntity.objects.order_by('name')
    
    if hideNif:
        form.fields['nif'].widget=forms.HiddenInput()
    
    return form

class EntityForm(ModelForm):
    required_css_class="required"
    class Meta:
        model=InsuranceEntity

EntitiesFormset = modelformset_factory(InsuranceEntity, can_delete=True, form=EntityForm)
        
ExpertiseAreaFormset = modelformset_factory(ExpertiseArea, can_delete=True, extra= 4)

DegreeFormset = modelformset_factory(Degree, can_delete=True, extra= 4)

class ResetPasswordForm(Form):
    required_css_class="required"

    email=forms.EmailField(label=u"e-mail", max_length=75, required=False)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if email: 
            if not user_exists(email):
                raise forms.ValidationError(u"No existe el usuario")
            try:
                get_user(email).get_profile()
            except:
                raise forms.ValidationError(u"Este usuario es especial y no se puede cambiar la contraseña aquí")
        return email

class MediatorForm2(MediatorForm):

    class Meta:
        model=Mediator
        fields = ('nif', 'institution', 'isCompany', 'name', 'surname', 'image', 'email', 'address',
                   'postalCode', 'city', 'province', 'phoneNumber', 'mobileNumber', 
                   'faxNumber', 'website', 'expertiseArea', 'degree',
                   'expertiseDescription', 'description', 'insuranceEntity',
                   'insuranceContract', 'insuranceExpiration')
        exclude=('institution', 'isCompany', 'insuranceEntity', 'insuranceContract', 'insuranceExpiration',
                 'expertiseArea', 'degree')
        widgets={
                 'image':AdminImageWidget, 
                 }

class PasswordChangeForm(Form):
    password=forms.CharField(label=u"Contraseña", widget=forms.PasswordInput(render_value=True), required=False)
    password2=forms.CharField(label=u"Confirmación de contraseña", widget=forms.PasswordInput(render_value=True), help_text=u"Por favor, repita la contraseña para asegurarse de que la ha introducido correctamemte.", required=False)
    
    def clean_password2(self):
        passwd1 = self.cleaned_data["password"]
        passwd2 = self.cleaned_data["password2"]
        if passwd1:
            if not passwd2:
                raise forms.ValidationError(u"Este campo es obligatorio.")
            if passwd1 != passwd2:
                raise forms.ValidationError(u"Las contraseñas no coinciden.")
        
        return passwd2

class UserConfigForm(Form):
    name=forms.CharField(label=u"Nombre", max_length=64, required=False)
    surname=forms.CharField(label=u"Apellidos", max_length=128, required=False)
    email=forms.EmailField(label=u"e-mail", max_length=75, required=False)
    
    def setCurrentUser(self, currentUser):
        self.currentUser = currentUser
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if email and user_exists(email, queryset=User.objects.exclude(pk=self.currentUser.pk)):
            raise forms.ValidationError(u"Dirección de correo electrónico no válida. Introduzca otra.")
    
        return email
 
            
            