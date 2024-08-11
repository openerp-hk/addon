/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";

import { Component, useState } from "@odoo/owl";

export class StockPickingListController extends ListController {
    setup() {
        super.setup();
    }
};

StockPickingListController.components = {
    ...ListController.components,
};

export const StockPickingListView = {
    ...listView,
    Controller: StockPickingListController,
};

registry.category("views").add("stock_header_search", StockPickingListView);
