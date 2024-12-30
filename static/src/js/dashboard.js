odoo.define('GEMA.contracts_dashboard', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.contractsDashboard = publicWidget.Widget.extend({
        selector: '.contracts-dashboard',  // Debe coincidir con el selector de tu plantilla
        xmlDependencies: ['/GEMA/views/dashboard.xml'],  // Ruta correcta de la plantilla
        events: {
            'input #contractSearch': '_onSearchInput',  // Filtro de búsqueda
        },

        init: function (parent, options) {
            this._super.apply(this, arguments);
            console.log('Contracts Dashboard Widget Initialized');
        },

        _onSearchInput: function (ev) {
            console.log('HOLA')
            var searchTerm = ev.target.value.toLowerCase();
            var cards = document.querySelectorAll('.card');
            cards.forEach(function(card) {
                var contractName = card.querySelector('.card-title').textContent.toLowerCase();
                if (contractName.includes(searchTerm)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        },

    });

});
