import datetime
import email
import imaplib
import shlex
from dataclasses import dataclass
from email.header import decode_header, make_header

from utils.menu_worker.imaputf7 import imaputf7decode, imaputf7encode


@dataclass
class File:
    filename: str
    content: bytes


@dataclass
class MessageSubject:
    theme: str
    uk: str
    date: datetime.datetime


@dataclass
class Message:
    id: int
    subject: MessageSubject
    date: datetime.datetime
    from_user: str
    file: File


class MailWorker:
    auth_status: bool
    folders_list: list
    messages: list

    def __init__(self, server, login, password, save_dir, menu_folder_name):
        self.server = server
        self.mail = imaplib.IMAP4_SSL(self.server)
        self.save_dir = save_dir
        self.menu_folder_name = menu_folder_name
        status = ''
        try:
            status, message = self.mail.login(login, password)
        except Exception:
            self.auth_status = False
        if status == 'OK':
            self.auth_status = True
        else:
            self.auth_status = False

    @staticmethod
    def get_message_subject(subject: str):
        fields = subject.replace('  ', ' ').split(' ')
        if len(fields) == 3:
            date = fields[2].rstrip('.pdf').split('.')
            if len(date) == 3 and len(date[2]) == 4:
                return MessageSubject(
                    theme=subject.split(' ')[0].upper().rstrip('.pdf'),
                    uk='UK' + subject.rstrip('.pdf').upper().split(' ')[1].split('УК')[-1],
                    date=datetime.datetime.strptime(subject.rstrip('.pdf').split(' ')[-1], "%d.%m.%Y")
                )
        else:
            return None

    def get_folder_list(self):
        status, folder_list = self.mail.list()
        if status == 'OK':
            self.folders_list = [shlex.split(imaputf7decode(folder.decode()))[-1] for folder in folder_list]
            return True
        else:
            return False

    def select_folder(self, folder_name):
        status, data = self.mail.select(imaputf7encode(folder_name))
        if status == 'OK':
            return True
        else:
            return False

    def get_messages_from_folder(self):
        status, data = self.mail.search(None, "ALL")
        if not status == 'OK':
            return False
        self.messages = list()
        ids = data[0].split()
        for i in range(len(ids) - 1, -1, -1):
            self.messages += self.process_message(id=ids[i])
        return True

    def complete_message(self, id, message, part):
        subject = self.get_message_subject(str(make_header(decode_header(message['Subject']))))
        if subject:
            return Message(
                id=id,
                subject=subject,
                date=datetime.datetime.strptime(
                    str(make_header(decode_header(message['Date']))), '%a, %d %b %Y %H:%M:%S %z'
                ),
                from_user=str(make_header(decode_header(message['From']))),
                file=File(filename=part.get_filename(),
                          content=part.get_payload(decode=True))
            )
        return None

    def process_message(self, id):
        status, data = self.mail.fetch(id, "(RFC822)")
        messages = list()
        if status == 'OK':
            raw_message = data[0][1].decode('utf-8')
            message = email.message_from_string(raw_message)
            for part in message.walk():
                if 'application' in part.get_content_type().split('/'):
                    complete_message = self.complete_message(id=id,
                                                             message=message,
                                                             part=part)
                    if complete_message:
                        messages.append(complete_message)
            return messages
        return list()

    def disconnect(self) -> None:
        self.get_folder_list()
        self.select_folder(self.menu_folder_name)
        status, data = self.mail.search(None, "ALL")
        if status == 'OK':
            ids = data[0].split()
            for i in range(len(ids) - 1, -1, -1):
                cur_id = ids[i]
                self.mail.copy(cur_id, imaputf7encode('Выложено'))
                self.mail.store(cur_id, '+FLAGS', '\Deleted')
        self.mail.expunge()
        self.mail.close()
        self.mail.logout()
