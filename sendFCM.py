from pyfcm import FCMNotification

def paytimePush(event, context):
    fcm = FCMNotification(api_key="API-KEY")
    _type = event.get("_type", False)

    tokens = event.get("tokens", [])
    msg = event.get("msg", "")
    msg_data = event.get("msg_data", {})

    if _type == "push":
        fcm.notify_multiple_devices(
                registration_ids=tokens,
                message_body=msg,
                data_message=msg_data,
                content_available=True,
                sound="default"
            )
    elif _type == "alert_chat":
        fcm.notify_multiple_devices(
                registration_ids=tokens,
                message_body=msg,
                message_title=event.get("message_title", ""),
                data_message=msg_data,
                content_available=True,
                sound="default")
    elif _type == "silent_chat":
        fcm.notify_multiple_devices(
                registration_ids=tokens,
                data_message=msg_data,
                content_available=True)
    return msg
