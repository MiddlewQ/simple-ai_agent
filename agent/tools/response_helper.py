
def response_ok(result, **meta):
    out = {'ok': True, "result": result}
    if meta:
        out["meta"] = meta
    return out 

def response_error(error_type, message, result = None, **meta):
    out = {'ok': False, "error": {"type": error_type, "message": message}}
    if result is not None:
        out["result"] = result
    if meta:
        out["meta"] = meta
    return out