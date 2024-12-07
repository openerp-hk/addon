/** @odoo-module **/

import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";


patch(NavBar.prototype, {
    getSystemLogo(){
        const root = this.menuService.getMenu('root');
        return root.system_logo ? 'data:image/png;base64,' + root.system_logo: '/openerphk_theme/static/src/img/system logo.png'
    }
})