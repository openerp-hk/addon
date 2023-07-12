odoo.define('web.EditableListRenderer.ext', function (require) {
"use strict";

let ListRenderer = require('web.ListRenderer');

ListRenderer.include({
    init: function (parent, state, params) {
        this._super.apply(this, arguments);
        this.tempFieldIndex = null;
        this.totalDataRows = null;
    },
    editRecord: function (recordID) {
        var $row = this._getRow(recordID);
        var rowIndex = $row.prop('rowIndex') - 1;
        let res = this._selectCell(rowIndex, this.tempFieldIndex ? this.tempFieldIndex : 0);
        this.tempFieldIndex = false;
        return res
    },
    _renderRows: function () {
        let $rows = this._super();
        let $dataRows = $rows.filter((el) => {
            return el.hasClass('o_data_row');
        });
        this.totalDataRows = $dataRows.length;
        return $rows;
    },
    _selectCell: function (rowIndex, fieldIndex, options) {
        options = options || {};
        // Do nothing if the user tries to select current cell
        if (!options.force && rowIndex === this.currentRow && fieldIndex === this.currentFieldIndex) {
            return Promise.resolve();
        }
        var wrap = options.wrap === undefined ? true : options.wrap;
        var recordID = this._getRecordID(rowIndex);

        // Select the row then activate the widget in the correct cell
        var self = this;
        let res = this._selectRow(rowIndex).then(function () {
            var record = self._getRecord(recordID);
            if (fieldIndex >= (self.allFieldWidgets[record.id] || []).length) {
                return Promise.reject();
            }
            // _activateFieldWidget might trigger an onchange,
            // which requires currentFieldIndex to be set
            // so that the cursor can be restored
            var oldFieldIndex = self.currentFieldIndex;
            self.currentFieldIndex = fieldIndex;
            fieldIndex = self._activateFieldWidget(record, fieldIndex, {
                inc: options.inc || 1,
                wrap: wrap,
                event: options && options.event,
            });
            if (fieldIndex < 0) {
                self.currentFieldIndex = oldFieldIndex;
                return Promise.reject();
            }
            self.currentFieldIndex = fieldIndex;
            // console.log("this.currentRow:", self.currentRow);
            // console.log("this.currentFieldIndex:", self.currentFieldIndex);
            // if(options && options.event){
            //     options.event.target.addEventListener('keydown', function(e){
            //         if(e.keyCode == 37){
            //             console.log("左")
            //         }else if (e.keyCode == 38){
            //             console.log("上")
            //         }else if (e.keyCode == 39){
            //             console.log("右")
            //         }else if (e.keyCode == 40){
            //             console.log("下")
            //         }
            //     })
            // }

        });
        return res;
    },
    _moveToSideLine: function (next, options) {
        options = options || {};
        const recordID = this._getRecordID(this.currentRow);
        this.commitChanges(recordID).then(() => {
            const record = this._getRecord(recordID);
            const multiEdit = this.isInMultipleRecordEdition(recordID);
            if (!multiEdit) {
                const fieldNames = this.canBeSaved(recordID);
                if (fieldNames.length && (record.isDirty() || options.forceCreate)) {
                    // the current row is invalid, we only leave it if it is not dirty
                    // (we didn't make any change on this row, which is a new one) and
                    // we are navigating with TAB (forceCreate=false)
                    return;
                }
            }
            // compute the index of the next (record) row to select, if any
            const side = next ? 'first' : 'last';
            const borderRowIndex = this._getBorderRow(side).prop('rowIndex') - 1;
            let _cellIndex = next && options.cellIndex ? options.cellIndex : 0
            const cellIndex = next ? _cellIndex : this.allFieldWidgets[recordID].length - 1;
            const cellOptions = { inc: next ? 1 : -1, force: true };
            const $currentRow = this._getRow(recordID);
            const $nextRow = this._getNearestEditableRow($currentRow, next);
            let nextRowIndex = null;
            let groupId;

            if (!this.isGrouped) {
                // ungrouped case
                if ($nextRow.length) {
                    nextRowIndex = $nextRow.prop('rowIndex') - 1;
                } else if (!this.editable) {
                    nextRowIndex = borderRowIndex;
                } else if (!options.forceCreate && !record.isDirty()) {
                    this.trigger_up('discard_changes', {
                        recordID: recordID,
                        onSuccess: this.trigger_up.bind(this, 'activate_next_widget', { side: side }),
                    });
                    return;
                }
            } else {
                // grouped case
                var $directNextRow = $currentRow.next();
                if (next && this.editable === "bottom" && $directNextRow.hasClass('o_add_record_row')) {
                    // the next row is the 'Add a line' row (i.e. the current one is the last record
                    // row of the group)
                    if (options.forceCreate || record.isDirty()) {
                        // if we modified the current record, add a row to create a new record
                        groupId = $directNextRow.data('group-id');
                    } else {
                        // if we didn't change anything to the current line (e.g. we pressed TAB on
                        // each cell without modifying/entering any data), we discard that line (if
                        // it was a new one) and move to the first record of the next group
                        nextRowIndex = ($nextRow.prop('rowIndex') - 1) || null;
                        this.trigger_up('discard_changes', {
                            recordID: recordID,
                            onSuccess: () => {
                                if (nextRowIndex !== null) {
                                    if (!record.res_id) {
                                        // the current record was a new one, so we decrement
                                        // nextRowIndex as that row has been removed meanwhile
                                        nextRowIndex--;
                                    }
                                    this._selectCell(nextRowIndex, cellIndex, cellOptions);
                                } else {
                                    // we were in the last group, so go back to the top
                                    this._selectCell(borderRowIndex, cellIndex, cellOptions);
                                }
                            },
                        });
                        return;
                    }
                } else {
                    // there is no 'Add a line' row (i.e. the create feature is disabled), or the
                    // list is editable="top", we focus the first record of the next group if any,
                    // or we go back to the top of the list
                    nextRowIndex = $nextRow.length ?
                        ($nextRow.prop('rowIndex') - 1) :
                        borderRowIndex;
                }
            }

            // if there is a (record) row to select, select it, otherwise, add a new record (in the
            // correct group, if the view is grouped)
            if (nextRowIndex !== null) {
                // cellOptions.force = true;
                this._selectCell(nextRowIndex, cellIndex, cellOptions);
            } else if (this.editable) {
                // if for some reason (e.g. create feature is disabled) we can't add a new
                // record, select the first record row
                this.unselectRow().then(this.trigger_up.bind(this, 'add_record', {
                    groupId: groupId,
                    onFail: this._selectCell.bind(this, borderRowIndex, cellIndex, cellOptions),
                }));
            }
        });
    },
    _onNavigationMove: function (ev) {
        var self = this;
        // Don't stop the propagation when navigating up while not editing any row
        if (this.currentRow === null && ev.data.direction === 'up') {
            return;
        }
        ev.stopPropagation(); // stop the event, the action is done by this renderer
        if (ev.data.originalEvent && ['next', 'previous'].includes(ev.data.direction)) {
            ev.data.originalEvent.preventDefault();
            ev.data.originalEvent.stopPropagation();
        }
        switch (ev.data.direction) {
            case 'previous':
                if (this.currentFieldIndex > 0) {
                    this._selectCell(this.currentRow, this.currentFieldIndex - 1, {inc: -1, wrap: false})
                        .guardedCatch(this._moveToPreviousLine.bind(this));
                } else {
                    this._moveToPreviousLine();
                }
                break;
            case 'next':
                if (this.currentFieldIndex + 1 < this.columns.length) {
                    this._selectCell(this.currentRow, this.currentFieldIndex + 1, {wrap: false})
                        .guardedCatch(this._moveToNextLine.bind(this));
                } else {
                    this._moveToNextLine();
                }
                break;
            case 'next_line':
                // If the list is readonly and the current is the only record editable, we unselect the line
                if (!this.editable && this.selection.length === 1 &&
                    this._getRecordID(this.currentRow) === ev.target.dataPointID) {
                    this.unselectRow();
                } else {
                    this._moveToNextLine({ forceCreate: true });
                }
                break;
            case 'cancel':
                // stop the original event (typically an ESCAPE keydown), to
                // prevent from closing the potential dialog containing this list
                // also auto-focus the 1st control, if any.
                ev.data.originalEvent.stopPropagation();
                var rowIndex = this.currentRow;
                var cellIndex = this.currentFieldIndex + 1;
                this.trigger_up('discard_changes', {
                    recordID: ev.target.dataPointID,
                    onSuccess: function () {
                        self._enableRecordSelectors();
                        var recordId = self._getRecordID(rowIndex);
                        if (recordId) {
                            var correspondingRow = self._getRow(recordId);
                            correspondingRow.children().eq(cellIndex).focus();
                        } else if (self.currentGroupId) {
                            self.$('a[data-group-id="' + self.currentGroupId + '"]').focus();
                        } else {
                            self.$('.o_field_x2many_list_row_add a:first').focus(); // FIXME
                        }
                    }
                });
                break;
            case 'up':
                if(this.currentRow != 0){
                    this._selectCell(this.currentRow - 1, this.currentFieldIndex, {wrap: false});
                }
                break;
            case 'down':
                let tempRow = this.currentRow + 1;
                this.tempFieldIndex = this.currentFieldIndex;
                if (this.currentRow >= this.totalDataRows - 1){
                    this._moveToNextLine({ forceCreate: true , cellIndex: this.tempFieldIndex});
                }
                this._selectCell(tempRow, this.tempFieldIndex, {wrap: false});
                break;
            case 'right':
                if (this.currentFieldIndex + 1 < this.columns.length) {
                    ev.stopPropagation();
                    this.trigger_up('navigation_move', {direction: 'next'});
                } else {
                    this._moveToNextLine({ forceCreate: true });
                }
                break;
            case 'left':
                if(this.currentRow != 0 || this.currentFieldIndex != 0){
                    ev.stopPropagation();
                    this.trigger_up('navigation_move', {direction: 'previous'});
                }
                break;

        }
    },
});

});
