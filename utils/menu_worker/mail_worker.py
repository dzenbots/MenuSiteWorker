import imaplib

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
        except:
            self.auth_status = False
        if status == 'OK':
            self.auth_status = True
        else:
            self.auth_status = False