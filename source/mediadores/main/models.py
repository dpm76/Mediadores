# -*- coding: utf-8 -*-
from PIL import Image
from datetime import date
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.context import Context
from django.template.loader import get_template
from mediadores.emailusernames.utils import create_user
from mediadores.main.enums import PROVINCES_SET, INSTITUTION_TYPES, \
    MEDIATION_MODE, PROVINCES_MAP
from mediadores.settings import MEDIA_ROOT, SITE_URL_ROOT
from os import remove
from os.path import join, exists
import random
import string

class Institution(models.Model):
    name=models.CharField(verbose_name=u"denominación", max_length=128, blank=False)
    address=models.CharField(verbose_name=u"dirección", max_length=128, blank=False)
    postalcode=models.CharField(verbose_name=u"código postal", max_length=5, blank=False)
    city=models.CharField(verbose_name=u"población", max_length=64, blank=False)
    website=models.URLField(verbose_name=u"sitio web", null=True, blank=True)
    phone=models.CharField(verbose_name=u"teléfono", max_length=16, default="-")
    fax=models.CharField(verbose_name=u"fax", max_length=16, null=True, blank=True)
    logo=models.ImageField(verbose_name=u"logotipo", upload_to="images", null=True, blank=True)
    institutionType=models.CharField(verbose_name=u"tipo de institución", max_length=2, blank=False, choices=INSTITUTION_TYPES)
    province=models.CharField(verbose_name=u"provincia", max_length=2, blank=False, choices=PROVINCES_SET)
    contactEMail=models.EmailField(verbose_name=u"e-mail de contacto", blank=False)
    mapIframe=models.TextField(verbose_name=u"código del mapa", null=True, blank=True, help_text=u"Código HTML que genera Google Maps para añadir un mapa en un sitio web.")
    mapX=models.IntegerField(verbose_name=u"coodernada X", default=0, help_text=u"Coodenada para de la imagen del mapa de selección inicial")
    mapY=models.IntegerField(verbose_name=u"coodernada Y", default=0, help_text=u"Coodenada para de la imagen del mapa de selección inicial")
    
    def __unicode__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    name=models.CharField(verbose_name=u"nombre", max_length=64, blank=False)
    surname=models.CharField(verbose_name=u"apellidos", max_length=128, blank=True)
    email=models.EmailField(verbose_name=u"e-Mail", max_length=75, unique=True)

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self.mustSendCreationEMail = False

    def __unicode__(self):
        return unicode.format(u"{0} {1}", self.name, self.surname)
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        
        if not self.id or self.id == 0:
            #Crear password aleatorio
            self.passwd = self.createPassword()
            user = create_user(self.email, self.passwd)
            self.user = user
            self.mustSendCreationEMail = True           
        else: #ya existe el usuario
            user = self.user
            user.email = self.email
            user.save()      
        super(UserProfile, self).save(*args, **kwargs)
        
        if self.mustSendCreationEMail:
            # enviar correo al usuario con su password
            self.sendCreationEMail(self.passwd)
        
    def delete(self, *args, **kwargs):
        user = self.user
        super(UserProfile, self).delete(*args, **kwargs)
        user.delete()
    
    def createPassword(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(8))
    
    def resetPassword(self):
        self.passwd = self.createPassword()
        self.user.set_password(self.passwd)
        self.sendPasswordResetEMail(self.passwd)
    
    def sendCreationEMail(self, passwd):
        raise Exception(u"No se puede enviar correo desde la clase base.")
    
    def sendPasswordResetEMail(self, passwd):
        raise Exception(u"No se puede enviar correo desde la clase base.")
    
    def getClassName(self):
        className = ""
        try:
            self.mediator
            className = Mediator.__name__
        except:
            pass
        try:
            self.institutionadmin
            className = InstitutionAdmin.__name__
        except:
            pass
            
        return className

class ExpertiseArea(models.Model):
    name=models.CharField(verbose_name="campo de experiencia", max_length=64, blank=False)
    
    def __unicode__(self):
        return self.name 

class Degree(models.Model):
        
    name=models.CharField(verbose_name=u"denominación", max_length=64, blank=False, unique=True)
    
    def __unicode__(self):
        return self.name

