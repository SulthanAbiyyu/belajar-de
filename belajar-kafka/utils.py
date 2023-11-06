from minio import Minio
from minio.error import S3Error
import io
import os

class MinioBasicOperator:
    def __init__(self, endpoint, access_key, secret_key, bucket_name=None):
        self.client = Minio(
            endpoint = endpoint,
            access_key= access_key,
            secret_key= secret_key,
        )
        self.bucket_name = bucket_name
    
    def upload_json(self, data, object_name, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        
        try:
            with io.BytesIO() as file:
                file.write(json.dumps(data).encode())
                file.seek(0)
                self.client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name,
                    data=file,
                    length=len(file.getvalue()),
                    content_type="application/json",
                )
        except S3Error as exc:
            print("error occurred.", exc)
    
    def upload_anydata(self, data, object_name, bucket_name=None, content_type=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        
        try:
            with io.BytesIO() as file:
                file.write(data.encode())
                file.seek(0)
                self.client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name,
                    data=file,
                    length=len(file.getvalue()),
                    content_type=content_type,
                )
        except S3Error as exc:
            print("error occurred.", exc)

    def ls(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
            
        response = self.client.list_objects(bucket_name=bucket_name)
        try:
            objs = []
            for i in response:
                objs.append(i.object_name)
            return objs
        except S3Error as exc:
            print("error occurred.", exc)
    
    def ls_all(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
            
        response = self.client.list_objects(bucket_name=bucket_name, recursive=True)
        try:
            objs = []
            for i in response:
                objs.append(i.object_name)
            return objs
        except S3Error as exc:
            print("error occurred.", exc)
    
    def ls_dir(self, dir, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
            
        response = self.client.list_objects(bucket_name=bucket_name, prefix=dir)
        try:
            objs = []
            for i in response:
                objs.append(i.object_name)
            return objs
        except S3Error as exc:
            print("error occurred.", exc)

    def get_file(self, object_name, file_path, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        try:
            self.client.fget_object(
                bucket_name=bucket_name,
                object_name=object_name,
                file_path=file_path,
            )
        except S3Error as exc:
            print("error occurred.", exc)
        
        if os.path.isfile(file_path):
            return True
        else: 
            return False

    def get_json(self, object_name, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        response = self.client.get_object(
            bucket_name=bucket_name,
            object_name=object_name,
        )
        hasil = response.read().decode()
        response.close()
        response.release_conn()
        
        return hasil

    def mkbuck(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
            
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

        buckets = self.client.list_buckets()
        for bucket in buckets:
            print(bucket.name, bucket.creation_date)
    
    def rm_file(self, object_name, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        try:
            self.client.remove_object(
                bucket_name=bucket_name,
                object_name=object_name,
            )
        except S3Error as exc:
            print("error occurred.", exc)
    
    def rm_buck(self, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        try:
            self.client.remove_bucket(bucket_name)
        except S3Error as exc:
            print("error occurred.", exc)
    
    def rm_lists(self, remove_list, bucket_name=None):
        if bucket_name is None:
            bucket_name = self.bucket_name
        try:
            for i in remove_list:
                self.client.remove_object(bucket_name, i)
        except S3Error as exc:
            print("error occurred.", exc)