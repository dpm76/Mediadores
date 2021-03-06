# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.core.serializers import json
from django.forms.widgets import HiddenInput
from django.http import HttpResponseBadRequest, HttpResponseRedirect, \
    HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from django.template.loader import get_template
from django.utils.simplejson import dumps
from mediadores import settings
from mediadores.emailusernames.utils import get_user
from mediadores.main.forms import RequestForm, ContactForm, SearchForm, \
    getMediatorForm, EntitiesFormset, ExpertiseAreaFormset, DegreeFormset, \
    InstitutionSelectForm, ResetPasswordForm, MediatorForm2, UserConfigForm, \
    PasswordChangeForm, SelectAndContactForm
from mediadores.main.models import Mediator, Request, Institution, ExpertiseArea, \
    InsuranceEntity, Degree, InstitutionAdmin
from mediadores.main.search import search
from mediadores.recaptcha.client import captcha

def home(request):
    
    try:
        user = request.user
        profile = user.get_profile()
    except:
        profile = None
        
    if (profile != None):
        #TODO Comprobar el tipo mediante método del perfil y no con try-except
        try:
            admin = profile.institutionadmin
        except:
            admin = None
            
        try:
            mediator = profile.mediator
        except:
            mediator = None
                   
        if admin != None:
            response = home_admin(request)
        elif mediator != None:
            response = home_mediator(request)
        else:
            raise Exception(u"Perfil no válido")
    else:
        response = home_general(request)
        
    return response

def home_general(request):
    
    """
    if request.method=="POST":
        institutionSelectionForm = InstitutionSelectForm(request.POST)
        if institutionSelectionForm.is_valid():
            institution = institutionSelectionForm.cleaned_data["institution"]
            return HttpResponseRedirect("/{instutionId}/".format(instutionId = institution.id))
    else:
        institutionSelectionForm = InstitutionSelectForm()
    """
        
    institutions = Institution.objects.all()
        
    return render_to_response("main/institution-selection.html",
                          {"institutions": institutions},
                          context_instance=RequestContext(request))

