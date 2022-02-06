import os
import random
import string

import requests
from bs4 import BeautifulSoup
from loguru import logger
from requests_toolbelt import MultipartEncoder

from data.config import SchoolSiteAuth, FilesConfig
from utils.db_api.sqlite_api import SchoolStorageItem


class SiteWorker(requests.Session):

    def __init__(self, site_auth: SchoolSiteAuth, folder_paths: FilesConfig):
        super(SiteWorker, self).__init__()
        self.folder_paths: FilesConfig = folder_paths
        self.base_url = site_auth.base_addr
        self.login = site_auth.login
        self.password = site_auth.password
        self.authorized = False
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'})
        while True:
            try:
                self.response = self.get(url=self.base_url)
                if self.response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                logger.info('WebSite is not allowed')
        while not self.authorized:
            while True:
                try:
                    self.response = self.get(url=self.base_url + '/login')
                    break
                except requests.exceptions.RequestException:
                    logger.info('Some trouble while authorization')
            self.csrf_token = BeautifulSoup(self.response.text, 'html.parser'). \
                find('input', dict(name='_csrf_token'))['value']
            self.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
            try:
                self.response = self.post(url=self.base_url + '/login_check', data={
                    '_csrf_token': self.csrf_token,
                    '_username': self.login,
                    '_password': self.password,
                    '_submit': 'Войти'
                })
            except requests.exceptions.RequestException:
                logger.info('Some trouble while authorization')
            if self.response.status_code == 200:
                self.authorized = True

    def get_file_info(self, base_url, filename) -> SchoolStorageItem:
        self.response = self.get(base_url + '/efconnect/files',
                                 params={
                                     'cmd': 'open',
                                     'target': SchoolStorageItem.get(name=filename).hash
                                 })
        if self.response.status_code == 200:
            for file in self.response.json().get('files'):
                SchoolStorageItem.get_or_create(
                    name=filename + '/' + file.get('name'),
                    hash=file.get('hash'),
                    mime=file.get('mime'),
                    parent_hash=file.get('phash'))
        if SchoolStorageItem.select(SchoolStorageItem).where(SchoolStorageItem.name == filename).count() > 0:
            return SchoolStorageItem.get(name=filename)
        else:
            return None

    def get_target_folder_id(self, base_url, folder_path) -> SchoolStorageItem:
        item: SchoolStorageItem
        try:
            item = SchoolStorageItem.get(name=folder_path)
        except:
            directory_path = folder_path.split('/')
            for i in range(1, len(directory_path) + 1):
                self.get_file_info(base_url, '/'.join(directory_path[:i]))
            return SchoolStorageItem.get(name=folder_path)
        return item

    def copy_tomorrow_today(self):
        dst_folder = self.get_target_folder_id(base_url=self.base_url,
                                               folder_path=self.folder_paths.today_folder_path)
        src_folder = self.get_target_folder_id(base_url=self.base_url,
                                               folder_path=self.folder_paths.tomorrow_folder_path)

        while True:
            try:
                self.response = self.get(url=self.base_url + '/efconnect/files', params={
                    'cmd': 'open',
                    'target': src_folder.hash
                })
            except requests.exceptions.RequestException:
                logger.info(f'Some trouble while uploading file copying files')
            if self.response.status_code == 200:
                break

        target_files = {item.get('name'): item.get('hash') for item in self.response.json().get('files')}

        for filename, hash_id in target_files.items():
            self.response = self.get(url=self.base_url + '/efconnect/files',
                                     params={
                                         'mode': '',
                                         'cmd': 'paste',
                                         'dst': dst_folder.hash,
                                         'targets[]': hash_id,
                                         'cut': 0,
                                         'src': src_folder.hash
                                     },
                                     headers={'Content-Type': 'application/json'})

    def delete_all_in_folder(self, folder_path):
        folder_info = self.get_target_folder_id(base_url=self.base_url, folder_path=folder_path)
        while True:
            try:
                self.response = self.get(url=self.base_url + '/efconnect/files', params={
                    'cmd': 'open',
                    'target': folder_info.hash
                })
            except requests.exceptions.RequestException:
                print('.', end='')
            if self.response.status_code == 200:
                break

        target_files = {item.get('name'): item.get('hash') for item in self.response.json().get('files')}
        for file_name, hash in target_files.items():
            self.response = self.get(url=self.base_url + '/efconnect/files', params={
                'cmd': 'rm',
                'targets[]': hash
            })

    def upload_files(self, folder_path, files):
        folder_info = self.get_target_folder_id(base_url=self.base_url, folder_path=folder_path)
        if folder_info:
            for file_path in files:
                self.process_uploading(folder_id=folder_info.hash, file_path=file_path)

    def process_uploading(self, folder_id, file_path):
        filename = os.path.basename(file_path)
        while True:
            try:
                self.response = self.get(url=self.base_url + '/efconnect/files', params={
                    'cmd': 'upload',
                    'target': folder_id
                })
            except requests.exceptions.RequestException:
                logger.info(f'Some trouble while uploading file {filename}')
            if self.response.status_code == 200:
                break
        multipart = MultipartEncoder(fields={
            'cmd': 'upload',
            'target': folder_id,
            'suffix': '~',
            'upload[]': (f'{filename}', open(file_path, 'rb'), 'application/pdf'),
            'uploading_path[]': ''
        }, boundary='----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16)))
        try:
            self.response = self.post(url=self.base_url + '/efconnect/files',
                                      data=multipart,
                                      headers={'Content-Type': multipart.content_type})
        except requests.exceptions.RequestException:
            logger.info(f'Some trouble while uploading file {filename}')
        if self.response.status_code == 200:
            return True


