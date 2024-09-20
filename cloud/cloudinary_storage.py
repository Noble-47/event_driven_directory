import cloudinary.uploader
import cloudinary.api
import cloudinary

from base import CloudStorageService

class CloudinaryStorageService(CloudStorageService):

    def __init__(self, cloud_name, api_key, api_secret):
        cloudinary.config(
            cloud_name = cloud_name,
            api_key = api_key,
            api_secret = api_secret
        )

    def upload_file(self, file_content, file_name):
        response = cloudinary.uploader.upload(file_cntent, public_id=file_name)
        return response['secure_url']

    def get_file_url(self, file_name):
        return cloudinary.CloudinaryImage(file_name).build_url()

    def delete_file(self, file_name):
        response = cloudinary.uploader.destroy(file_name)
        return response['result']
