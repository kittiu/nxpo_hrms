frappe.pages['my-documents'].on_page_load = function(wrapper) {
	frappe.my_documents = new MyDocuments(wrapper);

	$(wrapper).bind("show", () => {
		let doctype = frappe.get_route()[1];
		frappe.my_documents.show_my_documents(doctype);
	});

}

class MyDocuments {
	constructor(parent) {
		frappe.ui.make_app_page({
			parent: parent,
			title: __("My Documents"),
			single_column: false,
			card_layout: true,
		});
		this.parent = parent;
		this.page = this.parent.page;
		this.page.sidebar.html(
			`<ul class="standard-sidebar my_documents-sidebar overlay-sidebar"></ul>`
		);
		this.$sidebar_list = this.page.sidebar.find("ul");
		this.get_my_documents_config();
	}

	get_my_documents_config() {
		this.doctypes = [];
		this.filters = {};
		this.my_documents_limit = 20;

		frappe
			.xcall("nxpo_hrms.nxpo_hrms.page.my_documents.my_documents.get_my_documents_config")
			.then((config) => {
				this.my_documents_config = config;
				for (let doctype in this.my_documents_config) {
					this.doctypes.push(doctype);
					this.filters[doctype] = this.my_documents_config[doctype].fields.map(
						(field) => {
							if (typeof field === "object") {
								return field.label || field.fieldname;
							}
							return field;
						}
					);
				}

				// time filter
				this.timespans = [
					"This Year",
					"Last Year",
					"All Time",
					"Select Date Range",
				];

				// for saving current selected filters
				const _initial_doctype = frappe.get_route()[1] || this.doctypes[0];
				const _initial_timespan = this.timespans[0];
				const _initial_filter = this.filters[_initial_doctype];

				this.options = {
					selected_doctype: _initial_doctype,
					selected_filter: _initial_filter,
					selected_filter_item: _initial_filter[0],
					selected_timespan: _initial_timespan,
				};

				this.message = null;
				this.make();
			});
	}

	make() {
		this.$container = $(`<div class="my_documents page-main-content">
			<div class="my_documents-list"></div>
		</div>`).appendTo(this.page.main);

		this.doctypes.map((doctype) => {
			const icon = this.my_documents_config[doctype].icon;
			const menu_name = this.my_documents_config[doctype].menu_name;
			this.get_sidebar_item(doctype, icon, menu_name).appendTo(this.$sidebar_list);
		});

		this.setup_my_documents_fields(); // Fiter Fields

		this.render_selected_doctype();

		// this.render_search_box();

		// Get which my_documents to show
		let doctype = frappe.get_route()[1];
		this.show_my_documents(doctype);
	}

	setup_my_documents_fields() {
		this.company_select = this.page.add_field({
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_default("company"),
			reqd: 1,
			change: (e) => {
				this.make_request();
			},
		});

		this.timespan_select = this.page.add_select(
			__("Timespan"),
			this.timespans.map((d) => {
				return { label: __(d), value: d };
			})
		);
		this.create_date_range_field();

		this.type_select = this.page.add_select(
			__("Field"),
			this.options.selected_filter.map((d) => {
				return { label: __(frappe.model.unscrub(d)), value: d };
			})
		);

		this.timespan_select.on("change", (e) => {
			this.options.selected_timespan = e.currentTarget.value;
			if (this.options.selected_timespan === "Select Date Range") {
				this.date_range_field.show();
			} else {
				this.date_range_field.hide();
			}
			this.make_request();
		});

		this.type_select.on("change", (e) => {
			this.options.selected_filter_item = e.currentTarget.value;
			this.make_request();
		});

		this.employee_select = this.page.add_field({
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			change: (e) => {
				this.make_request();
			},
		});
	}

