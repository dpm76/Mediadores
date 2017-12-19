
/* gettext library */

var catalog = new Array();

function pluralidx(n) {
  var v=(n != 1);
  if (typeof(v) == 'boolean') {
    return v ? 1 : 0;
  } else {
    return v;
  }
}
catalog['%(sel)s of %(cnt)s selected'] = ['',''];
catalog['%(sel)s of %(cnt)s selected'][0] = 'one: %(sel)s de %(cnt)s seleccionado';
catalog['%(sel)s of %(cnt)s selected'][1] = 'other: %(sel)s de  %(cnt)s seleccionados';
catalog['6 a.m.'] = '6 a.m.';
catalog['Add'] = 'Agregar';
catalog['Available %s'] = '%s Disponibles';
catalog['Calendar'] = 'Calendario';
catalog['Cancel'] = 'Cancelar';
catalog['Choose a time'] = 'Elige una hora';
catalog['Choose all'] = 'Selecciona todos';
catalog['Chosen %s'] = '%s Elegidos';
catalog['Clear all'] = 'Elimina todos';
catalog['Clock'] = 'Reloj';
catalog['Hide'] = 'Esconder';
catalog['January February March April May June July August September October November December'] = 'Enero Febrero Marzo Abril Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre';
catalog['Midnight'] = 'Medianoche';
catalog['Noon'] = 'Mediod\u00eda';
catalog['Now'] = 'Ahora';
catalog['Remove'] = 'Remover';
catalog['S M T W T F S'] = 'D L M M J V S';
catalog['Select your choice(s) and click '] = 'Haz tus elecciones y da click en ';
catalog['Show'] = 'Mostrar';
catalog['Sunday Monday Tuesday Wednesday Thursday Friday Saturday'] = 'Domingo Lunes Martes Mi\u00e9rcoles Jueves Viernes S\u00e1bado';
catalog['Today'] = 'Hoy';
catalog['Tomorrow'] = 'Ma\u00f1ana';
catalog['Yesterday'] = 'Ayer';
catalog['You have selected an action, and you haven\'t made any changes on individual fields. You\'re probably looking for the Go button rather than the Save button.'] = 'Has seleccionado una acci\u00f3n y no has hecho ning\u00fan cambio en campos individuales. Probablemente est\u00e9s buscando el bot\u00f3n Ejecutar en lugar del bot\u00f3n Guardar.';
catalog['You have selected an action, but you haven\'t saved your changes to individual fields yet. Please click OK to save. You\'ll need to re-run the action.'] = 'Has seleccionado una acci\u00f3n, pero no has guardado los cambios en los campos individuales todav\u00eda. Pulsa OK para guardar. Tendr\u00e1s que volver a ejecutar la acci\u00f3n.';
catalog['You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost.'] = 'Tienes cambios sin guardar en campos editables individuales. Si ejecutas una acci\u00f3n, los cambios no guardados se perder\u00e1n.';


function gettext(msgid) {
  var value = catalog[msgid];
  if (typeof(value) == 'undefined') {
    return msgid;
  } else {
    return (typeof(value) == 'string') ? value : value[0];
  }
}

function ngettext(singular, plural, count) {
  value = catalog[singular];
  if (typeof(value) == 'undefined') {
    return (count == 1) ? singular : plural;
  } else {
    return value[pluralidx(count)];
  }
}

function gettext_noop(msgid) { return msgid; }

function pgettext(context, msgid) {
  var value = gettext(context + '' + msgid);
  if (value.indexOf('') != -1) {
    value = msgid;
  }
  return value;
}

function npgettext(context, singular, plural, count) {
  var value = ngettext(context + '' + singular, context + '' + plural, count);
  if (value.indexOf('') != -1) {
    value = ngettext(singular, plural, count);
  }
  return value;
}

function interpolate(fmt, obj, named) {
  if (named) {
    return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
  } else {
    return fmt.replace(/%s/g, function(match){return String(obj.shift())});
  }
}

/* formatting library */

var formats = new Array();

formats['DATETIME_FORMAT'] = 'j \\de F \\de Y \\a \\l\\a\\s H:i';
formats['DATE_FORMAT'] = 'j \\de F \\de Y';
formats['DECIMAL_SEPARATOR'] = ',';
formats['MONTH_DAY_FORMAT'] = 'j \\de F';
formats['NUMBER_GROUPING'] = '3';
formats['TIME_FORMAT'] = 'H:i:s';
formats['FIRST_DAY_OF_WEEK'] = '1';
formats['TIME_INPUT_FORMATS'] = ['%H:%M:%S', '%H:%M'];
formats['THOUSAND_SEPARATOR'] = '.';
formats['DATE_INPUT_FORMATS'] = ['%d/%m/%Y', '%d/%m/%y'];
formats['YEAR_MONTH_FORMAT'] = 'F \\de Y';
formats['SHORT_DATE_FORMAT'] = 'd/m/Y';
formats['SHORT_DATETIME_FORMAT'] = 'd/m/Y H:i';
formats['DATETIME_INPUT_FORMATS'] = ['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M'];

function get_format(format_type) {
    var value = formats[format_type];
    if (typeof(value) == 'undefined') {
      return msgid;
    } else {
      return value;
    }
}
