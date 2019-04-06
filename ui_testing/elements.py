elements = {
    'general': {'search': {'method': 'id',
                           'value': 'generalSearch'},
                'table': {'method': 'id',
                          'value': 'table'}},
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
                 'value': 'namefield'},
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
                           'order': 0}
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
}
