from .email import EmailNotificationChannel


NOTIFICATION_CHANNELS = {
    EmailNotificationChannel.type: EmailNotificationChannel(),
}
