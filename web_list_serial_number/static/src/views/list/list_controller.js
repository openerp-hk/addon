/** @odoo-module **/

import {ListController} from "@web/views/list/list_controller";
import {useState} from "@odoo/owl";

export class serialNumberListController extends ListController{
    setup(){
        super.setup(...arguments);
        this.serialNumber = useState({
            displayNumSwitch: true,
            numSwitch: !!localStorage.getItem(this.env.config.viewId.toString())
        })
    }

    onNumSwitch(){
      this.serialNumber.numSwitch = !this.serialNumber.numSwitch;
      localStorage.setItem(this.env.config.viewId.toString(), this.serialNumber.numSwitch);
    }
}

serialNumberListController.template = `web_list_serial_number.ListView`;