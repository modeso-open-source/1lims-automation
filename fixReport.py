import requests, sys, uuid

def get_project_launchs(project_name):
    API = f"{BASE_API}/{project_name}/launch"
    response = session.get(API, headers=headers)
    return response

def get_project_launch_by_description(project_name, description):
    API = f"{BASE_API}/{project_name}/launch?filter.eq.description={description}&page.size=100"
    response = session.get(API, headers=headers)
    return response

def get_project_launch_id_by_description(project_name, desription):
    res = get_project_launch_by_description(project_name, desription)
    return res

def get_test_items(project_name, launch_id):
    API = f"{BASE_API}/{project_name}/item?page.size=500&filter.eq.launch={launch_id}"
    response = session.get(API, headers=headers)
    return response


def get_test_items_by_status(project_name, launch_id, status):
    API = f"{BASE_API}/{project_name}/item?page.size=500&filter.eq.launch={launch_id}&filter.eq.status={status}"
    response = session.get(API, headers=headers)
    return response

def delete_test_items(project_name, ids):
    API = f"{BASE_API}/{project_name}/item?ids={ids}"
    response = session.delete(API, headers=headers)
    return response

def filter_duplicate_test_case(project_name, test_case_ids):
    to_be_deleted = []
    for test_case_id in test_case_ids:
        API = f"{BASE_API}/{project_name}/log?filter.eq.item={test_case_id}&filter.in.level=ERROR"
        response = session.get(API, headers=headers)
        if len(response.json()['content']) > 0 and response.json()['content'][0]['message']:
            pass
        else:
            to_be_deleted.append(test_case_id)
    return to_be_deleted

def merge_launchs_with_same_description(project_name, launch_des):
    API = f"{BASE_API}/{project_name}/launch/merge?page.size=200"
    launchs_res = get_project_launch_id_by_description(project_name, launch_des)
    print(len(launchs_res.json()['content']))
    ids = [content['id'] for content in launchs_res.json()['content']]
    _payload = {
              "tags": [""],
              "start_time": launchs_res.json()['content'][0]['start_time'],
              "end_time": launchs_res.json()['content'][0]['end_time'],
              "name": project_name,
              "description": f"{launch_des}__{str(uuid.uuid4())[:8]}",
              "launches": ids,
              "extendSuitesDescription": False,
              "merge_type": "BASIC"
    }
    res = session.post(API, headers=headers, json=_payload)
    return res

def _get_duplicate_fliky_test_cases(project_name, launch_id):
    duplicate_test_case = {}
    test_items = get_test_items(project_name, launch_id).json()['content']
    ids = []
    for test_item in test_items:
        for tmp in test_items:
            if (test_item['name'] == tmp['name']) and (test_item['id'] != tmp['id']) and (test_item['id'] not in ids):
                ids.append(test_item['id'])
                if test_item['name'] in duplicate_test_case.keys():
                    duplicate_test_case[test_item['name']].append(test_item)
                else:
                    duplicate_test_case[test_item['name']] = [test_item]
    return duplicate_test_case

def delete_fliky_failed_test_items(project_name, launch_id):
    delete_id = ""
    duplicate_fliky_tests = _get_duplicate_fliky_test_cases(project_name, launch_id)
    for _, duplicate_tests in duplicate_fliky_tests.items():
        duplicate_test_failed = []
        fliky_flag = False
        for duplicate_test in duplicate_tests:
            if duplicate_test['status'] == 'FAILED':
                duplicate_test_failed.append(duplicate_test['id'])
            elif duplicate_test['status'] == 'PASSED':
                fliky_flag = True

        if fliky_flag:
            for duplicate_test in duplicate_test_failed:
                delete_id = f"{delete_id},{duplicate_test}"
        else:
            filtered = filter_duplicate_test_case(project_name, duplicate_test_failed)
            for duplicate_test in filtered:
                delete_id = f"{delete_id},{duplicate_test}"
    return delete_test_items(project_name, delete_id[1:])


BASE_API = "http://18.158.202.89:8080/api/v1"
AUTHONTICATION = f"bearer {sys.argv[1]}"
PROJECT_NAME = 'onelims'
LAUNCH_DES = f"{sys.argv[2]}"


session = requests.Session()
headers = {'Content-Type': "application/json",
           'Authorization': AUTHONTICATION,
           'Connection': "keep-alive",
           'cache-control': "no-cache"}
# import IPython
# IPython.embed()
#
# print(f'merge all launches with {LAUNCH_DES} description')
merged_launch = merge_launchs_with_same_description(PROJECT_NAME, LAUNCH_DES)

# print(f'launch ID : {merged_launch.json()["id"]}')
if "id" in merged_launch.json().keys():
    res = delete_fliky_failed_test_items(PROJECT_NAME, merged_launch.json()["id"])
# print(res.json())

#IPython.embed()
