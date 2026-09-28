import sys
import json
from client import HoareLogicVerifier

verifier = HoareLogicVerifier()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "weakest_precondition",
                        "description": "Compute weakest precondition wp(x := e, Q) for Hoare triple verification",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "postcondition": {"type": "string"},
                                "var_name": {"type": "string"},
                                "expr": {"type": "string"}
                            },
                            "required": ["postcondition", "var_name", "expr"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "weakest_precondition":
            wp = verifier.verify_assignment(args["postcondition"], args["var_name"], args["expr"])
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"postcondition": args["postcondition"], "weakest_precondition": wp})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
