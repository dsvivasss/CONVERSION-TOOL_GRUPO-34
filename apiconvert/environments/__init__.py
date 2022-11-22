import os

project_id = os.getenv('project-id', None)
if project_id is None:
    download_bucket_name='convert-song-v1'
    upload_bucket_name='original-song-v1'
    project_id='conversiontoolg34'
    file_topic_name='file-topic'
    email_topic_name='email-topic'
    zone='us-east4'
    instance_name='tool-conversion'
    db_user='postgres'
    db_password='root'
    db_name='tool-conversion-v1'
else:
    file_topic = os.getenv('file-topic', None)
    upload_bucket_name= os.getenv('upload-bucket-name', None)
    download_bucket_name= os.getenv('download-bucket-name', None)
    zone=os.getenv('zone', None)
    instance_name=os.getenv('instance-name', None)
    db_user=os.getenv('db-user', None)
    db_password=os.getenv('db-password', None)
    db_name=os.getenv('db-name', None)