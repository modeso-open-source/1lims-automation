elements = {
    'general': {'search': {'method': 'id',
                           'value': 'generalSearch'},
                'table': {'method': 'id',
                          'value': 'table'},
                'save': {'method': 'class_name',
                         'value': 'btn-primary',
                         'order': 0},
                'cancel': {'method': 'class_name',
                           'value': 'btn-secondary',
                           'order': 1},
                'confirmation_pop_up': {
                    'method': 'id',
                    'value': 'swal2-title'},

                'confirm_pop': {'method': 'class_name',
                                'value': 'btn-success',
                                'order': 0},
                'confirm_cancel': {'method': 'class_name',
                                   'value': 'btn-secondary',
                                   'order': 0},
                'drop_down_options': {'method': 'class_name',
                                      'value': 'ng-option'}
                },
    'login': {
        'username': {'method': 'name',
                     'value': 'username',
                     'order': 0},
        'password': {'method': 'name',
                     'value': 'password',
                     'order': 0},
        'login_btn': {'method': 'id',
                      'value': 'm_login_signin_submit'}
    },

    'articles': {
        'article_table': {'method': 'id',
                          'value': 'table'},
        'article_edit_button': {'method': 'tag_name',
                                'value': 'a',
                                'order': 2},
        'article_archive_button': {'method': 'tag_name',
                                   'value': 'a',
                                   'order': 0},
        'article_archive_dropdown': {'method': 'link_text',
                                     'value': 'Archive'},
        'confirm_archive': {'method': 'class_name',
                            'value': 'swal2-confirm',
                            'order': 0},
        'cancel_archive': {'method': 'class_name',
                           'value': 'swal2-cancel',
                           'order': 0},
        'new_article': {'method': 'link_text',
                        'value': 'New Article'}
    },
    'article': {
        'unit': {'method': 'id',
                 'value': 'unitfield'},
        'material_type': {'method': 'id',
                          'value': 'materialType'},
        'material_type_options': {'method': 'class_name',
                                  'value': 'ng-option'},
        'no': {'method': 'id',
               'value': 'Nofield'},
        'comment': {'method': 'id',
                    'value': 'comment'},

        'name': {'method': 'id',
                 'value': 'namefield'}
    },

    'test_plans': {
        'test_plans_table': {'method': 'id',
                             'value': 'table'},
        'test_plans_edit_button': {'method': 'tag_name',
                                   'value': 'a',
                                   'order': 1},
        'new_test_plan': {'method': 'link_text',
                          'value': 'New Test Plan'}
    },

    'test_plan': {
        'no': {'method': 'id',
               'value': 'numberfield'},
        'test_plan': {'method': 'xpath',
                      'value': '//*[@id="testPlan"]/div/div/div[3]/input'},
        'add_test_plan': {'method': 'class_name',
                          'value': 'ng-option-marked',
                          'order': 0},
        'material_type': {'method': 'xpath',
                          'value': '//*[@id="materialTypefield"]'},
        'material_type_options': {'method': 'class_name',
                                  'value': 'ng-option'},
        'article': {'method': 'css_selector',
                    'value': '#selectedArticles > div'
                    },
        'article_options': {'method': 'class_name',
                            'value': 'ng-option'},
    },

    'orders': {
        'orders_table': {'method': 'id',
                         'value': 'table'},
        'orders_edit_button': {'method': 'tag_name',
                               'value': 'a',
                               'order': 4},
        'new_order': {'method': 'link_text',
                      'value': 'New Order'}
    },

    'order': {
        'order': {'method': 'id',
                  'value': 'orderTypefield'},
        'material_type': {'method': 'xpath',
                          'value': '//*[@id="materialTypefield"]'},

        'article': {'method': 'css_selector',
                    'value': '#articlefield > div'}
    }

}
