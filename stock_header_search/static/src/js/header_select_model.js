/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import {DateSearch} from "./date_search";
import {patch} from "@web/core/utils/patch";
import { StockPickingListController } from "./stock_picking_list";
import {useState} from "@odoo/owl";

patch(ListController.prototype,{
    setup(){
        super.setup()
        this.state = useState({
            stock_date_search: false,
        });
    }
})

patch(StockPickingListController.prototype,{
    setup(){
        super.setup()
        this.state = useState({
            stock_date_search: true,
        });
    }
})

patch(StockPickingListController.components,Object.assign({}, ListController.components, {DateSearch}))