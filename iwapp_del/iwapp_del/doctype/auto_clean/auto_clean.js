// Copyright (c) 2023, Craft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Auto Clean', {
	after_save: function (frm) {
		if (frm.doc.auto_clean.length > 0) {
			frm.set_value("display_schedule", 1)
		}
		else {
			frm.set_value("display_schedule", 0)
		}
	},
	refresh: function (frm) {
		if (frm.doc.auto_clean.length > 0) {
			frm.set_value("display_schedule", 1)
		}
		else {
			frm.set_value("display_schedule", 0)
		}
	},
	delete_files: function (frm) {
		if (frm.doc.schedular == 0 && frm.doc.auto_clean.length > 0) {
			$.each(frm.doc.auto_clean, function (j, row) {
				frappe.call({
					method: 'iwapp_del.iwapp_del.doctype.auto_clean.auto_clean.delete_documents',
					args: {
						'doctype': row.doctype_name,
						'before_date': row.delete_files_before_date

					},
					callback: function (r) {
						// if(r.message)
						// frappe.msgprint("successfully deleted documents")
						frm.reload_doc();
					},
				});
			})
		}
	},
	schedular: function (frm) {
		if (frm.doc.schedular == 1) {
			// if (frm.doc.auto_clean){
			$.each(frm.doc.auto_clean, function (j, row) {
				frappe.model.set_value(row.doctype, row.name, "schedular", 1)
			})
			// }
		}
		else {
			// if (frm.doc.auto_clean){
			$.each(frm.doc.auto_clean, function (j, row) {
				frappe.model.set_value(row.doctype, row.name, "schedular", 0)
			})
			// }

		}

	}
});
