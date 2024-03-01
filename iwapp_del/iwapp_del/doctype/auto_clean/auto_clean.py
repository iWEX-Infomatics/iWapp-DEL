# Copyright (c) 2023, Craft and contributors
# For license information, please see license.txt

import frappe
import json
import logging
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	add_months,
	add_years,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_last_day,
	get_timestamp,
	getdate,
	nowdate,
)

class AutoClean(Document):
	pass
	# wriiten this code for testing after days deleting docs
	# def on_update(self):
	# 	auto_clean = frappe.db.sql('''
	# 	SELECT
	# 		act.doctype_name as doctype,
	# 		act.delete_files_after_days as after_days
	# 	FROM
	# 		`tabAuto Clean Table` as act
	# 	WHERE
	# 		act.schedular = 1 ''',as_dict=1)
	# 	for i in auto_clean:
	# 		after_date = add_days((getdate(nowdate)), -(int(i.after_days)))
	# 		after_date_midnight = get_datetime(after_date).replace(hour=0, minute=0, second=0, microsecond=0)
	# 		doc_date = frappe.db.get_list(i.doctype, filters={
	# 						'creation': ['<', after_date_midnight]
	# 					},  pluck= 'name')
	# 		if doc_date:
	# 			for j in doc_date:
	# 				frappe.db.delete(i.doctype, j)
	# 		frappe.log_error(message=doc_date, title="hello")
@frappe.whitelist()
def delete_documents(doctype, before_date):
	doc = frappe.db.get_list(doctype, filters={
						'creation': ['<', before_date]
					},  pluck= 'name')
	for i in doc:
		frappe.db.delete(doctype, i)

@frappe.whitelist()
def days_scheduler():
	# auto_clean = frappe.db.get_single_value('Auto Clean', 'auto_clean')
	auto_clean = frappe.db.sql('''
	SELECT
		act.doctype_name as doctype,
		act.delete_files_after_days as after_days
	FROM
		`tabAuto Clean Table` as act
	WHERE
		act.schedular = 1 ''',as_dict=1)
	for i in auto_clean:
		after_date = add_days((getdate(nowdate)), -(int(i.after_days)))
		after_date_midnight = get_datetime(after_date).replace(hour=0, minute=0, second=0, microsecond=0)
		doc_date = frappe.db.get_list(i.doctype, filters={
						'creation': ['<', after_date_midnight]
					},  pluck= 'name')
		if doc_date:
			for j in doc_date:
				frappe.db.delete(i.doctype, j)
		frappe.log_error(message=doc_date, title="hello")
