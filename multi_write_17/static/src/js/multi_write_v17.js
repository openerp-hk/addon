/* @odoo-module */
import {
    deleteConfirmationMessage,
    ConfirmationDialog,
} from "@web/core/confirmation_dialog/confirmation_dialog";
import {ListController} from "@web/views/list/list_controller";
import {viewService} from "@web/views/view_service";
import {patch} from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { UPDATE_METHODS } from "@web/core/orm_service";
import { registry } from "@web/core/registry";

patch(viewService, {
    start(env, { orm }) {
        let cache = {};

        function clearCache() {
            cache = {};
            const processedArchs = registry.category("__processed_archs__");
            processedArchs.content = {};
            processedArchs.trigger("UPDATE");
        }

        env.bus.addEventListener("CLEAR-CACHES", clearCache);
        env.bus.addEventListener("RPC:RESPONSE", (ev) => {
            const { model, method } = ev.detail.data.params;
            if (["ir.ui.view", "ir.filters"].includes(model)) {
                if (UPDATE_METHODS.includes(method)) {
                    clearCache();
                }
            }
        });
        async function loadViews(params, options = {}) {
            const { context, resModel, views } = params;
            const loadViewsOptions = {
                action_id: options.actionId || false,
                load_filters: options.loadIrFilters || false,
                toolbar: (!context?.disable_toolbar && options.loadActionMenus) || false,
            };
            for (const key in options) {
                if (!["actionId", "loadIrFilters", "loadActionMenus"].includes(key)) {
                    loadViewsOptions[key] = options[key];
                }
            }
            if (env.isSmall) {
                loadViewsOptions.mobile = true;
            }
            const filteredContext = Object.fromEntries(
                Object.entries(context || {}).filter(
                    ([k, v]) => k == "lang" || k.endsWith("_view_ref")
                )
            );

            const key = JSON.stringify([resModel, views, filteredContext, loadViewsOptions]);

            if (typeof context.multi_write != 'undefined' && context.multi_write){
                let res = orm
                    .call(resModel, "get_views_multi_write", [[]], {
                        context: filteredContext,
                        views,
                        options: loadViewsOptions,
                    })
                    .then((result) => {
                        const { models, views } = result;
                        const viewDescriptions = {
                            fields: models[resModel],
                            relatedModels: models,
                            views: {},
                        };
                        for (const viewType in views) {
                            const { arch, toolbar, id, filters, custom_view_id } = views[viewType];
                            const viewDescription = { arch, id, custom_view_id };
                            if (toolbar) {
                                viewDescription.actionMenus = toolbar;
                            }
                            if (filters) {
                                viewDescription.irFilters = filters;
                            }
                            viewDescriptions.views[viewType] = viewDescription;
                        }
                        return viewDescriptions;
                    })
                    .catch((error) => {
                        return Promise.reject(error);
                    });
                return res;
            }else{
                if (!cache[key]) {
                    cache[key] = orm
                        .call(resModel, "get_views", [], {
                            context: filteredContext,
                            views,
                            options: loadViewsOptions,
                        })
                        .then((result) => {
                            const { models, views } = result;
                            const viewDescriptions = {
                                fields: models[resModel],
                                relatedModels: models,
                                views: {},
                            };
                            for (const viewType in views) {
                                const { arch, toolbar, id, filters, custom_view_id } = views[viewType];
                                const viewDescription = { arch, id, custom_view_id };
                                if (toolbar) {
                                    viewDescription.actionMenus = toolbar;
                                }
                                if (filters) {
                                    viewDescription.irFilters = filters;
                                }
                                viewDescriptions.views[viewType] = viewDescription;
                            }
                            return viewDescriptions;
                        })
                        .catch((error) => {
                            delete cache[key];
                            return Promise.reject(error);
                        });
                }
                return cache[key];
            }
        }
        return { loadViews };
    },
});

patch(ListController.prototype, {
    async multiEditRecords() {
        let self = this;
        let selectIDs = await this.getSelectedResIds();
        var context = this.props.context;
        context['multi_write'] = true;
        context['multi_write_ids'] = selectIDs;
        context['multi_write_model'] = this.model.root.resModel;
        this.actionService.doAction(
            {
                type: "ir.actions.act_window",
                res_model: this.model.root.resModel,
                views: [[false, "form"]],
                res_id: selectIDs[0],
                view_mode: "form",
                target: "new",
                context: context,
            },
            {
                onClose: async () => {
                    await self.model.load();
                },
            }
        );
    },
    getStaticActionMenuItems() {
        const list = this.model.root;
        const isM2MGrouped = list.groupBy.some((groupBy) => {
            const fieldName = groupBy.split(":")[0];
            return list.fields[fieldName].type === "many2many";
        });
        return {
            multiEdit: {
                isAvailable: () => this.activeActions.edit && this.props.editable,
                sequence: 10,
                icon: "fa fa-edit",
                description: _t("Batch Modify"),
                callback: () => this.multiEditRecords(),
            },
            export: {
                isAvailable: () => this.isExportEnable,
                sequence: 10,
                icon: "fa fa-upload",
                description: _t("Export"),
                callback: () => this.onExportData(),
            },
            archive: {
                isAvailable: () => this.archiveEnabled && !isM2MGrouped,
                sequence: 20,
                icon: "oi oi-archive",
                description: _t("Archive"),
                callback: () => {
                    this.dialogService.add(ConfirmationDialog, this.archiveDialogProps);
                },
            },
            unarchive: {
                isAvailable: () => this.archiveEnabled && !isM2MGrouped,
                sequence: 30,
                icon: "oi oi-unarchive",
                description: _t("Unarchive"),
                callback: () => this.toggleArchiveState(false),
            },
            duplicate: {
                isAvailable: () => this.activeActions.duplicate && !isM2MGrouped,
                sequence: 35,
                icon: "fa fa-clone",
                description: _t("Duplicate"),
                callback: () => this.duplicateRecords(),
            },
            delete: {
                isAvailable: () => this.activeActions.delete && !isM2MGrouped,
                sequence: 40,
                icon: "fa fa-trash-o",
                description: _t("Delete"),
                callback: () => this.onDeleteSelectedRecords(),
            },
        };
    }
});