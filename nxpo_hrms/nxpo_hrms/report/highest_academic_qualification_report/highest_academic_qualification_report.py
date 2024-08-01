# Copyright (c) 2024, Ecosoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)

    return columns, data


def get_columns(filters):
    columns = [
            {
                "fieldname": "employee",
                "fieldtype": "Data",
                "label": "รหัส",
                "width": 0
            },
            {
                "fieldname": "prefix",
                "fieldtype": "Data",
                "label": "คำนำหน้า",
                "width": 0
            },
            {
                "fieldname": "employee_name",
                "fieldtype": "Data",
                "label": "ชื่อ-นามสกุล",
                "width": 0
            },
            {
                "fieldname": "schooluniversity",
                "fieldtype": "Data",
                "label": "School / University",
                "width": 0
            },
            {
                "fieldname": "qualification",
                "fieldtype": "Data",
                "label": "Qualification",
                "width": 0
            },
            {
                "fieldname": "major",
                "fieldtype": "Data",
                "label": "Major",
                "width": 0
            },
            {
                "fieldname": "major_optional_subjects",
                "fieldtype": "Data",
                "label": "Major/Optional Subjects",
                "width": 0
            },
            {
                "fieldname": "degree",
                "fieldtype": "Data",
                "label": "Highest Degree",
                "width": 0
            },
            {
                "fieldname": "year_of_graduation",
                "fieldtype": "Data",
                "label": "Year of Graduation",
                "width": 0
            },
            {
                "fieldname": "year_of_admission",
                "fieldtype": "Data",
                "label": "Year of Admission",
                "width": 0
            },
            {
                "fieldname": "gpa",
                "fieldtype": "Data",
                "label": "GPA",
                "width": 0
            },
            {
                "fieldname": "country",
                "fieldtype": "Data",
                "label": "Country",
                "width": 0
            },
    ]

    return columns

def get_data(filters):
    data = []
    conditions = get_conditions(filters)

    query_data = frappe.db.sql(
        f"""select 
                emp.employee,
                emp.custom_prefix as prefix,
                emp.employee_name
            from `tabEmployee` emp
            WHERE emp.company = %(company)s {conditions}
            """,
        filters,
        as_dict=True,
    )


    data = query_data

    for row in data:
        highest_qualification  = get_highest_academic_qualification_by_emp(row['employee'])
        # Check if a qualification was found before accessing its details
        if highest_qualification is not None:
            row['schooluniversity'] = highest_qualification['schooluniversity']
            row['qualification'] = highest_qualification['qualification']
            row['major'] = highest_qualification['major']
            row['major_optional_subjects'] = highest_qualification['major_optional_subjects']
            row['degree'] = highest_qualification['degree']
            row['year_of_graduation'] = highest_qualification['year_of_graduation']
            row['year_of_admission'] = highest_qualification['year_of_admission']
            row['gpa'] = highest_qualification['gpa']
            row['country'] = highest_qualification['country']

    if  filters.degree is not None:
        # Filter data to include only those rows where 'degree' matches the filter
        data = [row for row in data if row.get('degree') == filters.get('degree')]

    return data

def get_conditions(filters):
    conditions = ""

    if filters.get("employee"):
        conditions += f"and emp.employee = %(employee)s"
    

    return conditions

def get_highest_academic_qualification_by_emp(employee):
    query = """
        SELECT 
            custom_schooluniversity as schooluniversity,
            custom_degree as degree,
            custom_qualification_new as qualification,
            custom_major as major,
            maj_opt_subj as major_optional_subjects,
            custom_year_of_graduation as year_of_graduation,
            custom_year_of_admission as year_of_admission,
            custom_gpa as gpa,
            custom_country as country
        FROM `tabEmployee Education`
        WHERE parent = %(employee)s
    """
    result = frappe.db.sql(query, {'employee': employee}, as_dict=True)

    # Priority mapping, higher number means higher priority
    degree_priority = {
        'ปริญญาเอก': 3,  # Doctorate has the highest priority
        'ปริญญาโท': 2,   # Master's
        'ปริญญาตรี': 1   # Bachelor's
    }

    # Filter and select the highest degree according to the priority
    if result:
        # Sort results by degree priority (descending order)
        sorted_results = sorted(result, key=lambda x: degree_priority.get(x['degree'], 0), reverse=True)
        highest_qualification = sorted_results[0]
        return highest_qualification
    else:
        return None


