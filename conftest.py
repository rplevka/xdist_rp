from pdb import set_trace
from time import time
import traceback
from reportportal_client import ReportPortalServiceAsync

endpoint = "http://localhost:8080"
project = "foo_personal"
token = "feee450c-401d-40a1-854d-96c42672701c"
launch_name = "Test_launch"
launch_doc = "Testing logging with attachment."

stack = {}

def timestamp():
    return str(int(time() * 1000))


def my_error_handler(exc_info):
    """
    This callback function will be called by async service client when error occurs.
    Return True if error is not critical and you want to continue work.
    :param exc_info: result of sys.exc_info() -> (type, value, traceback)
    :return:
    """
    print("Error occurred: {}".format(exc_info[1]))
    traceback.print_exception(*exc_info)

def stack_merge(d1, d2, create_missing=False, exists=None):
    """
    This method merges a given dictionary structure with the stack
    It directly modifies the `stack` variable
    """
    path = {}
    exists = exists
    for k in d2.keys():
        if d1.get(k) is None:
            # neni tam, pridame:
            if create_missing:
                exists = False
                d1[k] = d2[k]
            else:
                return False
        else:
            # je tam, vnorime sa:
            if exists is None:
                exists = True
            if isinstance(d2[k], dict):
                exists = stack_merge(d1[k], d2[k], create_missing=create_missing, exists=exists)
    return exists

def compare_stack(components, create_missing=True):
    """
    This method merges a given dictionary structure with the stack
    It directly modifies the `stack` variable
    """
    tree = {}
    for comp in reversed(components):
        if comp == '()':
            continue
        if comp == components[-1]:
            tree = {"tests": [{"name": "comp", "item_id": ""}]}
        else:
            tree = {comp: {"children": tree, "item_id": ""}}
    return stack_merge(stack, tree, create_missing=create_missing)


service = ReportPortalServiceAsync(endpoint=endpoint, project=project, token=token, error_handler=my_error_handler)


def pytest_runtestloop(session):
    # Start launch.
    service.start_launch(name=launch_name, start_time=timestamp(), description=launch_doc)
    print(service.rp_client.launch_id)
    #set_trace()

def pytest_sessionfinish(session):
    service.finish_launch(end_time=timestamp())

def pytest_report_collectionfinish(config, startdir, items):
    for i in items:
        compare_stack(i.nodeid.split('::'), create_missing=True)

def pytest_runtest_logstart(nodeid, location):
    exists=compare_stack(nodeid.split('::'), create_missing=False)
    set_trace()
