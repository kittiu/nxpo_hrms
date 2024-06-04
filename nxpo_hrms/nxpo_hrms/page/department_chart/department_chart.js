frappe.pages['department-chart'].on_page_load = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Department Chart"),
		single_column: true,
	});

	$(wrapper).bind("show", () => {
		frappe.require("hierarchy-chart.bundle.js", () => {
			let department_chart;
			let method = "nxpo_hrms.nxpo_hrms.page.department_chart.department_chart.get_children";

			if (frappe.is_mobile()) {
				department_chart = new hrms.HierarchyChartMobile("Department", wrapper, method);
			} else {
				department_chart = new hrms.HierarchyChart("Department", wrapper, method);
			}

			frappe.breadcrumbs.add("HR");
			department_chart.show();
		});
	});
}