/** @odoo-module **/

import {Field} from "@web/views/fields/field"
import {patch} from "@web/core/utils/patch";
import {fieldVisualFeedback} from "@web/views/fields/field";
import {evaluateBooleanExpr} from "@web/core/py_js/py";
import {getClassNameFromDecoration} from "@web/views/utils";

function checkValue(value) {
    return (value === false || value === null || value === undefined || value === '' || Number.isNaN(value));

}

patch(Field.prototype, {
    get classNames() {
        const {class: _class, fieldInfo, name, record} = this.props;
        const {readonly, required, invalid, empty} = fieldVisualFeedback(
            this.field,
            record,
            name,
            fieldInfo || {}
        );
        const classNames = {
            o_field_widget: true,
            o_readonly_modifier: readonly,
            o_required_modifier: required,
            o_field_invalid: invalid,
            o_field_empty: empty,
            [`o_field_${this.type}`]: true,
            [_class]: Boolean(_class),
            o_empty: checkValue(record.data[name])
        };
        if (this.field.additionalClasses) {
            for (const cls of this.field.additionalClasses) {
                classNames[cls] = true;
            }
        }

        // generate field decorations classNames (only if field-specific decorations
        // have been defined in an attribute, e.g. decoration-danger="other_field = 5")
        // only handle the text-decoration.
        if (fieldInfo && fieldInfo.decorations) {
            const {decorations} = fieldInfo;
            for (const decoName in decorations) {
                const value = evaluateBooleanExpr(
                    decorations[decoName],
                    record.evalContextWithVirtualIds
                );
                classNames[getClassNameFromDecoration(decoName)] = value;
            }
        }

        return classNames;
    }
})