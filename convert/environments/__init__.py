import os

project_id = os.getenv('project-id', None)
if project_id is None:
    project_id='conversiontoolg34'
    api_host= 'http://35.245.77.88:5001'
    file_sub_name = 'email-topic-sub'
    download_bucket_name='convert-song-v1'
    upload_bucket_name='original-song-v1'
else:
    api_host = os.getenv('api-host', None)
    file_sub_name = os.getenv('file-sub-name', None)
    upload_bucket_name= os.getenv('upload-bucket-name', None)
    download_bucket_name= os.getenv('download-bucket-name', None)