def home_general_institution(request, institutionId):

    try:    
        institution = Institution.objects.get(id=institutionId)
        
        searchForm = SearchForm()
        searchForm.fields["nif"].widget = HiddenInput()
    
        return render_to_response("main/home_general.html",
                              {"searchForm": searchForm,
                               "institution": institution},
                              context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect("/") 

@login_required
def home_admin(request):
    iadmin = request.user.get_profile().institutionadmin
    if request.method == "POST":
        searchForm=SearchForm(request.POST)
        params = searchForm.getSearchParams(iadmin.institution)
        if params:
            mediators = search(params, False).order_by("nif")
        else:
            mediators = iadmin.institution.mediator_set.order_by("nif").all()
    else:        
        mediators = iadmin.institution.mediator_set.order_by("nif").all()
        searchForm=SearchForm()
        
    return render_to_response("main/home_admin.html",
                              {'searchForm': searchForm,
                               'mediators': mediators,
                               'institution': iadmin.institution,
                               },
                              context_instance=RequestContext(request))

@login_required
def home_mediator(request):
    
    try:
        mediator = request.user.get_profile().mediator
    except:
        return HttpResponseForbidden()
    
    dataUpdated = False
    
    if request.method == "POST":
        mediatorForm = MediatorForm2(request.POST, instance=mediator)
        if mediatorForm.is_valid():
            mediatorForm.save()
            dataUpdated = True
    else:
        mediatorForm = MediatorForm2(instance=mediator)
    
    return render_to_response("main/home_mediator.html",
                              {"mediatorForm":mediatorForm,
                               "mediator": mediator,
                               "dataUpdated": dataUpdated,
                               "institution": mediator.getFirstInstitution()},
                              context_instance=RequestContext(request))

def mediators_list(request, institutionId):
    
    institution = Institution.objects.get(id=institutionId)

    if request.method=="POST":
        searchForm = SearchForm(request.POST)        
        searchParams = searchForm.getSearchParams(institution)
        
        if searchParams:
            mediatorsList = search(searchParams)
            
            response = render_to_response("main/mediators_list.html",
                              {'mediators': mediatorsList,
                               'institution': searchParams.institution},
                              context_instance=RequestContext(request))
        else:
            response = render_to_response("main/home_general.html",
                              {"searchForm": searchForm,
                               "institution": institution},
                              context_instance=RequestContext(request))            
        
    else:
        response = HttpResponseBadRequest()
        
    return response
    
def do_request(request, institutionId, mediatorNif):
    
    captchaResponse = ""
    captchaVerified = request.user and request.user.is_authenticated() 
    sent = error = False
    institution = Institution.objects.get(id=institutionId)
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        
        if not captchaVerified:
            response = captcha.submit(
                                      request.POST.get('recaptcha_challenge_field'),
                                      request.POST.get('recaptcha_response_field'),
                                      settings.RECAPTCHA_PRI_KEY,
                                      request.META['REMOTE_ADDR'],)
            
            captchaVerified = response.is_valid
                                    
        if captchaVerified:
            captchaResponse = ""
            if form.is_valid():
                mediatorRequest = form.save(True)
                #Enviar correo con la petición a: Usuario, InstitutionAdmin y a Mediator
                #Si se necesita host dinámico puede ser util la biblioteca smtplib
                
                #Envío a solicitante
                message = get_template("main/confirm-mediator-request.txt").render(Context({"request": mediatorRequest}))
                    
                send_mail(u"Confirmación de petición de mediación",
                          message,
                          mediatorRequest.institution.contactEMail,
                          [mediatorRequest.requester_email])

                #Envío a mediador
                message = get_template("main/mediator-request-to-mediator.txt").render(Context({"request": mediatorRequest}))
                    
                send_mail(u"Aviso de petición de mediación",
                          message,
                          mediatorRequest.institution.contactEMail,
                          [mediatorRequest.mediator.email])

                #Envío a administración
                message = get_template("main/mediator-request-to-admin.txt").render(Context({"request": mediatorRequest}))
                
                iadmins = mediatorRequest.institution.institutionadmin_set.filter(canReceiveEMails=True)
                emails = [mediatorRequest.institution.contactEMail]
                for iadmin in iadmins:
                    emails.append(iadmin.email)
                    
                send_mail(u"Entrada de petición de mediación",
                          message,
                          mediatorRequest.institution.contactEMail,
                          emails)
                
                sent = True
                
        else:
            captchaResponse = u"Palabras incorrectas"
                                  
    else:
        mediatorRequest = Request()
        mediatorRequest.mediator = Mediator.objects.get(nif=mediatorNif)
        mediatorRequest.institution = institution
                
        form = RequestForm(instance=mediatorRequest)
    
    return render_to_response("main/request.html",
                          {"requestForm": form,
                           "institution":institution,
                           "captchaResponse": captchaResponse,
                           "captchaVerified": captchaVerified,
                           "sent": sent,
                           "error": error},
                          context_instance=RequestContext(request))

def info(request, institutionId):
    institution = Institution.objects.get(id=institutionId)
    institutionSet = None
    isMediator = False
    
    if request.user.is_authenticated():
        try:
            mediator = request.user.get_profile().mediator
            institutionSet = mediator.institution.order_by("name")
            isMediator = True
        except:
            pass 
    
    if institutionSet:
        if request.method=="POST":
            institutionSelectionForm = InstitutionSelectForm(request.POST)
            if institutionSelectionForm.is_valid():
                return HttpResponseRedirect("/info/%d/"%(institutionSelectionForm.cleaned_data["institution"].id))
                
        else:
            institutionSelectionForm = InstitutionSelectForm(initial={"institution": Institution.objects.get(id = institutionId)})
        institutionSelectionForm.fields["institution"].queryset = institutionSet
    else:
        institutionSelectionForm = None 
    
    return render_to_response("main/info.html",
                              {"institution": institution,
                               "isMediator": isMediator,
                               "institutionSelectionForm": institutionSelectionForm},
                              context_instance=RequestContext(request))

def sendEMailContact(institution, senderEMail, name, surname, subject, content):

    iadmins = institution.institutionadmin_set.filter(canReceiveEMails = True)
    emails=[institution.contactEMail]
    for iadmin in iadmins:
        emails.append(iadmin.email)
                
                
    # Envío de confirmación
    message = get_template("main/confirm-contact-email.txt").render(Context({
                                "content": content,
                                "institution": institution.name}))
                    
    send_mail(u"Confirmación: " + subject,
                              message,
                              institution.contactEMail,
                              [senderEMail])
                    
    # Envío a los administradores
    message = get_template("main/contact-email.txt").render(Context({
                                "name":name,
                                "surname":surname,
                                "content":content}))
                    
    send_mail(subject,
                message,
                senderEMail,
                emails)


def contact(request, institutionId):
    
    if request.user.is_authenticated():
        try:
            mediator = request.user.get_profile().mediator
            if mediator:
                return selectAndContact(request)
        except:
            pass
    
    captchaResponse = ""
    captchaVerified = request.user and request.user.is_authenticated()
    sent = False
    error = False
    institution = Institution.objects.get(id=institutionId)
    
    if request.method == 'POST':
        contactForm = ContactForm(request.POST)
        
        if not captchaVerified:
            response = captcha.submit(
                                  request.POST.get('recaptcha_challenge_field'),
                                  request.POST.get('recaptcha_response_field'),
                                  settings.RECAPTCHA_PRI_KEY,
                                  request.META['REMOTE_ADDR'],)
            captchaVerified = response.is_valid
                                
        if captchaVerified:
            captchaResponse = ""
            if contactForm.is_valid():
                
                try:    
                    senderEMail=contactForm.cleaned_data["senderEMail"]
                    name=contactForm.cleaned_data["name"]
                    surname=contactForm.cleaned_data["surname"]
                    subject=contactForm.cleaned_data["subject"]
                    content=contactForm.cleaned_data["content"]
                    sendEMailContact(institution, senderEMail, name, surname, subject, content)
                    sent = True
                except Exception:
                    error = True
                    raise
        else:
            captchaResponse = u"Palabras incorrectas"
            
    else:
        contactForm = ContactForm()
    
    return render_to_response("main/contact.html",
                              {"contactForm": contactForm,
                               "captchaResponse": captchaResponse,
                               "captchaVerified": captchaVerified,
                               "institution": institution,
                               "sent": sent,
                               "error": error},
                          context_instance=RequestContext(request))

@login_required
def selectAndContact(request):
    
    sent=False
    error=False
    
    mediator = request.user.get_profile().mediator
    institutionList = mediator.institution.order_by("name")   
    
    if request.method == "POST":
        contactForm = SelectAndContactForm(request.POST, initial={'institution':institutionList[0].id})
        contactForm.fields['institution'].queryset = institutionList
        if contactForm.is_valid():
            try:
                institution=contactForm.cleaned_data["institution"]
                senderEMail=request.user.email
                name=mediator.name
                surname=mediator.surname
                subject=contactForm.cleaned_data["subject"]
                content=contactForm.cleaned_data["content"]
                sendEMailContact(institution, senderEMail, name, surname, subject, content)
                sent = True
            except:
                error = True
                raise
    else:    
        contactForm = SelectAndContactForm(initial={'institution':institutionList[0].id})        
        contactForm.fields['institution'].queryset = institutionList
    
                                                
    return render_to_response("main/contact.html",
                              {"contactForm": contactForm,                                                              
                               "captchaVerified": True,                               
                               "sent": sent,
                               "error": error},
                                context_instance=RequestContext(request))
                        
@login_required    
def editMediator(request, mediatorId):
    #TODO Comprobar que el usuario es iadmin, o el mediador es el usuario
    mediator = get_object_or_404(Mediator, id = mediatorId)

    profile = request.user.get_profile()
    if profile.getClassName() == InstitutionAdmin.__name__:
        institution = profile.institutionadmin.institution
        if not institution in mediator.institution.all():
            mediator.institution.add(institution)
            mediator.save()
    else:
        institution = None

    if request.method=="POST":
            
        mediatorForm=getMediatorForm(post=request.POST, files=request.FILES, instance=mediator, hideNif=False)
        if mediatorForm.is_valid():
            mediatorForm.save()
            response=HttpResponseRedirect("/")
        else:
            response = render_to_response("main/edit_mediator.html",
                                          {"mediatorForm": mediatorForm,
                                           "institution": institution},
                                          context_instance=RequestContext(request))
                
    else:
        mediatorForm=getMediatorForm(instance=mediator, hideNif=False)
        response = render_to_response("main/edit_mediator.html",
                                      {"mediatorForm": mediatorForm,
                                       "institution": institution},
                                      context_instance=RequestContext(request))
    
    return response

@login_required
def deleteMediator(request, mediatorId):
    try:
        institution = request.user.get_profile().institutionadmin.institution
        mediator=Mediator.objects.get(id=mediatorId)
        if mediator:
            #Sólo se da de baja de la institución. Si no quedan instituciones, entonces se borra
            if institution in mediator.institution.all():
                if len(mediator.institution.all()) > 1:
                    mediator.institution.remove(institution)
                else:
                    mediator.delete()
    except:
        pass
    
    return HttpResponseRedirect("/")

#@login_required
def addMediator(request):
    #TODO comprobar que el usuario es institutionandmin
    institution = request.user.get_profile().institutionadmin.institution
    if request.method == 'POST':
        mediatorForm = getMediatorForm(post=request.POST, files=request.FILES, hideNif=False)
        if mediatorForm.is_valid():

            mediator=mediatorForm.save()
            mediator.institution.add(institution)
            mediator.save()
                       
            response = HttpResponseRedirect("/")
        else:
            response = render_to_response("main/add_mediator.html",
                                          {"mediatorForm": mediatorForm,
                                           "institution": institution},
                                          context_instance=RequestContext(request))
            
    else:
        mediatorForm = getMediatorForm(hideNif=False)
        response = render_to_response("main/add_mediator.html",
                                          {"mediatorForm": mediatorForm,
                                           "institution": institution},
                                          context_instance=RequestContext(request))
    
    return response

@login_required
def insuranceEntities(request):
    institution = request.user.get_profile().institutionadmin.institution
    q = InsuranceEntity.objects.order_by("name")
    if request.method=="POST":
        entitiesFormset= EntitiesFormset(request.POST)
        if entitiesFormset.is_valid():
            entitiesFormset.save()
            response = HttpResponseRedirect("/")
        else:
            response = render_to_response("main/insurance_entities.html",
                              {"entitiesFormset": entitiesFormset,
                               "institution":institution},
                              context_instance=RequestContext(request))
    else:
        entitiesFormset = EntitiesFormset(queryset=q)
        response = render_to_response("main/insurance_entities.html",
                              {"entitiesFormset": entitiesFormset,
                               "institution":institution},
                              context_instance=RequestContext(request))
        
    return response

@login_required
def areas(request):
    institution = request.user.get_profile().institutionadmin.institution
    q = ExpertiseArea.objects.order_by("name")
    if request.method=="POST":
        formset= ExpertiseAreaFormset(request.POST)
        if formset.is_valid():
            formset.save()
            response = HttpResponseRedirect("/")
        else:
            response = render_to_response("main/areas.html",
                              {"formset": formset,
                               "institution":institution},
                              context_instance=RequestContext(request))
    else:
        formset = ExpertiseAreaFormset(queryset=q)
        response = render_to_response("main/areas.html",
                              {"formset": formset,
                               "institution":institution},
                              context_instance=RequestContext(request))
        
    return response

@login_required
def degrees(request):
    institution=request.user.get_profile().institutionadmin.institution
    q = Degree.objects.order_by("name")
    if request.method=="POST":
        formset= DegreeFormset(request.POST)
        if formset.is_valid():
            formset.save()
            response = HttpResponseRedirect("/")
        else:
            response = render_to_response("main/degrees.html",
                              {"formset": formset,
                               "institution":institution},
                              context_instance=RequestContext(request))
    else:
        formset = DegreeFormset(queryset=q)
        response = render_to_response("main/degrees.html",
                              {"formset": formset,
                               "institution":institution},
                              context_instance=RequestContext(request))
        
    return response

def legal(request):
    return render_to_response("main/legal.html", context_instance=RequestContext(request))

def resetPassword(request):
    done=False
    if request.method=="POST":
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if email != "":
                user = get_user(email)
                if user:
                    try:
                        profile = user.get_profile()
                    except:
                        profile = None
                    
                    try:
                        profile.institutionadmin.resetPassword()
                        done=True
                    except:
                        pass
                    
                    try:
                        profile.mediator.resetPassword()
                        done=True
                    except:
                        pass
                    
    else:
        form = ResetPasswordForm()
    return render_to_response("main/reset-password.html",
                              {"form":form,
                               "done":done},
                              context_instance=RequestContext(request))

@login_required
def userconfig(request):
    
    done = False
    user = request.user
    try:    
        profile = user.get_profile()
    except:
        return HttpResponseForbidden(u"No autorizado")
    
    isInstitutionAdmin = profile.getClassName() == InstitutionAdmin.__name__
    if isInstitutionAdmin:
        institution = profile.institutionadmin.institution
    else:
        institution = profile.mediator.getFirstInstitution()
     
    initialData = {"name": profile.name, "surname": profile.surname, "email": user.email}
    if request.method=="POST":
        if isInstitutionAdmin:
            userConfigForm=UserConfigForm(request.POST, initial=initialData)
            userConfigForm.setCurrentUser(user)
        else:
            userConfigForm = None
            
        passwordChangeForm=PasswordChangeForm(request.POST)
        if (not isInstitutionAdmin or userConfigForm.is_valid()) and passwordChangeForm.is_valid():
            if isInstitutionAdmin and userConfigForm.has_changed():
                profile.name = userConfigForm.cleaned_data['name']
                profile.surname = userConfigForm.cleaned_data['surname']
                profile.email = userConfigForm.cleaned_data['email']
                profile.save()
            password = passwordChangeForm.cleaned_data["password"]
            if password:
                user.set_password(password)
                user.save()
            done=True
            
    else:
        if isInstitutionAdmin:
            userConfigForm=UserConfigForm(initial=initialData)
        else:
            userConfigForm = None
        passwordChangeForm=PasswordChangeForm()
    
    return render_to_response("main/userconfig.html",
                              {"userConfigForm":userConfigForm,
                               "passwordChangeForm":passwordChangeForm,
                               "done":done,
                               "institution":institution},
                              context_instance=RequestContext(request))

@login_required
def addExpertiseArea(request):
    response = {}
    if request.method=="POST":
        name = request.POST["data"]
        if ExpertiseArea.objects.filter(name=name).exists():
            response["status"] = -1
            response["error"] = u"Ya existe el área '%s'"%(name)
        else:
            area = ExpertiseArea(name=name)
            area.save()
            response["status"] = 0
            response["value"]=area.id
            response["text"]=name
    else:
        return HttpResponseBadRequest()
    
    return HttpResponse(dumps(response))

@login_required
def addDegree(request):
    response = {}
    if request.method=="POST":
        name = request.POST["data"]
        if Degree.objects.filter(name=name).exists():
            response["status"] = -1
            response["error"] = u"Ya existe la titulación '%s'"%(name)
        else:
            degree = Degree(name=name)
            degree.save()
            response["status"] = 0
            response["value"]=degree.id
            response["text"]=name
    else:
        return HttpResponseBadRequest()
    
    return HttpResponse(json.simplejson.dumps(response))

@login_required
def getNifList(request):
    if request.is_ajax():
        nifList = []

        nifStart = request.POST.get("nif-start","")
        if nifStart:
            q = Mediator.objects.filter(nif__startswith=nifStart)        
            for m in q:
                nifList.append(m.nif)
                
        return HttpResponse(dumps(nifList))
    
    else:
        return HttpResponseForbidden()

@login_required
def getMediator(request):
    try:
        if request.is_ajax():
            data=""
            nif = request.POST.get("nif", "")
            if nif:
                data = serializers.serialize("json", Mediator.objects.filter(nif=nif))
                                
            return HttpResponse(data)            
            
        else:
            return HttpResponseForbidden()
    except Exception as ex:
        return HttpResponse(str(ex))
