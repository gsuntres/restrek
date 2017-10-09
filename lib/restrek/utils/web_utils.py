
def is_json(headers=dict()):
    for header in headers.keys():
        if 'application/json' in headers[header]:
            return True

    return False
