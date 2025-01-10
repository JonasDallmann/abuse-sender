import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, Style, init

init(autoreset=True)

TEMPLATE_FOLDER = "templates"
CONFIG_FILE = "config.json"
SMTP_SERVER = ""
SMTP_PORT = 587
SMTP_USER = ""
SMTP_PASSWORD = ""

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Configuration file {CONFIG_FILE} not found.")
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def list_templates():
    templates = [f for f in os.listdir(TEMPLATE_FOLDER) if f.endswith(".txt")]
    return templates

def load_template(template_name):
    with open(os.path.join(TEMPLATE_FOLDER, template_name), "r") as file:
        return file.read()

def replace_placeholders(template_content, config):
    for key, value in config.items():
        placeholder = f"{{{{ {key} }}}}"
        template_content = template_content.replace(placeholder, value)
    while "{{" in template_content and "}}" in template_content:
        start = template_content.find("{{") + 2
        end = template_content.find("}}")
        placeholder = template_content[start:end].strip()
        user_input = input(f"{Fore.GREEN}[INPUT]{Style.RESET_ALL} Enter value for {placeholder}: ")
        template_content = template_content.replace(f"{{{{ {placeholder} }}}}", user_input)
    return template_content

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Email sent to {to_email}")

def main():
    config = load_config()
    print(f"{Fore.CYAN}Available Templates:{Style.RESET_ALL}")
    templates = list_templates()
    for idx, template in enumerate(templates, start=1):
        print(f"{idx}. {template}")
    print("")
    template_index = int(input(f"{Fore.GREEN}[INPUT]{Style.RESET_ALL} Select a template by number: ")) - 1
    if template_index < 0 or template_index >= len(templates):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid selection.")
        return
    clear_console()
    selected_template = templates[template_index]
    template_content = load_template(selected_template)
    final_content = replace_placeholders(template_content, config)
    clear_console()
    print(f"\n{Fore.CYAN}Preview of the Email:{Style.RESET_ALL} \n")
    print(final_content)
    confirm = input(f"\n{Fore.GREEN}[INPUT]{Style.RESET_ALL} Do you want to send this email? ({Fore.GREEN}yes{Style.RESET_ALL}/{Fore.RED}no{Style.RESET_ALL}): ").strip().lower()
    if confirm == "yes":
        to_email = input(f"{Fore.GREEN}[INPUT]{Style.RESET_ALL} Enter recipient's email address: ")
        subject = input(f"{Fore.GREEN}[INPUT]{Style.RESET_ALL} Enter subject for the email: ")
        send_email(to_email, subject, final_content)
    else:
        print(f"{Fore.RED}[ABORT] {Style.RESET_ALL}Email not sent.")

if __name__ == "__main__":
    clear_console()
    main()
