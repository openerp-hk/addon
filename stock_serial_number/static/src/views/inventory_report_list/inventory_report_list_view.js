/** @odoo-module */

import {InventoryReportListController} from "@stock/views/list/inventory_report_list_controller"
import {InventoryReportListView} from "@stock/views/list/inventory_report_list_view"
import {serialNumberListRenderer} from "@web_list_serial_number/views/list/list_renderer"
import {useState} from "@odoo/owl";
import {
    forcePurchaseDashBoardRenderer
} from "../../../../../purchase_serial_number/static/src/views/purchase_dashboard_list/purchase_list_view";

export class forceInventoryReportListController extends InventoryReportListController {
    setup() {
        super.setup(...arguments);
        this.serialNumber = useState({
            displayNumSwitch: true,
            numSwitch: !!localStorage.getItem(this.env.config.viewId.toString())
        })
    }

    onNumSwitch() {
        this.serialNumber.numSwitch = !this.serialNumber.numSwitch;
        localStorage.setItem(this.env.config.viewId.toString(), this.serialNumber.numSwitch);
    }

}

forceInventoryReportListController.template = `web_list_serial_number.ListView`;
InventoryReportListView.Renderer = serialNumberListRenderer;
InventoryReportListView.Controller = forceInventoryReportListController;

