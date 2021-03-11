from concurrent.futures import Future
fut = Future()
print(fut)
fut.set_result("hello")
print(fut)

print(fut.result())