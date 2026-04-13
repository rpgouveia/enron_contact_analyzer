from config import ENRON_DATABASE_PATH, SENT_FOLDER
from enron_pkg import load_emails, print_summary


def main():
    frequency = load_emails(ENRON_DATABASE_PATH, sent_folder=SENT_FOLDER)
    print_summary(frequency)


if __name__ == "__main__":
    main()