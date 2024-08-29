import frappe
import json

ECM_TO_FRAPPE = {
    "employee_code": "name",
    "prefix_th": "custom_prefix",
    "salutation_th": "salutation",
    "fname_th": "first_name",
    "lname_th": "last_name",
    "fname_en": "custom_first_name_en",
    "lname_en": "custom_last_name_en",
    "nick_name": "custom_nick_name",
    "gender": "gender",
    "probation_day": "custom_probation_days",
    "current_house_no": "custom_house_no",
    "current_soi": "custom_soi",
    "current_street": "custom_street",
    "current_subdistrict": "custom_subdistrict",
    "current_district": "custom_district",
    "current_province": "custom_province",
    "current_zipcode": "custom_zip_code",
    "permanent_house_no": "custom_perm_house_no",
    "permanent_soi": "custom_perm_soi",
    "permanent_street": "custom_perm_street",
    "permanent_subdistrict": "custom_perm_subdistrict",
    "permanent_district": "custom_perm_district",
    "permanent_province": "custom_perm_province",
    "permanent_zipcode": "custom_perm_zip_code",
    "date_birth": "date_of_birth",
    "date_join": "date_of_joining",
    "citizen_id": "custom_citizen_id",
    "mobile": "cell_number",
    "martial_status": "custom_married_status",
    "personal_email": "personal_email",
    "company_email": "company_email",
    "nick_name": "custom_nick_name",
    "bank_name": "custom_bank",
    "bank_ac_no": "bank_ac_no",
    "bank_branch_code": "custom_bank_branch_code",
    "bank_branch_name": "custom_bank_branch",
    "education": {
        "edu_level": "custom_degree",
        "edu_educational": "custom_qualification_new",
        "edu_datestart": "custom_year_of_admission",
        "edu_dateend": "custom_year_of_graduation",
        "edu_academy": "custom_schooluniversity",
        "edu_country": "custom_country",
        "edu_major": "custom_major",
        "edu_subject": "maj_opt_subj",
        "edu_gpa": "custom_gpa",
    },
    "status": "status"
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
            emp.custom_prefix as PREFIX_NAME,
            emp.gender as GENDER,
            emp.salutation as SALUTATION_NAME,
            emp.custom_salutation_en as SALUTATION_NAME_EN,
            emp.first_name as FNAME,
            emp.last_name as LNAME,
            emp.custom_first_name_en as FNAME_EN,
            emp.custom_last_name_en as LNAME_EN,
            emp.custom_nick_name as NICK_NAME,
            emp.custom_citizen_id as CITIZEN_ID,
            emp.date_of_birth as BIRTHDAY,
            emp.cell_number as CURRENT_TEL,
            emp.company_email as EMAIL,  # Company Email is not in ECM
            emp.custom_house_no as CURRENT_ADDRESS,
            emp.custom_soi as CURRENT_SOI,
            emp.custom_street as CURRENT_ROAD,
            emp.custom_subdistrict as CURRENT_DISTRICT_NAME,
            emp.custom_district as CURRENT_AMPHUR_NAME,
            emp.custom_province as CURRENT_PROVINCE_NAME,
            emp.custom_zip_code as CURRENT_ZIPCODE,
            emp.custom_perm_house_no as PERMANENT_ADDRESS,
            emp.custom_perm_soi as PERMANENT_SOI,
            emp.custom_perm_street as PERMANENT_ROAD,
            emp.custom_perm_subdistrict as PERMANENT_DISTRICT_NAME,
            emp.custom_perm_district as PERMANENT_AMPHUR_NAME,
            emp.custom_perm_province as PERMANENT_PROVINCE_NAME,
            emp.custom_perm_zip_code as PERMANENT_ZIPCODE,
            dep.custom_department_sync_code as DEPARTMENT_CODE,
            dep.department_name as DEPARTMENT_NAME,
            dit.custom_department_sync_code as DIRECTORATE_CODE,
            dit.department_name as DIRECTORATE_NAME,
            pos.custom_sync_code as POSITION_CODE,
            emp.designation as POSITION_NAME,
            emp.custom_bank as BANK_NAME,
            emp.custom_bank_branch_code as BRANCH_BANK_CODE,
            emp.custom_bank_branch as BRANCH_BANK_NAME,
            bank.custom_bank_code as BANK_CODE,
            bank.custom_bank_symbol as BANK_SYMBOL,
            bank.custom_bank_name_en as BANK_NAME_EN,
            bank.custom_detail as DETAIL,
            bank.custom_detail2 as DETAIL2,
            emp.bank_ac_no as BANK_ACCOUNT_NUMBER,
            sub.custom_department_sync_code as SUB_DEPARTMENT_CODE,
            sub.department_name as SUB_DEPARTMENT_NAME,
            dep.custom_chief as MANAGER,
            dep.custom_chief_name as MANAGER_NAME,
            emp.modified as LAST_UPDATE,
            emp.date_of_joining as START_DATE,
            emp.relieving_date as END_DATE,
            emp.status as STATUS,
            emp.custom_job_family as POSITION_GROUP_ID,
            emp.grade as POSITION_LEVEL_ID,
            emp.custom_probation_days as PROBATION_DAY,
            emp.image as AVATAR_URL
        from `tabEmployee` emp
        left outer join `tabDepartment` dit on emp.custom_directorate = dit.name and dit.custom_type = 'กลุ่มงาน'
        left outer join `tabDepartment` dep on emp.department = dep.name and dep.custom_type = 'ฝ่ายงาน'
        left outer join `tabDepartment` sub on emp.custom_subdepartment = sub.name and sub.custom_type = 'แผนกงาน'
        left outer join `tabDesignation` pos on emp.designation = pos.name
        left outer join `tabBank` bank on emp.custom_bank = bank.name
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
                GREATEST(sub.modified, dep.modified, dit.modified) as LAST_UPDATE,
                case
                    when dit.disabled = 1 then 0
                    when dit.disabled = 0 then 1
                    else 1
                end as ACTIVE
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
                GREATEST(dep.modified, dit.modified) as LAST_UPDATE,
                case
                    when dit.disabled = 1 then 0
                    when dit.disabled = 0 then 1
                    else 1
                end as ACTIVE
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
                dit.modified as LAST_UPDATE,
                case
                    when dit.disabled = 1 then 0
                    when dit.disabled = 0 then 1
                    else 1
                end as ACTIVE
            from `tabDepartment` dit
            where dit.custom_type = 'กลุ่มงาน'
        """,
        as_dict=True
    )
    return data


@frappe.whitelist(methods=["POST"])
def create_employee_performance():
    # nxpo_hrms.rest_api.create_employee_grade
    data = frappe._dict(json.loads(frappe.request.data))
    data["doctype"] = "Employee Performance"
    grade = frappe.get_doc(data)
    return grade.insert()


@frappe.whitelist(methods=["GET"])
def get_holiday(holiday_list=None, weekly_holiday=None):
    sql = """
        select parent as holiday_list, holiday_date, description, weekly_off
        from tabHoliday
        where 1 = 1
    """
    if holiday_list is not None:
        sql += " and parent = '{0}'".format(holiday_list)
    if weekly_holiday is not None:
        sql += " and weekly_off = '{0}'".format(weekly_holiday)
    data = frappe.db.sql(sql, as_dict=True)
    return data


@frappe.whitelist(methods=["GET"])
def get_employee_family(employee=None):
    sql = """
        select parent as employee, prefix, first_name, last_name, citizen_id,
            relationship, date_of_birth, custom_gender, phone
        from `tabEmployee Family Members`
        where 1 = 1
    """
    if employee is not None:
        sql += " and parent = '{0}'".format(employee)
    data = frappe.db.sql(sql, as_dict=True)
    return data

@frappe.whitelist(methods=["GET"])
def get_employee_education(employee=None):
    sql = """
        select emp.employee as employee_code,
            emp.first_name as first_name,
            emp.last_name as last_name,
            edu.custom_degree as edu_level,
            edu.custom_qualification_new as edu_educational,
            edu.custom_major as edu_major,
            edu.maj_opt_subj as edu_subject,
            edu.custom_country as edu_country,
            edu.custom_schooluniversity as edu_academy,
            edu.custom_gpa as edu_gpa,
            edu.custom_year_of_admission as edu_datestart,
            edu.custom_year_of_graduation as edu_dateend
        from `tabEmployee` emp join `tabEmployee Education` edu on emp.name = edu.parent
        where 1 = 1
    """
    if employee is not None:
        sql += " and edu.parent = '{0}'".format(employee)
    data = frappe.db.sql(sql, as_dict=True)
    return data