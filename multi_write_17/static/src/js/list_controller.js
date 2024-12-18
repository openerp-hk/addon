odoo.define('multi_write.ListController', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Sidebar = require('web.Sidebar');
    var _t = core._t;

    ListController.include({
        renderSidebar: function ($node) {
            var self = this;
            if (this.hasSidebar) {
                var other = [{
                    label: _t("Export"),
                    callback: this._onExportData.bind(this)
                }, {
                    label: _t("批量修改"),
                    callback: function() {
                        var context = self.model.get(self.handle, {create: false}).getContext();
                        context['multi_write'] = true;
                        context['multi_write_ids'] = self.getSelectedIds();
                        context['multi_write_model'] = self.modelName;
                        self.do_action({
                            context: context,
                            type: 'ir.actions.act_window',
                            views: [[false, 'form']],
                            res_model: self.modelName,
                            res_id: self.getSelectedIds()[0],
                            flags: {mode: 'edit'},
                            target: 'new'
                        }, {
                            on_close: function () {
                                self.reload();
                            }
                        });
                    },
                }];

                if (this.archiveEnabled) {
                    other.push({
                        label: _t("Archive"),
                        callback: function () {
                            Dialog.confirm(self, _t("Are you sure that you want to archive all the selected records?"), {
                                confirm_callback: self._onToggleArchiveState.bind(self, true),
                            });
                        }
                    });
                    other.push({
                        label: _t("Unarchive"),
                        callback: this._onToggleArchiveState.bind(this, false)
                    });
                }
                if (this.is_action_enabled('delete')) {
                    other.push({
                        label: _t('Delete'),
                        callback: this._onDeleteSelectedRecords.bind(this)
                    });
                }
                this.sidebar = new Sidebar(this, {
                    editable: this.is_action_enabled('edit'),
                    env: {
                        context: this.model.get(this.handle, {raw: true}).getContext(),
                        activeIds: this.getSelectedIds(),
                        model: this.modelName,
                    },
                    actions: _.extend(this.toolbarActions, {other: other}),
                });
                this.sidebar.appendTo($node);

                this._toggleSidebar();
            }
        },
    });
});