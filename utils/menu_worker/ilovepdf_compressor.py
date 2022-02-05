import datetime
import os

from pylovepdf import Compress

from loader import dp


def get_public_key(date=datetime.date.today()) -> str:
    return dp.bot.get('config').misc.pdf_keys.key1 if int(str(date).split('-')[2]) % 2 == 0 else dp.bot.get(
        'config').misc.pdf_keys.key2


class PdfCompressor:

    def __init__(self, public_api_key=get_public_key()):
        self.compressor = Compress(public_api_key, verify_ssl=True, proxies=None)

    def compress_file(self, filepath, output_directory_path):
        self.compressor.add_file(filepath)
        self.compressor.compression_level = 'recommended'
        self.compressor.set_output_folder('./temp')
        self.compressor.execute()
        self.compressor.download()
        file_src = './temp/' + os.listdir('./temp')[0]
        file_destination = output_directory_path + '/' + os.path.basename(filepath)
        os.rename(file_src, file_destination)
        self.compressor.delete_current_task()
