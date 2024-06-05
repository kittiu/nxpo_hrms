import frappe

# def fetch_org_structure():
#     query = """
#         SELECT idx, level_1, level_2, level_3 
#         FROM `tabOrg Structure Tree`
#         ORDER BY idx ASC
#     """
#     results = frappe.db.sql(query, as_dict=True)

#     # Organize the data into a nested structure
#     org_structure = {'level_1': [], 'level_2': {}, 'level_3': {}}

#     for row in results:
#         if row['level_1']:
#             org_structure['level_1'].append(row['level_1'])
#         elif row['level_2']:
#             if row['level_2'] not in org_structure['level_2']:
#                 org_structure['level_2'][row['level_2']] = []
#             org_structure['level_2'][row['level_2']].append(row['level_1'])
#         elif row['level_3']:
#             if row['level_3'] not in org_structure['level_3']:
#                 org_structure['level_3'][row['level_3']] = []
#             org_structure['level_3'][row['level_3']].append(row['level_2'])

#     return org_structure

def fetch_org_structure(parent):
    filters = {'parent': parent}
    query = """
        SELECT idx, level_1, level_2, level_3, parent 
        FROM `tabOrg Structure Tree`
        WHERE parent = %(parent)s and idx > 0 and idx < 13
        ORDER BY idx ASC
    """
    results = frappe.db.sql(query, filters, as_dict=True)

    org_structure = []

    current_group = None
    current_department = None

    for row in results:
        if row['level_1']:
            current_group = {
                'name': row['level_1'],
                'departments': []
            }
            org_structure.append(current_group)
        elif row['level_2'] and current_group:
            current_department = {
                'name': row['level_2'],
                'units': []
            }
            current_group['departments'].append(current_department)
        elif row['level_3'] and current_department:
            current_department['units'].append({
                'name': row['level_3']
            })

    return org_structure