	create_date_range_field() {
		let timespan_field = $(this.parent).find(
			`.frappe-control[data-original-title="${__("Timespan")}"]`
		);
		this.date_range_field = $(`<div class="from-date-field"></div>`)
			.insertAfter(timespan_field)
			.hide();

		let date_field = frappe.ui.form.make_control({
			df: {
				fieldtype: "DateRange",
				fieldname: "selected_date_range",
				placeholder: __("Date Range"),
				default: [frappe.datetime.month_start(), frappe.datetime.now_date()],
				input_class: "input-xs",
				reqd: 1,
				change: () => {
					this.selected_date_range = date_field.get_value();
					if (this.selected_date_range) this.make_request();
				},
			},
			parent: $(this.parent).find(".from-date-field"),
			render_input: 1,
		});
	}

	render_selected_doctype() {
		this.$sidebar_list.on("click", "li", (e) => {
			let $li = $(e.currentTarget);
			let doctype = $li.find(".doctype-text").attr("doctype-value");

			this.company_select.set_value(
				frappe.defaults.get_default("company") || this.company_select.get_value()
			);
			this.options.selected_doctype = doctype;
			this.options.selected_filter = this.filters[doctype];
			this.options.selected_filter_item = this.filters[doctype][0];

			this.type_select.empty().add_options(
				this.options.selected_filter.map((d) => {
					return { label: __(frappe.model.unscrub(d)), value: d };
				})
			);
			if (this.my_documents_config[this.options.selected_doctype].company_disabled) {
				$(this.parent).find("[data-original-title=Company]").hide();
			} else {
				$(this.parent).find("[data-original-title=Company]").show();
			}

			this.$sidebar_list.find("li").removeClass("active selected");
			$li.addClass("active selected");

			frappe.set_route("my-documents", this.options.selected_doctype);
			this.make_request();
		});
	}

	// render_search_box() {
	// 	this.$search_box = $(`<div class="my_documents-search form-group col-md-3">
	// 			<input type="text" placeholder=${__(
	// 				"Search"
	// 			)} data-element="search" class="form-control my_documents-search-input input-xs">
	// 		</div>`);

	// 	$(this.parent).find(".page-form").append(this.$search_box);
	// }

	show_my_documents(doctype) {
		if (this.doctypes.length) {
			if (this.doctypes.includes(doctype)) {
				this.options.selected_doctype = doctype;
				this.$sidebar_list
					.find(`[doctype-value = "${this.options.selected_doctype}"]`)
					.trigger("click");
			}

			// this.$search_box.find(".my_documents-search-input").val("");
			frappe.set_route("my-documents", this.options.selected_doctype);
		}
	}

	make_request() {
		frappe.model.with_doctype(this.options.selected_doctype, () => {
			this.get_my_documents(this.get_my_documents_data);
		});
	}

	get_my_documents(notify) {
		let company = this.company_select.get_value();
		if (!company && !this.my_documents_config[this.options.selected_doctype].company_disabled) {
			notify(this, null);
			frappe.show_alert(__("Please select Company"));
			return;
		}
		frappe
			.call(this.my_documents_config[this.options.selected_doctype].method, {
				date_range: this.get_date_range(),
				company: company,
				field: this.options.selected_filter_item,
				employee: this.employee_select.get_value(),
				limit: this.my_documents_limit,
			})
			.then((r) => {
				notify(this, r);
			});
	}

	get_my_documents_data(me, res) {
		me.message = null;
		me.$container.find(".my_documents-list").html(me.render_list_view(res.message));
		frappe.utils.setup_search($(me.parent), ".list-item-container", ".list-id");
	}

	render_list_view(items = []) {
		var html = `${this.render_message()}
			<div class="result" style="${this.message ? "display: none;" : ""}">
				${this.render_result(items)}
			</div>`;

		return $(html);
	}

	render_result(items) {
		var html = `${this.render_list_header()}
			${this.render_list_result(items)}`;
		return html;
	}

	render_list_header() {
		const _selected_filter = this.options.selected_filter.map((i) => frappe.model.unscrub(i));
		const fields = ["no", "name","month_period", this.options.selected_filter_item, "employee_name"];
		const filters = fields
			.map((filter) => {
				const col = __(frappe.model.unscrub(filter));
				return `<div class="my_documents-item list-item_content ellipsis text-muted list-item__content--flex-2
					header-btn-base ${filter}
					${col && _selected_filter.indexOf(col) !== -1 ? "text-right" : ""}">
					<span class="list-col-title ellipsis">
						${col}
					</span>
				</div>`;
			})
			.join("");

		return `<div class="list-headers">
  				<div class="list-item" data-list-renderer="List">${filters}</div>
  			</div>`;
	}

