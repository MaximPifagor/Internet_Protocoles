import socket
from info import Info
from info import read_info_json_file
import json
import os.path
import ssl
import base64
import Lib.mimetypes
import argparse



def sendToServer(data, host, port):
    sock = socket.socket()
    sock = ssl.wrap_socket(sock)
    sock.connect((host, port))
    for mess in data:
        sock.sendall(mess.encode(encoding="utf-8"))
    answer = sock.recv(1024).decode(encoding="utf-8")
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--configs", help="JSON file's path (for more information look at readme)")
    args = parser.parse_args()
    info = read_info_json_file(args.configs)
    headers = create_message_headers(info)
    body = create_message_body(info)
    headers.append(body)
    print(sendToServer(headers, info.server, info.server_port))


def create_message_headers(info: Info):
    data_str = []
    data_str.append("EHLO " + info.sender + "\n")
    data_str.append("AUTH LOGIN " + "\n")
    data_str.append(encode_to_base64(info.sender) + '\n')
    data_str.append(encode_to_base64(info.password) + '\n')
    data_str.append("MAIL FROM: " + info.sender + "\n")
    data_str.append("RCPT TO: " + info.rcpt + "\n")
    data_str.append("DATA" + '\n')
    return data_str


def create_message_body(info: Info):
    mail = ""
    bounder = "b0"
    mail += f"Content-Type: multipart/mixed; boundary=\"{bounder}\"\n"
    mail += "MIME-Version: 1.0\n"
    mail += f"From: {info.sender}\n"
    mail += f"Subject: {info.subject}\n\n"
    mail += f"--{bounder}\n"
    mail += "Content-Type: text/plain; charset=utf-8\n\n"
    mail += read_mail(info.mail) + '\n'
    blocks = create_attachments_blocks(info.attachments)
    for block in blocks:
        mail += f"--{bounder}\n"
        mail += block
    mail += f"--{bounder}--\n"
    mail += ".\n"
    return mail


def read_mail(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        str = file.read()
    return str


def encode_to_base64(data):
    base64data = base64.b64encode(data.encode())
    base64data = base64data.decode()
    return base64data


def create_attachments_blocks(path):
    block = []
    con_type = "Content-Type: "
    con_dis = "Content-Disposition: attachment; filename="
    con_encoding = "Content-Transfer-Encoding: base64"
    attachments = read_attachments(path)
    for file in attachments:
        st, type, filename = file
        sub = ""
        sub += con_type + type + '\n'
        sub += con_dis + filename + "\n"
        sub += con_encoding + '\n\n'
        sub += st
        block.append(sub)

    return block


def read_attachments(path):
    attachments_as_bytes = []
    dir = os.listdir("test")
    for attachment in dir:
        with open(path + '\\' + attachment, "rb") as file:
            bytes = file.read()
            b64_bytes = base64.b64encode(bytes)
            string = b64_bytes.decode()
            type, r = file_mime_type(path + '\\' + attachment)
        attachments_as_bytes.append((string, type, attachment))
    return attachments_as_bytes


def file_mime_type(filename):
    return Lib.mimetypes.guess_type(filename, strict=True)


if __name__ == '__main__':
    main()
