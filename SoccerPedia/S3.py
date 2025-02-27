import boto3
from django.conf import settings


class S3:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

    def upload_photo(self,file_obj,flag):
        is_ai = False
        if flag == 'team':
            object_key = f"media/images/team_logos/{file_obj.name}"
        elif flag == 'league':
            object_key = f"media/images/league_logos/{file_obj.name}"
        elif flag == 'review':
            object_key = f"media/images/review_images/{file_obj.name}"
        if not is_ai:
            try:
                self.s3_client.upload_fileobj(
                    file_obj,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    object_key,
                    ExtraArgs={'ACL': 'public-read',
                               'ContentType': file_obj.content_type}
                )
                return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{object_key}"
            except Exception as e:
                print(e)

        if flag == 'ai_league':
            object_key = f"media/images/league_logos/{file_obj}"
        elif flag == 'ai':
            object_key = f"media/images/ai_images/{file_obj}"
        try:
            with open(file_obj,"rb") as file:
                self.s3_client.upload_fileobj(
                    file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    object_key,
                    ExtraArgs={'ACL': 'public-read'}
                )
                return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{object_key}"
        except Exception as e:
            print(e)

    def delete_photo(self,s3_key):
        s3_key = "media/" + str(s3_key)
        try:
            self.s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,Key=s3_key)
        except Exception as e:
            print(e)


