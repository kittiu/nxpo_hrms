import frappe
import json


@frappe.whitelist(methods=["POST"])
def create_employee():
    # nxpo_hrms.rest_api.create_employee
    data = frappe._dict(json.loads(frappe.request.data))
    data["doctype"] = "Employee"
    employee_dict = {
        "doctype": "Employee",
        "preferred_contact_email": "Company Email",
        "name": data.name,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "custom_first_name_en": data.custom_first_name_en,
        "custom_last_name_en": data.custom_last_name_en,
        "gender": data.gender,
        "date_of_birth": data.date_of_birth,
        "date_of_joining": data.date_of_joining,
        "custom_probation_days": data.probation_days,  # default to 180
        "cell_number": data.cell_number,
        "personal_email": data.personal_email,
        "company_email": data.company_email,
        "custom_house_no": data.house_no,
        "custom_street": data.street,
        "custom_subdistrict": data.subdistrict,
        "custom_district": data.district,
        "custom_province": data.province,
        "custom_zip_code": data.zip_code,
        "bio": data.bio
    }
    employee = frappe.get_doc(employee_dict)
    return employee.insert()

# create a frappe.whitelist() function that will return directorate data
@frappe.whitelist(methods=["GET"])
def get_directorate():
    # nxpo_hrms.rest_api.get_directorate
    data = frappe.get_all(
        "Department",
        filters={"custom_type": "กลุ่มงาน", "disabled": 0},
        fields=[
            "custom_department_sync_code as DIRECTORATE_CODE",
            "department_name as DIRECTORATE_NAME",
            "modified as LAST_UPDATE"
        ])
    return data