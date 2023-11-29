import http.server
import socketserver
import time

# Set the port number you want to use
port = 8000

# Define rate-limiting parameters
rate_limit_threshold = 5  # Maximum allowed requests per second
rate_limit_duration = 10  # Time window to check for rate limit violations in seconds

# Initialize rate-limiting variables
request_count = 0
start_time = time.time()

# Create a custom request handler to serve the index.html file
class RateLimitedRequestHandler(http.server.SimpleHTTPRequestHandler):
    def handle_request(self):
        global request_count, start_time

        # Check if the rate limit is exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time >= rate_limit_duration:
            request_count = 0
            start_time = time.time()

        request_count += 1

        if request_count > rate_limit_threshold:
            print("Possible attack detected! Rate limit exceeded.")
            print("Stopping the connection.")
            self.server.shutdown()
        else:
            super().handle_request()

# Create a socket server that listens on the specified port
with socketserver.TCPServer(("0.0.0.0", port), RateLimitedRequestHandler) as httpd:
    local_ip = "127.0.0.1"  # Local IP address of the machine
    url = f"http://{local_ip}:{port}"
    print(f"Serving on {url}")

    try:
        # Serve requests for a specified duration
        while time.time() - start_time < rate_limit_duration:
            httpd.handle_request()

    except KeyboardInterrupt:
        print("\nServer stopped by user.")
