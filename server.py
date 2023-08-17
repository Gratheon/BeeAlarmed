#!/usr/bin/env python3
from ImageProvider import ImageProvider
from ImageConsumer import ImageConsumer
from ImageExtractor import ImageExtractor
from LoRaWANThread import LoRaWANThread
from Visual import Visual
from Utils import get_args, get_config
import logging
import time
import sys
from Statistics import getStatistics

import os
import cgi
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

# Only load neural network if needed. the overhead is quite large
if get_config("NN_ENABLE"):
    from BeeClassification import BeeClassification

logging.basicConfig(level=logging.DEBUG, format='%(process)d %(asctime)s - %(name)s - %(levelname)s - \t%(message)s')
logger = logging.getLogger(__name__)


def main(video)->str:
    context = {
        'stats': getStatistics()
    }

    # Check input format: camera or video file
    # args = get_args()
    # if args.video:
    #     logger.info("Starting on video file '%s'" % (args.video))
    #     imgProvider = ImageProvider(context, video_file=args.video)
    # else:
    #     logger.info("Starting on camera input")
    #     imgProvider = ImageProvider(context, video_source=0)
    imgProvider = ImageProvider(context, video_file=video)

    while(not (imgProvider.isStarted() or imgProvider.isDone())):
        time.sleep(1)

    if imgProvider.isDone():
        logger.error("Aborted, ImageProvider did not start. Please see log for errors!")
        return ""

    # Enable bee classification process only when its enabled
    imgClassifier = None
    if get_config("NN_ENABLE"):
        imgClassifier = BeeClassification()

    # Create processes and connect message queues between them
    lorawan = None
    if get_config("RN2483A_LORA_ENABLE"):
        lorawan = LoRaWANThread()
    imgExtractor = ImageExtractor()
    imgConsumer = ImageConsumer(context)
    visualiser = Visual()
    imgConsumer.setContext(context)
    imgConsumer.setImageQueue(imgProvider.getQueue())
    imgConsumer.setVisualQueue(visualiser.getInQueue())
    if get_config("NN_ENABLE"):
        imgExtractor.setResultQueue(imgClassifier.getQueue())
        imgConsumer.setClassifierResultQueue(imgClassifier.getResultQueue())
    imgExtractor.setInQueue(imgConsumer.getPositionQueue())

    try:

        # Start the processes
        imgConsumer.start()
        imgExtractor.start()
        visualiser.start()
        if lorawan is not None:
            lorawan.start()

        # Quit program if end of video-file is reached or
        # the camera got disconnected
        #imgConsumer.join()
        while True:
            time.sleep(0.01)
            if imgConsumer.isDone() or imgProvider.isDone():
                raise SystemExit(0)

    except (KeyboardInterrupt, SystemExit):

        # Tear down all running process to ensure that we don't get any zombies
        if lorawan is not None:
            lorawan.stop()
        imgProvider.stop()
        imgExtractor.stop()
        visualiser.stop()
        imgConsumer.stop()
        if imgClassifier:
            imgClassifier.stop()
            imgClassifier.join()
        imgExtractor.join()
        imgProvider.join()
        visualiser.join()

    return context['stats'].readJSON()
# if __name__ == '__main__':
#     main()
#     logger.info('\n! -- BeeAlarmed stopped!\n')



UPLOAD_DIR = 'uploads'

class UploadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)  # Send 200 OK status code
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send the HTML form as the response body
        form_html = '''
        <html>
        <body>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" />
            <input type="submit" value="Upload" />
        </form>
        </body>
        </html>
        '''
        self.wfile.write(form_html.encode('utf-8'))

    def do_POST(self):
        # Add CORS headers to allow requests from any domain
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        # if self.path == '/upload':
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
        if 'file' not in form:
            self.wfile.write(b'No video file uploaded')
            return

        # Get the video file data
        video_file = form['file']
        _, file_extension = os.path.splitext(video_file.filename)
        timestamp = str(int(time.time()))  # Generate a timestamp
        filename = timestamp + file_extension

        # Save the file to the uploads directory
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, 'wb') as file:
            file.write(video_file.file.read())

        # self.wfile.write(b'File uploaded successfully')
        result = main(filepath)
        self.wfile.write(result.encode('utf-8'))
        # else:
        #     self.wfile.write(b'Not found')

if __name__ == '__main__':
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    server_address = ('', 9100)
    httpd = ThreadingHTTPServer(server_address, UploadHandler)
    print('Server is listening on port 9100')
    httpd.serve_forever()