// static/src/js/custom_owl_component.js
/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
console.log("Componente OWL ADADADAD", Component);

export class CustomOwlComponent extends Component {
  // static template = xml`<div>Hello Owl</div>`;
  static template = "prova4.CustomOwlComponent";

  setup() {
    console.log("Componente OWL inizializzato");
  }

  get recordName() {
    return this.props.record.data.name || "Nessun nome";
  }

  onClick() {
    alert("Pulsante cliccato!");
  }
}

// CustomOwlComponent.template = xml`<div>Hello Owl</div>`;
// CustomOwlComponent.template = "your_module_name.CustomOwlComponent";
// export default CustomOwlComponent;
