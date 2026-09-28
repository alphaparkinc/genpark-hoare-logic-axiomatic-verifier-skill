from client import HoareLogicVerifier

verifier = HoareLogicVerifier()
post = "x > 10"
wp = verifier.verify_assignment(post, "x", "x + 1")
print(f"Weakest Precondition for '{post}' after 'x := x + 1': {wp}")