class InsuranceEntity(models.Model):
        
    name=models.CharField(verbose_name=u"entidad aseguradora", max_length=64, blank=False)
    eMail=models.EmailField(verbose_name=u"e-mail", blank=False)
    phone=models.CharField(verbose_name=u"teléfono", max_length=32, blank=True, null= True)
    address=models.CharField(verbose_name=u"dirección postal", max_length=128, blank=True, null=True)
    city=models.CharField(verbose_name=u"población", max_length=64, blank=True, null=True)
    postalCode=models.CharField(verbose_name=u"código postal", max_length=5, blank=True, null=True)
    province=models.CharField(verbose_name=u"provincia", max_length=2, blank=False, choices=PROVINCES_SET)

    def __unicode__(self):
        return self.name
    
    def provinceName(self):
        return PROVINCES_MAP[self.province]
        
class Mediator(UserProfile):
    nif=models.CharField(verbose_name=u"NIF", max_length=32, help_text=u"DNI o NIF", unique=True)
    institution = models.ManyToManyField(Institution, verbose_name=u"institución")
    address=models.CharField(verbose_name=u"dirección", max_length=128, blank=False)
    postalCode=models.CharField(verbose_name=u"código postal", max_length=5, blank=False)
    city=models.CharField(verbose_name=u"población", max_length=64, blank=False)
    province=models.CharField(verbose_name=u"provincia", max_length=2, blank=False, choices=PROVINCES_SET)
    phoneNumber=models.CharField(verbose_name=u"teléfono", max_length=16, blank=True, null=True)
    mobileNumber=models.CharField(verbose_name=u"tel. móvil", max_length=16, blank=True, null=True)
    faxNumber=models.CharField(verbose_name=u"fax", max_length=16, blank=True, null=True)    
    image=models.ImageField(verbose_name=u"imagen de perfil", upload_to="images/", null=True, blank=True)
    website=models.URLField(verbose_name=u"sitio web", null=True, blank=True)    
    degree=models.ManyToManyField(Degree, verbose_name=u"titulación")
    expertiseArea=models.ManyToManyField(ExpertiseArea, verbose_name=u"área de experiencia")
    description=models.TextField(verbose_name=u"resumen profesional", max_length=4096, help_text=u"Resumen de la experiencia profesional del mediador")    
    expertiseDescription=models.CharField(verbose_name=u"etiquetas", max_length=128, help_text=u"Palabras que definen el ámbito del mediador, separadas por espacios. Por ejemplo: \"tasador propiedad rural\"", blank=True, null=True)
    insuranceEntity=models.ForeignKey(InsuranceEntity, verbose_name=u"entidad aseguradora", blank=True, null=True)
    insuranceContract=models.CharField(verbose_name=u"número de póliza", max_length=32, blank=True, null=True)
    insuranceExpiration=models.DateField(verbose_name=u"expiración de la póliza", blank=True, null=True)
    isCompany=models.BooleanField(verbose_name=u"¿Es una sociedad?", default=False)

    def __unicode__(self):
        return unicode.format(u"{0}: {1} {2}", self.nif, self.name, self.surname)
    
    def provinceName(self):
        return PROVINCES_MAP[self.province]
    
    def hasInsurance(self):
        return self.insuranceEntity and self.insuranceContract and self.insuranceExpiration
    
    def isInsuranceExpired(self):
        return not self.insuranceExpiration or self.insuranceExpiration < date.today()
    
    def save(self, *args, **kwargs):
        imageFileName = join(self.image.field.upload_to, self.nif + ".jpg")
        imageFilePath = join(MEDIA_ROOT, imageFileName)
            
        super(Mediator, self).save(*args, **kwargs)
            
        if self.image.name:
            image = Image.open(self.image.path)
        
            image.thumbnail((100,75), Image.ANTIALIAS)
            image.save(imageFilePath, "JPEG")
            if self.image.name != imageFileName:
                remove(self.image.path)
            
            self.image = imageFileName
            super(Mediator, self).save(*args, **kwargs)
        else:
            if exists(imageFilePath):
                remove(imageFilePath)

    def delete(self, *args, **kwargs):
        super(Mediator,self).delete(*args, **kwargs)
        if self.image.name:
            remove(self.image.path)
    
    def getInstitutionSender(self):
        institutions = self.institution.all()
        if len(institutions) > 0:
            institution = institutions[0]
        else:
            institution = None
            
        return institution
        
    def sendCreationEMail(self, passwd):
        institution = self.getInstitutionSender()
        if institution:
            message = get_template("main/mediator-creation-notify.txt").render(Context({
                                       "mediator": self,
                                       "institution": institution,
                                       "passwd": passwd,
                                       "siteUrl" : SITE_URL_ROOT}))
             
            send_mail(u"Creación de usuario",
                      message,
                      institution.contactEMail,
                      [self.user.email])
            self.mustSendCreationEMail = False
            
    def sendPasswordResetEMail(self, passwd):
        institution = self.getInstitutionSender()
        if institution:
            message = get_template("main/password-reset-email.txt").render(Context({
                                       "userProfile": self,
                                       "institution": institution,
                                       "passwd": passwd}))
             
            send_mail(u"Reinicio de contraseña",
                      message,
                      institution.contactEMail,
                      [self.user.email])
    
    def getFirstInstitution(self):
        return self.institution.all()[0]
        
