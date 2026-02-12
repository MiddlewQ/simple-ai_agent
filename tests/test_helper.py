
def show(resp, expect_err=None, *, ok_key="result"):
    if resp.get("ok"):
        # print the main payload if it exists, otherwise print whole dict
        payload = resp.get(ok_key, None)
        if payload is None:
            print(resp)
            return

        if isinstance(payload, dict):
            if "content" in payload:
                print(payload["content"])
                if payload.get("truncated") is True:
                    print("(truncated)")
            elif "stdout" in payload or "stderr" in payload:
                out = payload.get("stdout", "")
                err = payload.get("stderr", "")
                if out: print(out, end="" if out.endswith("\n") else "\n")
                if err: print(err, end="" if err.endswith("\n") else "\n")
            else:
                print(payload)
        else:
            print(payload)
    else:
        err = resp.get("error", {})
        et = err.get("type")
        msg = err.get("message")
        print(f"ERR {et}: {msg}")
        if expect_err is not None and et != expect_err:
            print(f"(UNEXPECTED: expected {expect_err})")
