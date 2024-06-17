import frappe
import json

ECM_TO_FRAPPE = {
    "employee_code": "name",
    "prefix_th": "custom_prefix",
    "fname_th": "first_name",
    "lname_th": "last_name",
    "fname_en": "custom_first_name_en",
    "lname_en": "custom_last_name_en",
    "gender": "gender",
    "house_no": "custom_house_no",
    "street": "custom_street",
    "subdistrict": "custom_subdistrict",
    "district": "custom_district",
    "province": "custom_province",
    "zipcode": "custom_zip_code",
    "date_birth": "date_of_birth",
    "date_join": "date_of_joining",
    "citizen_id": "custom_citizen_id",
    "mobile": "cell_number",
    "martial_status": "custom_married_status",
    "personal_email": "personal_email",
    "education": {
        "edu_level": "custom_degree",
        "edu_educational": "qualification",
        "edu_datestart": "custom_year_of_admission",
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


def _sql_employee():
    return """
        select emp.name as EMPLOYEE_CODE,
            emp.custom_prefix as INITIAL_NAME,
            emp.first_name as FNAME,
            emp.last_name as LNAME,
            emp.cell_number as CURRENT_TEL,
            emp.company_email as EMAIL,  # Company Email is not in ECM
            emp.custom_house_no as CURRENT_ADDRESS,
            emp.custom_street as CURRENT_ROAD,
            emp.custom_subdistrict as DISTRICT_NAME,
            emp.custom_district as AMPHUR_NAME,
            emp.custom_province as PROVINCE_NAME,
            emp.custom_zip_code as CURRENT_ZIPCODE,
            dep.custom_department_sync_code as DEPARTMENT_CODE,
            dep.department_name as DEPARTMENT_NAME,
            dit.custom_department_sync_code as DIRECTORATE_CODE,
            dit.department_name as DIRECTORATE_NAME,
            pos.custom_sync_code as POSITION_CODE,
            emp.designation as POSITION_NAME,
            # BANK_ID
            # BANK_CODE
            emp.custom_bank as BANK_NAME,
            # BRANCH_BANK_CODE
            # BRANCH_BANK_NAME
            # BRANCH_BANK_NAME_EN
            emp.bank_ac_no as BANK_ACCOUNT_NUMBER,
            sub.custom_department_sync_code as SUB_DEPARTMENT_CODE,
            sub.department_name as SUB_DEPARTMENT_NAME,
            dep.custom_chief as MANAGER,
            dep.custom_chief_name as MANAGER_NAME,
            emp.modified as LAST_UPDATE,
            # ------- EXTRA ---------
            emp.status as STATUS
        from `tabEmployee` emp
        left outer join `tabDepartment` dit on emp.custom_directorate = dit.name and dit.custom_type = 'กลุ่มงาน'
        left outer join `tabDepartment` dep on emp.department = dep.name and dep.custom_type = 'ฝ่ายงาน'
        left outer join `tabDepartment` sub on emp.custom_subdepartment = sub.name and sub.custom_type = 'แผนกงาน'
        left outer join `tabDesignation` pos on emp.designation = pos.name
    """


@frappe.whitelist(methods=["GET"])
def get_all_employee():
    data = frappe.db.sql(
        """{0}""".format(_sql_employee()),
        as_dict=True
    )
    return data


@frappe.whitelist(methods=["GET"])
def get_all_subdepartment():
    data = frappe.db.sql(
        """
            select sub.custom_department_sync_code as SUB_DEPARTMENT_CODE,
                sub.department_name as SUB_DEPARTMENT_NAME,
                dep.custom_department_sync_code as DEPARTMENT_CODE,
                dit.custom_department_sync_code as DIRECTORATE_CODE,
                GREATEST(sub.modified, dep.modified, dit.modified) as LAST_UPDATE
            from `tabDepartment` sub
            join `tabDepartment` dep on sub.parent_department = dep.name
            join `tabDepartment` dit on dep.parent_department = dit.name
            where sub.custom_type = 'แผนกงาน'
        """,
        as_dict=True
    )
    return data


@frappe.whitelist(methods=["GET"])
def get_all_department():
    data = frappe.db.sql(
        """
            select dep.custom_department_sync_code as DEPARTMENT_CODE,
                dep.department_name as DEPARTMENT_NAME,
                dep.custom_department_en as DEPARTMENT_NAME_EN,
                dep.custom_chief as CHIEF_CODE,
                dep.custom_chief_name as CHIEF_NAME,
                dit.custom_department_sync_code as DIRECTORATE_CODE,
                GREATEST(dep.modified, dit.modified) as LAST_UPDATE
            from `tabDepartment` dep
            join `tabDepartment` dit on dep.parent_department = dit.name
            where dep.custom_type = 'ฝ่ายงาน'
        """,
        as_dict=True
    )
    return data


@frappe.whitelist(methods=["GET"])
def get_all_directorate():
    data = frappe.db.sql(
        """
            select dit.custom_department_sync_code as DIRECTORATE_CODE,
                dit.department_name as DIRECTORATE_NAME,
                dit.custom_department_en as DIRECTORATE_NAME_EN,
                dit.modified as LAST_UPDATE,
                dit.custom_chief as CHIEF_CODE,
                dit.custom_chief_name as CHIEF_NAME,
                dit.custom_assistant as ASSISTANT_CODE,
                dit.custom_assistant_name as ASSISTANT_NAME,
                dit.modified as LAST_UPDATE
            from `tabDepartment` dit
            where dit.custom_type = 'กลุ่มงาน'
        """,
        as_dict=True
    )
    return data
