"""
Goal: Entry point to run server or client.
"""
def run_server():
    # TODO: Create KVServer instance
    # TODO: Call server.start()
    # TODO: Handle Ctrl+C gracefully
    pass

def run_client_example():
    # TODO: Create KVClient and connect
    # TODO: Test PUT, GET, DELETE operations
    # TODO: Print results
    # TODO: Close client
    pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        run_client_example()
    else:
        run_server()
