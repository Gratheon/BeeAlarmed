import os
import cgi
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

UPLOAD_DIR = 'uploads'

class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Add CORS headers to allow requests from any domain
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        if self.path == '/upload':
            content_type = self.headers.get('Content-Type')

            # Check if the request contains form data
            if 'multipart/form-data' not in content_type:
                self.wfile.write(b'Invalid request')
                return

            # Parse the form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            # Check if the 'video' field exists
            if 'video' not in form:
                self.wfile.write(b'No video file uploaded')
                return

            # Get the video file data
            video_file = form['video']
            _, file_extension = os.path.splitext(video_file.filename)
            timestamp = str(int(time.time()))  # Generate a timestamp
            filename = timestamp + file_extension

            # Save the file to the uploads directory
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, 'wb') as file:
                file.write(video_file.file.read())

            self.wfile.write(b'File uploaded successfully')
        else:
            self.wfile.write(b'Not found')

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    server_address = ('', 8900)
    httpd = ThreadingHTTPServer(server_address, UploadHandler)
    print('Server is listening on port 8900')
    httpd.serve_forever()
