end_points = {
    'article_api': {
        'list_all_articles': '/api/articles',
        'form_data': '/api/articles/get/',
        'archive_articles': '/api/articles/',
        'restore_articles': '/api/articles/',
        'delete_article': '/api/articles/',
        'create_article': '/api/articles',
        'list_articles_by_materialtype': '/api/articles/get/names/',
        'list_testplans_by_article_and_materialtype': '/api/articles/get/testplans/',
        'get_field_config': '/api/field_data/2',
        'archive_field_config': '/api/field_data/update/archive/',
        'restore_field_config': '/api/field_data/update/restore/'
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
        'list_testunit_by_name_and_materialtype': '/api/testUnits/get/names/',
        'get_auto_generated_number': '/api/testUnits/auto/generatedId'
    },
    'test_plan_api': {
        'list_all_test_plans': '/api/testPlans',
        'get_testunits_in_testplan': '/api/testPlans/get/',
        'list_testplan_testunits': '/api/testPlans/get/list/specifications',
        'form_data': '/api/testPlans/get/',
        'archive_testplans': '/api/testPlans/',
        'restore_testplans': '/api/testPlans/',
        'delete_testplan': '/api/testPlans/',
        'create_testplan': '/api/testPlans'
    },
    'orders_api': {
        'list_all_orders': '/api/orders',
        'get_order_by_id': '/api/orderInformation/get/orders/byId/',
        'create_new_order': '/api/orders',
        'get_auto_generated_number': '/api/orders/auto/generatedOrderNumber/?yearOption=',
        'archive_main_order': '/api/orders/archive/',
        'restore_main_order': '/api/orders/restore/',
        'delete_main_order': '/api/orders/',
        'archive_suborder': '/api/orders/archive/suborders/',
        'restore_suborder': '/api/orders/restore/suborders/',
        'delete_suborder': '/api/orders/suborders/',
        'get_suborder': '/api/orders/suborder/?orderId=',
        'set_filter_configurations': '/api/custom_field_data/table/'
    },
    'analysis_api': {
        'list_all_analysis': '/api/reportSheets',
        'archive_analysis': '/api/reportSheets/',
        'restore_analysis': '/api/reportSheets/',
        'delete_analysis': '/api/reportSheets/',
    },
    'contacts_api': {
        'list_all_contacts': '/api/contacts',
        'get_table_fields': '/api/custom_field_data/',
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
    },
    'field_data': {
        'configuration_update': '/api/field_data/update',
        'get_configuration': '/api/field_data/7'
    },
    'modules': {
        'disable_article': '/api/modulesConfigurations/disableArticles',
        'has_articles': '/api/modulesConfigurations/getComponentConfigs'
    }
}