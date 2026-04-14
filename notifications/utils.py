from notifications.models import Notification


def create_notification(user, notification_type, message, link=None):
    """Helper to create a notification for a user."""
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        message=message,
        link=link,
    )


def notify_all_users(notification_type, message, link=None, exclude_user=None):
    """Broadcast a notification to all active users."""
    from accounts.models import User
    users = User.objects.filter(is_active=True)
    if exclude_user:
        users = users.exclude(pk=exclude_user.pk)
    notifications = [
        Notification(
            user=user,
            notification_type=notification_type,
            message=message,
            link=link,
        )
        for user in users
    ]
    Notification.objects.bulk_create(notifications)
