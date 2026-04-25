import flet as ft

# كلاس يمثل الرسالة (الاسم والرسالة والنوع)
class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

def main(page: ft.Page):
    page.title = "دردشة تك - Chat Tech"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True  # لدعم اللغة العربية من اليمين لليسار

    # دالة لاستلام الرسائل وتحديث الواجهة
    def on_message(msg: Message):
        if msg.message_type == "chat_message":
            chat_messages.controls.append(ft.Text(f"{msg.user_name}: {msg.text}"))
        elif msg.message_type == "login_message":
            chat_messages.controls.append(
                ft.Text(msg.text, italic=True, color=ft.colors.GREY_400, size=12)
            )
        page.update()

    # الاشتراك في نظام البث التلقائي (PubSub)
    page.pubsub.subscribe(on_message)

    # قائمة الرسائل
    chat_messages = ft.Column()

    # حقل إدخال الرسالة
    new_message = ft.TextField(
        hint_text="اكتب رسالتك هنا...",
        autofocus=True,
        shift_enter=True,
        expand=True,
        on_submit=lambda e: send_message_click(e)
    )

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, "chat_message"))
            new_message.value = ""
            new_message.focus()
            page.update()

    # حوار تسجيل الدخول
    user_name_field = ft.TextField(label="أدخل اسمك المستعار")

    def join_chat_click(e):
        if not user_name_field.value:
            user_name_field.error_text = "الاسم مطلوب!"
            page.update()
        else:
            page.session.set("user_name", user_name_field.value)
            page.dialog.open = False
            page.pubsub.send_all(Message(user_name_field.value, f"انضم {user_name_field.value} إلى الدردشة", "login_message"))
            page.add(
                ft.Column(
                    [
                        ft.Container(
                            content=chat_messages,
                            height=500,
                            expand=True,
                            scroll=ft.ScrollMode.ALWAYS,
                        ),
                        ft.Row([new_message, ft.IconButton(icon=ft.icons.SEND, on_click=send_message_click)])
                    ],
                    expand=True
                )
            )
            page.update()

    page.dialog = ft.AlertDialog(
        title=ft.Text("مرحباً بك في دردشة تك"),
        content=user_name_field,
        actions=[ft.ElevatedButton("دخول", on_click=join_chat_click)],
        modal=True,
    )
    page.dialog.open = True
    page.update()

ft.app(target=main)
