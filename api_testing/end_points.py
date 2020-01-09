end_points = {
    'article_api': {
        'list_all_articles': '/api/articles',
        'form_data': '/api/articles/get/',
        'archive_articles': '/api/articles/',
        'restore_articles': '/api/articles/',
        'delete_article': '/api/articles/',
        'create_article': '/api/articles'
    },
    'test_unit_api': {
        'list_all_test_units': '/api/testUnits',
        'report_sheet_get_list_table': '/api/reportSheets/get/list/table/testunits',
        'form_data': '/api/testUnits/get/',
        'archive_testunits': '/api/testUnits/',
        'restore_testunits': '/api/testUnits/',
        'delete_testunit': '/api/testUnits/',
        'create_testunit': '/api/testUnits',
        'list_testunit_types': '/api/testUnits/list/types',
        'list_testunit_concentrations': '/api/testUnits/list/concentrations',
        'list_testunit_categories': '/api/testUnits/list/categories',
    },
    'test_plan_api': {
        'list_all_test_plans': '/api/testPlans',
        'get_testunits_in_testplan': '/api/testPlans/get/',
        'list_testplan_testunits': '/api/testPlans/get/list/specifications',
        'form_data': '/api/testPlans/get/',
        'archive_testplans': '/api/testPlans/',
        'restore_testplans': '/api/testPlans/',
        'delete_testplan': '/api/testPlans/'
    },
    'orders_api': {
        'list_all_orders': '/api/orders',
        'get_order_by_id': '/api/orderInformation/get/orders/byId/'
    },
    'contacts_api': {
        'list_all_contacts': '/api/contacts',
        'form_data': '/api/contacts/get/',
        'archive_contacts': '/api/contacts/archive/',
        'restore_contacts': '/api/contacts/restore/',
        'delete_contact': '/api/contacts/',
        'create_contact': '/api/contacts',
        'update_contact': '/api/contacts'
    },
    'users_api': {
        'list_all_users': '/api/users',
        'form_data': '/api/users/',
        'archive_users': '/api/users/',
        'restore_users': '/api/users/',
        'delete_user': '/api/users/'
    },
    'roles_api': {
        'list_all_roles': '/api/roles',
        'form_data': '/api/roles/',
        'archive_roles': '/api/roles/',
        'restore_roles': '/api/roles/',
        'delete_role': '/api/roles/',
        'create_role': '/api/roles',
        'update_role': '/api/roles'
    },
    'components': {
        'list_components': '/api/components'
    },
    'materialTypes': {
        'list_material_types': '/api/materialTypes'
    }
}
