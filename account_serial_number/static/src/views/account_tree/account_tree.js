/** @odoo-module **/

import {
    AccountMoveUploadListView,
    AccountMoveListController,
    AccountMoveUploadListRenderer
} from "@account/components/bills_upload/bills_upload"
import {serialNumberListRenderer} from "@web_list_serial_number/views/list/list_renderer"
import {useState} from "@odoo/owl";

export class forceAccountMoveListController extends AccountMoveListController {
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
forceAccountMoveListController.template = `web_list_serial_number.ListView`;

export class forceAccountMoveUploadListRenderer extends AccountMoveUploadListRenderer {
    setup() {
        super.setup();

        if (this.isX2Many) {
            this.serialNumber = {
                numSwitch: false
            }
        } else {
            this.serialNumber = this.props.serialNumber || {};
        }
    }
}
forceAccountMoveUploadListRenderer.recordRowTemplate = "web_list_serial_number.ListRenderer.RecordRow";
forceAccountMoveUploadListRenderer.rowsTemplate = "web_list_serial_number.ListRenderer.Rows";
forceAccountMoveUploadListRenderer.props = serialNumberListRenderer.props;

AccountMoveUploadListView.Controller = forceAccountMoveListController
AccountMoveUploadListView.Renderer = forceAccountMoveUploadListRenderer