	render_list_result(items) {
		let _html = items
			.map((item, index) => {
				const $value = $(this.get_item_html(item, index + 1));
				const $item_container = $(`<div class="list-item-container">`).append($value);
				return $item_container[0].outerHTML;
			})
			.join("");

		return `<div class="result-list">
  				<div class="list-items">
  					${_html}
  				</div>
  			</div>`;
	}

	render_message() {
		const display_class = this.message ? "" : "hide";
		return `<div class="my_documents-empty-state ${display_class}">
  			<div class="no-result text-center">
  				<img src="/assets/frappe/images/ui-states/search-empty-state.svg"
  					alt="Empty State"
  					class="null-state"
  				>
  				<div class="empty-state-text">${this.message}</div>
  			</div>
  		</div>`;
	}

	get_item_html(item, index) {
		const fields = this.my_documents_config[this.options.selected_doctype].fields;
		const value = frappe.format(
			item.value,
			fields.find((field) => {
				let fieldname = field.fieldname || field;
				return fieldname === this.options.selected_filter_item;
			})
		);

		// Transform posting_date to "Month YYYY"
		const date = new Date(item.posting_date);
		const options_date = { year: 'numeric', month: 'long' };
		const month_period = date.toLocaleDateString('en-US', options_date);
			
		const link = `/app/${frappe.router.slug(this.options.selected_doctype)}/${item.name}`;
		const name_html = item.formatted_name
			? `<span class="text-muted ellipsis list-id">${item.formatted_name}</span>`
			: `<a class="grey list-id ellipsis" href="${link}"> ${item.name} </a>`;
		return `<div class="list-item">
  				<div class="list-item_content ellipsis list-item__content--flex-2 no text-center">
  					<span class="text-muted ellipsis">${index}</span>
  				</div>
  				<div class="list-item_content ellipsis list-item__content--flex-2 name">
  					${name_html}
  				</div>
				<div class="list-item_content ellipsis list-item__content--flex-2 month_period">
				  ${month_period}
			  	</div>
  				<div class="list-item_content ellipsis list-item__content--flex-2 value text-right">
  					<span class="text-muted ellipsis">${value}</span>
  				</div>
  				<div class="list-item_content ellipsis list-item__content--flex-2 employee_name">
  					<span class="text-muted ellipsis">${item.employee_name}</span>
  				</div>
  			</div>`;
	}

	get_sidebar_item(item, icon, menu_name) {
		let icon_html = icon ? frappe.utils.icon(icon, "md") : "";
		return $(`<li class="standard-sidebar-item">
			<span>${icon_html}</span>
			<a class="sidebar-link">
				<span class="doctype-text" doctype-value="${item}">${__(menu_name)}</span>
			</a>
		</li>`);
	}

	get_date_range() {
		let timespan = this.options.selected_timespan.toLowerCase();
		let current_date = frappe.datetime.now_date();
		let date_range_map = {
			"this week": [frappe.datetime.week_start(), frappe.datetime.week_end()],
			"this month": [frappe.datetime.month_start(), frappe.datetime.month_end()],
			"this quarter": [frappe.datetime.quarter_start(), frappe.datetime.quarter_end()],
			"this year": [frappe.datetime.year_start(), frappe.datetime.year_end()],
			"last week": [frappe.datetime.add_days(current_date, -7), current_date],
			"last month": [frappe.datetime.add_months(current_date, -1), current_date],
			"last quarter": [frappe.datetime.add_months(current_date, -3), current_date],
			"last year": [frappe.datetime.add_months(current_date, -12), current_date],
			"all time": null,
			"select date range": this.selected_date_range || [
				frappe.datetime.month_start(),
				current_date,
			],
		};
		return date_range_map[timespan];
	}
}
