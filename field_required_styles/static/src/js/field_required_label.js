/* @odoo-module */

import {patch} from "@web/core/utils/patch";
import {Record} from "@web/model/relational_model/record";

patch(Record.prototype, {
    update(changes, {save} = {}) {
        if (this.model._urgentSave) {
            $('.o_wrap_field').each(function () {
                let $required_modifier = $(this).find('.o_required_modifier')
                if ($required_modifier.length > 0) {
                    let $label = $(this).find('label')
                    let field_name = $required_modifier.attr('name')
                    let is_key = field_name in changes
                    let field_value = changes[field_name]
                    var $input = $required_modifier.find('input');
                    if (is_key && field_value === false) {
                        $input.addClass('field_required_input');
                        if ($label.length > 0) {
                            $label.addClass('field_required_label')
                        }
                    } else if (is_key && field_value !== false) {
                        $input.removeClass('field_required_input');
                        if ($label.length > 0) {
                            $label.removeClass('field_required_label')
                        }
                    }
                }
            })
            return this._update(changes, {save: false}); // save is already scheduled
        }
        return this.model.mutex.exec(async () => {

            await this._update(changes, {withoutOnchange: save});
            $('.o_wrap_field').each(function () {
                let $required_modifier = $(this).find('.o_required_modifier')
                if ($required_modifier.length > 0) {
                    let $label = $(this).find('label')
                    let field_name = $required_modifier.attr('name')
                    let is_key = field_name in changes
                    let field_value = changes[field_name]
                    var $input = $required_modifier.find('input');
                    if (is_key && field_value === false) {
                        $input.addClass('field_required_input');
                        if ($label.length > 0) {
                            $label.addClass('field_required_label')
                        }
                    } else if (is_key && field_value !== false) {
                        $input.removeClass('field_required_input');
                        if ($label.length > 0) {
                            $label.removeClass('field_required_label')
                        }
                    }
                }
            })
            if (save) {
                return this._save();
            }
        });

    }
})