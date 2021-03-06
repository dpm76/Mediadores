# -*- coding: utf-8 -*-
'''
Created on 12/02/2013

@author: David
'''
from django.db.models.query_utils import Q
import datetime

class FilterParams(object):

    institution = None
    nif = None
    name = None
    expertiseKeywords = None
    expertiseAreas = None
    degrees = None

def search(filterParams, onlyActive=True):
    
    if filterParams.nif:
        q = filterParams.institution.mediator_set.filter(nif=filterParams.nif)
    else:
        q = filterParams.institution.mediator_set.all()
        if filterParams.name and filterParams.name.strip():
            words = filterParams.name.strip().split()
            exp=u"({0}".format(words[0])
            words.remove(words[0])            
            for word in words:
                exp += u"|{0}".format(word)
            exp += u")"
            q = q.filter(Q(name__iregex=exp) | Q(surname__iregex=exp))
            
        if filterParams.expertiseKeywords and filterParams.expertiseKeywords.strip():
            words = filterParams.expertiseKeywords.strip().split()
            exp=u"({0})".format(words[0])
            words.remove(words[0])            
            for word in words:
                exp += u"*({0})".format(word)
                
            q = q.filter(expertiseDescription__iregex=exp)
        
        if filterParams.degrees:
            q = q.filter(degree__in=filterParams.degrees)
        
        if filterParams.expertiseAreas:
            q = q.filter(expertiseArea__in=filterParams.expertiseAreas)

        if onlyActive:
            q = q.filter(insuranceExpiration__gte=datetime.datetime.today());
            
    return q.distinct()
