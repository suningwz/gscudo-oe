odoo.define('rewo_banner', function (require) {
    "use strict";
    const { Component } = owl;
    const { xml } = owl.tags

    class RewoBanner extends Component {
        static template = xml`
        <div class="bg-info text-center p-2">
        <b> Welcome to Gruppo Scudo </b>
        </div>`
    }



    // owl.utils.whenReady().then(() => {
    //     const app = new RewoBanner();
    //     app.mount(document.body);
    // });

}
);