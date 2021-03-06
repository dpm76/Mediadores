# -*- coding: utf-8 -*-
'''
Created on 19/12/2012

@author: David
'''
INSTITUTION_TYPES = (
                     ("CA", u"Cámara de Comercio"),
                     )

PROVINCES_SET = (
                 ("01", u"Álava"),
                 ("02", u"Albacete"),
                 ("03", u"Alicante"),
                 ("04", u"Almería"),
                 ("05", u"Ávila"),
                 ("06", u"Badajoz"),
                 ("07", u"Baleares (Illes)"),
                 ("08", u"Barcelona"),
                 ("09", u"Burgos"),
                 ("10", u"Cáceres"),
                 ("11", u"Cádiz"),
                 ("12", u"Castellón"),
                 ("13", u"Ciudad Real"),
                 ("14", u"Córdoba"),
                 ("15", u"A Coruña"),
                 ("16", u"Cuenca"),
                 ("17", u"Girona"),
                 ("18", u"Granada"),
                 ("19", u"Guadalajara"),
                 ("20", u"Guipúzcoa"),
                 ("21", u"Huelva"),
                 ("22", u"Huesca"),
                 ("23", u"Jaén"),
                 ("24", u"León"),
                 ("25", u"Lleida"),
                 ("26", u"La Rioja"),
                 ("27", u"Lugo"),
                 ("28", u"Madrid"),
                 ("29", u"Málaga"),
                 ("30", u"Murcia"),
                 ("31", u"Navarra"),
                 ("32", u"Ourense"),
                 ("33", u"Asturias"),
                 ("34", u"Palencia"),
                 ("35", u"Las Palmas"),
                 ("36", u"Pontevedra"),
                 ("37", u"Salamanca"),
                 ("38", u"Santa Cruz de Tenerife"),
                 ("39", u"Cantabria"),
                 ("40", u"Segovia"),
                 ("41", u"Sevilla"),
                 ("42", u"Soria"),
                 ("43", u"Tarragona"),
                 ("44", u"Teruel"),  
                 ("45", u"Toledo"),
                 ("46", u"Valencia"),
                 ("47", u"Valladolid"),
                 ("48", u"Vizcaya"),
                 ("49", u"Zamora"),
                 ("50", u"Zaragoza"),
                 ("51", u"Ceuta"),
                 ("52", u"Melilla"),                            
            )

PROVINCES_MAP = {}
for x,y in PROVINCES_SET:
    PROVINCES_MAP[x] = y

MEDIATION_MODE = (
                    ("0", u"A instancia de ambas partes"),
                    ("1", u"A petición de una parte con pacto de sometimiento a mediación"),
                    ("2", u"A petición de una sola parte"),
                  )
