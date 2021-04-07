import os
import glob
import traceback
import sys
from app.utilities import file_utility, pads_utility, email_utility


def handler(event, context):
    print(event)
    for record in event['Records']:
        try:
            # get article files from s3 and parse
            download_path = file_utility.download_subscription_file(record)
            unzipped_path = file_utility.unzip(download_path)
            update_data = file_utility.parse_subscription_files(unzipped_path)

            # get users from pads to send new articles to
            pads_users = pads_utility.get_pads_users()

            # send emails to pads users based on their subscription types
            email_utility.send_issue_update_emails(pads_users, update_data)
        except Exception as e:
            print(f'ERROR Unable to send PEP subscription notification messages: {e}')
            traceback.print_exception(*sys.exc_info())
        finally:
            try:
                print(os.system('rm -rf /tmp/*'))
                print(os.listdir('/tmp/'))
            except Exception as e:
                print(f'Error cleaning up files: {e}')

