import frappe
import json

ECM_TO_FRAPPE = {
    "employee_code": "name",  # Missing
    "prefix_th": "custom_prefix",
    "fname_th": "first_name",
    "lname_th": "last_name",
    # "prefix_en": "custom_prefix_en",  # No need as related to prefix_th
    "fname_en": "custom_first_name_en",
    "lname_en": "custom_last_name_en",
    "gender": "gender",  # Missing
    "house_no": "custom_house_no",
    "street": "custom_street",
    "subdistrict": "custom_subdistrict",
    "district": "custom_district",
    "province": "custom_province",
    "zipcode": "custom_zip_code",
    "date_birth": "date_of_birth",
    "date_join": "date_of_joining",  # Missing
    "citizen_id": "custom_citizen_id",
    "mobile": "cell_number",
    "martial_status": "custom_married_status",
    "personal_email": "personal_email",
    "education": {
        "edu_level": "custom_degree",
        "edu_educational": "qualification",
        "edu_datestart": "custom_year_of_admission",  # Missing
        "edu_dateend": "custom_year_of_graduation",
        "edu_academy": "school_univ",
        "edu_country": "custom_country",
        "edu_major": "custom_major",
        "edu_gpa": "custom_gpa",
    }
}

@frappe.whitelist(methods=["POST"])
def create_employee():
    # nxpo_hrms.rest_api.create_employee
    data = frappe._dict(json.loads(frappe.request.data))
    employee_dict = {"doctype": "Employee"}
    # Transform ECM data to frappe data
    for key, value in data.items():
        if key in ECM_TO_FRAPPE:
            if isinstance(ECM_TO_FRAPPE[key], dict):
                employee_dict[key] = []
                for row in data[key]:
                    edu_dict = {}
                    for k, v in ECM_TO_FRAPPE[key].items():
                        edu_dict[v] = row[k]
                    employee_dict[key].append(edu_dict)
            else:
                employee_dict[ECM_TO_FRAPPE[key]] = value
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