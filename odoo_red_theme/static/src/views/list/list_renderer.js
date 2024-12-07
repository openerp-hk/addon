/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {ListRenderer} from "@web/views/list/list_renderer";
import {useEffect, useExternalListener} from "@odoo/owl";


patch(ListRenderer.prototype, {
    setup() {
        super.setup();
        useEffect((tableRef) => {
            this.adaptiveColumnWidth()
        });

        useExternalListener(window, "resize", ()=>{
            this.adaptiveColumnWidth()
        });
    },

    adaptiveColumnWidth() {
        const table = this.tableRef.el;
        const headers = [...table.querySelectorAll("thead th")];
        headers.forEach((th, index) => {
            const text = th.querySelector('.text-truncate');
            if (text && text.innerText) {
                const _text = text.cloneNode(true);
                const fullWidth = this.getFullWidth(_text);
                const {width} = th.getBoundingClientRect();
                if (fullWidth >= Math.floor(width) || th.style.width.includes('%')) {
                    th.style.width = fullWidth + 'px';
                    th.style.maxWidth = fullWidth + 'px';
                }
            }
            if (!!!this.props.list.count && Array.from(th.classList).includes('o_list_controller')) {
                th.style.width = '30px'
            }
        });
    },

    getFullWidth(el) {
        el.style.position = 'absolute';
        el.style.zIndex = -1;
        document.body.appendChild(el);
        const width = el.offsetWidth;
        document.body.removeChild(el);
        return width + 40;
    }
})