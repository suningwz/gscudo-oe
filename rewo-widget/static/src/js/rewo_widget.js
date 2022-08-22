odoo.define('rewo_widget', function (require) {
    "use strict";
    const { Component } = owl;
    const AbstractField = require('web.AbstractFieldOwl');
    const fieldRegistry = require('web.field_registry_owl');


    class RewoDial extends Component {
        static template = 'OWLFieldDial';
        dialClicked() {
            alert("dialing ...");

        }
    }
    class FieldDial extends AbstractField {
        static supportedFieldTypes = ['integer'];
        static template = 'OWLFieldDial';
        static components = { RewoDial };

        constructor(...args) {
            super(...args);
            this.dial = new RewoDial();
        }
        async willStart() {
            this.num2dial = {};


        }
    }
    fieldRegistry.add('rewo_dial', FieldDial);
    
    return {
        FieldDial: FieldDial,
    };
});