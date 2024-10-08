(() => {
  // frappe-html:/home/kittiu/frappe-bench/apps/nxpo_hrms/nxpo_hrms/public/js/templates/nxpo_leave_application_dashboard.html
  frappe.templates["nxpo_leave_application_dashboard"] = `
{% if not jQuery.isEmptyObject(data) %}
<table class="table table-bordered small">
	<thead>
		<tr>
			<th style="width: 16%">{{ __("Leave Type") }}</th>
			<th style="width: 16%" class="text-right">{{ __("Total Allocated Leaves") }}</th>
			<!-- <th style="width: 16%" class="text-right">{{ __("Expired Leaves") }}</th> -->
			<th style="width: 16%" class="text-right">{{ __("Used Leaves") }}</th>
			<th style="width: 16%" class="text-right">{{ __("Leaves Pending Approval") }}</th>
			<th style="width: 16%" class="text-right">{{ __("Available Leaves") }}</th>
		</tr>
	</thead>
	<tbody>
		{% for(const [key, value] of Object.entries(data)) { %}
			{% let color = cint(value["remaining_leaves"]) > 0 ? "green" : "red" %}
			<tr>
				<td> {%= key %} </td>
				<td class="text-right"> {%= value["total_leaves"] %} </td>
				<!-- <td class="text-right"> {%= value["expired_leaves"] %} </td> -->
				<td class="text-right"> {%= value["leaves_taken"] %} </td>
				<td class="text-right"> {%= value["leaves_pending_approval"] %} </td>
				<td class="text-right" style="color: {{ color }}"> {%= value["remaining_leaves"] %} </td>
			</tr>
		{% } %}
	</tbody>
</table>
{% else %}
<p style="margin-top: 30px;"> {{ __("No leaves have been allocated.") }} </p>
{% endif %}
`;
})();
//# sourceMappingURL=nxpo_hrms.bundle.UZZ6AISM.js.map
