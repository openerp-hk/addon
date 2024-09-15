/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";

export class serialNumberListRenderer extends ListRenderer{
    setup(){
        super.setup();

        if (this.isX2Many){
            this.serialNumber = {
                numSwitch: false
            }
        }else{
            this.serialNumber = this.props.serialNumber || {};
        }
    }
}

serialNumberListRenderer.template = "web_list_serial_number.ListRenderer";
serialNumberListRenderer.rowsTemplate = "web_list_serial_number.ListRenderer.Rows";
serialNumberListRenderer.recordRowTemplate = "web_list_serial_number.ListRenderer.RecordRow";
serialNumberListRenderer.props = [
    "activeActions?",
    "list",
    "archInfo",
    "openRecord",
    "evalViewModifier",
    "onAdd?",
    "cycleOnTab?",
    "allowSelectors?",
    "editable?",
    "onOpenFormView?",
    "noContentHelp?",
    "nestedKeyOptionalFieldsData?",
    "onOptionalFieldsChanged?",
    "serialNumber?"
];