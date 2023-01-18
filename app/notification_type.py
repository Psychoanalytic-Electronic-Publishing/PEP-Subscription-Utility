import enum


class NotificationType(enum.Enum):
    Journal = 2
    Video = 3

    def get_pads_user_notification_types(user):
        user_notifications = []
        if user.get('SendJournalAlerts', False):
            user_notifications.append(NotificationType.Journal)
        if user.get('SendVideoAlerts', False):
            user_notifications.append(NotificationType.Video)
        return user_notifications
