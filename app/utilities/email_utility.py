import boto3
import os
import typing
from app.notification_type import NotificationType
from app.exceptions.no_issue_updates_exception import NoIssueUpdatesException
from botocore.exceptions import ClientError

ses_client = boto3.client('ses')

video_journals = ['AFCVS', 'BPSIVS', 'IJPVS', 'IPSAVS',
                  'NYPSIVS', 'PCVS', 'PEPGRANTVS', 'PEPTOPAUTHVS',
                  'PEPVS', 'SFCPVS', 'SPIVS', 'UCLVS']


def send_issue_update_emails(pads_users: str, update_data):
    email_subject = os.environ.get('EMAIL_SUBJECT_ISSUE_NOTIFICATIONS')
    issue_html_by_notification_type = get_issue_html_by_notification_type(update_data)
    if (len(issue_html_by_notification_type)) == 0:
        print('No updates to send')
        return

    for user in pads_users:
        try:
            formatted_email = get_formatted_email(
                issue_html_by_notification_type,
                NotificationType.get_pads_user_notification_types(user))

            print(f'Sending notification to {user.get("EmailAddress", "")}. journal {user.get("SendJournalAlerts", "")}, video {user.get("SendVideoAlerts", "")}')
            send_email(user.get('EmailAddress', ''), email_subject, formatted_email)

        except NoIssueUpdatesException as niue:
            print(niue)
        except Exception as e:
            print(f'Error creating and sending emails: {e}')


def send_email(to_address: list, subject: str, body: str):
    try:
        ses_client.send_email(
            Destination={
                'ToAddresses': [to_address]
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    }
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=os.environ.get('EMAIL_FROM_ADDRESS')
        )
    except ClientError as e:
        print(f'Error sending email: {e}')


def get_formatted_email(issue_html_by_notification_type: dict, user_notifcation_types: list) -> str:
    web_url = os.environ.get('WEB_URL')
    logo_image_url = os.environ.get('LOGO_IMAGE_URL')

    issue_updates = ''
    for notification_type in issue_html_by_notification_type:
        if notification_type in user_notifcation_types:
            issue_updates += issue_html_by_notification_type[notification_type]

    if issue_updates == '':
        raise NoIssueUpdatesException()

    unsubscribe_text = unsubscribe_template.format(
        unsubscribe_url=f'{web_url}?openNotificationModal=true')

    return message_body_template.format(
        pep_logo=f'{logo_image_url}/banner-alert.jpg',
        issue_updates=issue_updates,
        unsubscribe_template=unsubscribe_text
    )


def get_issue_html_by_notification_type(update_data) -> dict:
    logo_image_url = os.environ.get('LOGO_IMAGE_URL')
    issue_html_by_notification_type = {}

    for issue in update_data:
        issue_id=issue.find('issue_id/src').text
        issue_updates = issue_template.format(
            logo_image_url=f'{logo_image_url}/banner{issue_id}Logo.gif',
            alt_text=f'{issue_id}',
            articles_section_html=get_articles_section_html(issue.find('articles')))

        # TODO currently _PEPCurrent is using a single loader so we shouldn't have new journals split up, but might need to revisit this.
        issue_type = NotificationType.Video if issue_id in video_journals else NotificationType.Journal
        issue_html_by_notification_type[issue_type] = issue_html_by_notification_type.get(issue_type, '') + issue_updates
        print(f'processing issue src: {issue_id}, type: {issue_type}')
    return issue_html_by_notification_type


def get_articles_section_html(articles) -> str:
    web_url = os.environ.get('WEB_URL')
    articles_html = ''
    for article in articles:
        articles_html += article_template.format(
            article_url=f'{web_url}/search/document/{article.attrib["id"]}',
            reference_string=build_reference_string(article)
        )
    return articles_html


def build_reference_string(article) -> str:
    article_data = article.find('p').findall('span')
    return "{authors} ({year}). {title}. {sourcetitle}, {pgrg1}:{pgrg2}.".format(
        authors=get_field_from_article(article_data, "authors", 0),
        year=get_field_from_article(article_data, "year", 1),
        title=get_field_from_article(article_data, "title", 2),
        sourcetitle=get_field_from_article(article_data, "sourcetitle", 3),
        pgrg1=get_field_from_article(article_data, "pgrg", 4),
        pgrg2=get_field_from_article(article_data, "pgrg", 5)
    )


def get_field_from_article(article_data, class_type: str, expected_index: int) -> str:
    # try getting by index first before falling back to iteration since it looks like they're always in order
    text = ""
    if article_data[expected_index].attrib.get('class') == class_type:
        text = article_data[expected_index].text
    else:
        for item in article_data:
            if item.attrib.get('class') == class_type:
                text = item.text
    return text if text is not None else ""


message_body_template = """
<html>
    <body>
        <div>
            <p class="MsoNormal" style="margin-right:0in;margin-bottom:9.0pt;margin-left:0in">
            <span style="font-size:10.0pt;font-family:&quot;Arial&quot;,sans-serif">
            <img border="0" src="{pep_logo}" alt="PEP-Web: A Psychoanalytic Library at your Fingertips"></span></p>
            <span style="font-family:&quot;Arial&quot;,sans-serif">Announcing New Content on PEP-Web!</span><u></u><u></u></p>
        </div>
        <p>
        {issue_updates}
        </p>
        <p>
        {unsubscribe_template}
        </p>
    </body>
</html>
"""

issue_template = """
    <div>
        <p style="margin-right:0in;margin-bottom:9.0pt;margin-left:0in">
            <span style="font-size:10.0pt;font-family:&quot;Arial&quot;,sans-serif">
                <img border="0" src="{logo_image_url}"" alt="{alt_text}">
            </span>
        </p>
        {articles_section_html}
    </div>
"""

article_template = """
    <p style="margin-right:0in;margin-bottom:9.0pt;margin-left:0in">
        <span style="font-size:10.0pt;font-family:&quot;Arial&quot;,sans-serif">
            <a href="{article_url}"> {reference_string} </a>
        </span>
    </p>
"""

unsubscribe_template = """
    <div>
        <span style="font-size:10.0pt;font-family:&quot;Arial&quot;,sans-serif">
            <hr size="2" width="400" style="width:300.0pt" align="left">
        </span>

        <p style="margin-right:0in;margin-bottom:9.0pt;margin-left:0in">
            <span style="font-size:10.0pt;font-family:&quot;Arial&quot;,sans-serif">
            You are receiving this message because you subscribed to new content alerts from PEP-Web. To unsubscribe from these alerts or to change your email address
            <a href="{unsubscribe_url}">click here</a>.</span>
        </p>
    </div>
"""