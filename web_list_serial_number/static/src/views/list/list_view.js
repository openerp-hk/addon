/** @odoo-module */

import { registry } from "@web/core/registry";
import { serialNumberListController } from "./list_controller";
import { serialNumberListRenderer } from "./list_renderer";
import { listView } from "@web/views/list/list_view";

export const serialNumberListView = {
    ...listView,
    Controller: serialNumberListController,
    Renderer: serialNumberListRenderer,
}

registry.category("views").add("serialNumberListView", serialNumberListView);