/** @odoo-module **/

import { useCommand } from "@web/core/commands/command_hook";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState } from "@odoo/owl";
import { localization } from "@web/core/l10n/localization";
import { usePopover } from "@web/core/popover/popover_hook";

class KeypadFloatPopOver extends Component {
}
KeypadFloatPopOver.template = "keypad_float.KeypadFloatPopOver";

export class KeypadFloat extends Component {
    static template = "keypad_float.KeypadFloat";
    static props = {
        ...standardFieldProps,
        withCommand: { type: Boolean, optional: true },
        autosave: { type: Boolean, optional: true },
    };

    setup() {
        super.setup();
        this.maxLength = 16;
        this.state = useState({
            index: String(this.value),
        });
        const position = localization.direction === "rtl" ? "bottom" : "top";
        this.popover = usePopover(KeypadFloatPopOver, { position });
    }


    onKeyClick(ev) {
        this.popover.open(ev.currentTarget, {
            record: this.props.record,
            widget: this,
        });
    }

    async setNum(num) {
        let new_num = String(num);
        let str = this.state.index;
        if (new_num === "del" && str.length > 0) {
          str = str.substring(0, str.length - 1);
        } else if (new_num !== "del" && str.length < this.maxLength) {
          str = str + new_num;
        }
        let res = String(parseInt(str)?parseInt(str):0)
        this.props.record.update({ [this.props.name]: res});
        this.state.index = res;
    }

    get value() {
        return this.props.record.data[this.props.name];
    }
}

export const keypadFloat = {
    component: KeypadFloat,
    displayName: _t("Priority"),
    supportedOptions: [
        {
            label: _t("Autosave"),
            name: "autosave",
            type: "boolean",
            default: true,
            help: _t(
                "If checked, the record will be saved immediately when the field is modified."
            ),
        },
    ],
    supportedTypes: ["char"],
    extractProps({ options, viewType }, dynamicInfo) {
        return {
            withCommand: viewType === "form",
            readonly: dynamicInfo.readonly,
            autosave: "autosave" in options ? !!options.autosave : true,
        };
    },
};

registry.category("fields").add("keypad_float", keypadFloat);
