from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client, get_tracker_conf
from django.conf import settings


class FDFSStroage(Storage):

    def __init__(self, client_conf=None, base_url=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF

        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL

        self.base_url = base_url

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        # name: filename, content: File object

        tracker_path = get_tracker_conf(self.client_conf)
        client = Fdfs_client(tracker_path)

        res = client.upload_by_buffer(content.read())
        '''
        @return dict {
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,
            'Status'          : 'Upload successed.',
            'Local file name' : '',
            'Uploaded size'   : upload_size,
            'Storage IP'      : storage_ip
        } if success else None
        '''
        if res.get('Status') != 'Upload successed.':
            raise Exception('upload to fastdfs fails')

        filename = res.get('Remote file_id')

        return filename.decode()

    def exists(self, name):

        return False

    def url(self, name):

        return self.base_url + name