class InstitutionAdmin(UserProfile):
    institution = models.ForeignKey(Institution, verbose_name=u"institución")
    canReceiveEMails = models.BooleanField(verbose_name=u"recibe e-mails", default=True)
    
    def sendCreationEMail(self, passwd):
        
        message = get_template("main/iadmin-creation-notify.txt").render(Context({
                                   "iadmin": self,
                                   "passwd": passwd,
                                   "siteUrl" : SITE_URL_ROOT}))
         
        send_mail(u"Creación de usuario",
                  message,
                  self.institution.contactEMail,
                  [self.user.email])
        
    def sendPasswordResetEMail(self, passwd):
        
        if self.institution:
            message = get_template("main/password-reset-email.txt").render(Context({
                                       "userProfile": self,
                                       "institution": self.institution,
                                       "passwd": passwd}))
             
            send_mail(u"Reinicio de contraseña",
                      message,
                      self.institution.contactEMail,
                      [self.user.email])
      
class Request(models.Model):
    mediator=models.ForeignKey(Mediator, verbose_name=u"mediador")
    institution=models.ForeignKey(Institution, verbose_name=u"institución")
    requester_name=models.CharField(verbose_name=u"nombre", max_length=64)
    requester_surname=models.CharField(verbose_name=u"apellidos", max_length=128)
    requester_nif=models.CharField(verbose_name=u"nif o dni", max_length=32, db_index=True)
    requester_byself=models.BooleanField(verbose_name=u"en nombre propio", default=False)
    requester_representee=models.CharField(verbose_name=u"representado", max_length=256, blank=True, null=True, help_text=u"Rellenar sólo si se representa en nombre de una persona jurídica")
    requester_phone=models.CharField(verbose_name=u"teléfono fijo", max_length=32, blank=True, null=True)
    requester_mobile=models.CharField(verbose_name=u"teléfono móvil", max_length=32, blank=True, null=True)
    requester_fax=models.CharField(verbose_name=u"fax", max_length=32, blank=True, null=True)
    requester_email=models.EmailField(verbose_name=u"e-mail", max_length=64, blank=False)
    requester_address_street=models.CharField(verbose_name=u"dirección", max_length=128, help_text=u"Domicilio a efectos de notificación")
    requester_address_postalcode=models.CharField(verbose_name=u"código postal", max_length=8)
    requester_address_city=models.CharField(verbose_name=u"municipio", max_length=128, blank=True)
    requester_address_province=models.CharField(verbose_name=u"provincia", max_length=2, choices=PROVINCES_SET, blank=True, null=True)
    requester_party=models.CharField(verbose_name=u"parte solicitante", max_length=256)
    opponent_party=models.CharField(verbose_name=u"parte contraria", max_length=256)
    mediation_mode=models.CharField(verbose_name=u"mediación", max_length=1, choices=MEDIATION_MODE)
    purpose=models.TextField(verbose_name=u"motivo", max_length=2048, help_text=u"Breve descripción del objeto de la mediación")
    amount=models.FloatField(verbose_name=u"cuantía", default=0, help_text=u"En euros")
    timestamp=models.DateTimeField(verbose_name=u"fecha y hora", auto_now=True, help_text=u"Fecha y hora de realización")
    
    def __unicode__(self):
        return unicode.format(u"{0}| {1} -> {2} |{3}", self.timestamp, self.institution, self.mediator, self.requester_nif)

