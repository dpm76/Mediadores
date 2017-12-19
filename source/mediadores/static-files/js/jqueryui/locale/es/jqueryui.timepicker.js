jQuery(function($){
	$.timepicker.regional['es'] = { // Spanish regional settings
			currentText: 'Ahora',
			closeText: 'Hecho',
			ampm: false,
			amNames: ['AM', 'A'],
			pmNames: ['PM', 'P'],
			timeFormat: 'hh:mm tt',
			timeSuffix: '',
			timeOnlyTitle: 'Selecci&oacute;n de hora',
			timeText: '',
			hourText: 'Hora',
			minuteText: 'Minuto',
			secondText: 'Segundo',
			millisecText: 'Milisegundo',
			timezoneText: 'Zona horaria'
		};
	$.timepicker.setDefaults($.timepicker.regional['es']);
});
