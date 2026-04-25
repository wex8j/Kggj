import flet as ft

# كلاس الرسالة لترتيب البيانات
class Message:
    def __init__(self, user: str, text: str, type: str):
        self.user = user
        self.text = text
        self.type = type

def main(page: ft.Page):
    page.title = "دردشة تك | Chat Tech"
    page.rtl = True # دعم اللغة العربية
    page.theme_mode = ft.ThemeMode.DARK # وضع ليلي فخم
    page.bgcolor = "#1a1a1a"
    
    # دالة تحديث الرسائل لكل المستخدمين
    def on_message(msg: Message):
        if msg.type == "chat":
            chat_list.controls.append(
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(msg.user, weight="bold", color="#00ffcc", size=12),
                            ft.Text(msg.text, color="white", selectable=True),
                        ], spacing=2),
                        bgcolor="#2d2d2d",
                        padding=10,
                        border_radius=15,
                        width=250,
                    )
                ])
            )
        else:
            chat_list.controls.append(
                ft.Text(msg.text, italic=True, color="grey", size=12, text_align="center")
            )
        page.update()

    page.pubsub.subscribe(on_message)

    chat_list = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=10)

    # حقل الإرسال
    msg_input = ft.TextField(
        hint_text="اكتب رسالتك هنا...",
        expand=True,
        border_radius=20,
        on_submit=lambda _: send_click(None)
    )

    def send_click(e):
        if msg_input.value:
            page.pubsub.send_all(Message(page.session.get("username"), msg_input.value, "chat"))
            msg_input.value = ""
            page.update()

    # شاشة الدخول
    name_input = ft.TextField(label="اسم المستخدم", border_radius=10)

    def join_click(e):
        if name_input.value:
            page.session.set("username", name_input.value)
            page.dialog.open = False
            page.pubsub.send_all(Message(name_input.value, f"🔥 {name_input.value} انضم للدردشة الآن", "info"))
            
            page.add(
                ft.AppBar(title=ft.Text("دردشة تك"), center_title=True, bgcolor="#2d2d2d"),
                ft.Container(
                    content=chat_list,
                    expand=True,
                    padding=20,
                ),
                ft.Container(
                    content=ft.Row([msg_input, ft.IconButton(ft.icons.SEND_ROUNDED, on_click=send_click, icon_color="#00ffcc")]),
                    padding=10,
                    bgcolor="#2d2d2d"
                )
            )
            page.update()

    page.dialog = ft.AlertDialog(
        title=ft.Text("سجل دخولك في دردشة تك"),
        content=name_input,
        actions=[ft.ElevatedButton("دخول", on_click=join_click)],
        modal=True
    )
    page.dialog.open = True
    page.update()

# تشغيل التطبيق بوضعية الويب
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
