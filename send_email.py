import mimetypes
import smtplib
from email.message import EmailMessage
import configparser
from pathlib import Path


def guess_type(file):
    print("file: ", file)
    ctype, encoding = mimetypes.guess_type(file)
    print("with types: ", ctype)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)
    return (maintype, subtype)


config = configparser.ConfigParser()

config.read("./secrets/config.toml")

smtp_host = str(config["server"]["host"])
smtp_port = int(config["server"]["port"])

username = str(config["credentials"]["user"])
password = str(config["credentials"]["pass"])

directory = "./certs"
smtp = smtplib.SMTP(smtp_host, smtp_port)
smtp.starttls()  # for using port 587
smtp.login(username, password)

files = Path(directory).glob("*")

for file in files:
    to_user = file.name.removesuffix(".png")

    msg = EmailMessage()
    msg["Subject"] = "Certyfikat uczestnictwa Integralia 2022"
    msg["From"] = username
    msg["To"] = to_user
    html_content_path = Path("./text/text.html")
    html_types = guess_type(html_content_path)
    # Set email content
    with html_content_path.open("rb") as textb:
        msg.set_content(textb.read(), maintype=html_types[0], subtype=html_types[1])
    print(to_user)
    maintype, subtype = guess_type(file)
    with file.open("rb") as fb:
        msg.add_attachment(
            fb.read(),
            maintype=maintype,
            subtype=subtype,
            filename="Certyfikat Integralia 2022.png",
        )
    smtp.send_message(msg)

smtp.quit()
