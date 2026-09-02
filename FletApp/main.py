import flet as ft

def main(page: ft.Page):
    # ضبط أبعاد النافذة بحجم شاشة هاتف
    page.window.width = 390
    page.window.height = 700
    page.window.resizable = True
    
    page.title = "منظم المهام - Kanban Board"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def go_to_kanban(e):
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.padding = 10

        # قوائم احتواء المهام للأعمدة الثلاثة
        todo_tasks_column = ft.Column(spacing=10)
        in_progress_tasks_column = ft.Column(spacing=10)
        done_tasks_column = ft.Column(spacing=10)

        task_input = ft.TextField(hint_text="مهمة جديدة...", expand=True, dense=True)

        def add_task_click(e):
            if not task_input.value.strip():
                return

            task_text = task_input.value

            def move_to_done(card_ref):
                in_progress_tasks_column.controls.remove(card_ref)
                done_card = ft.Card(
                    content=ft.Container(
                        content=ft.Text(task_text, size=13),
                        padding=10
                    )
                )
                done_tasks_column.controls.append(done_card)
                page.update()

            def move_to_in_progress(card_ref):
                todo_tasks_column.controls.remove(card_ref)
                in_progress_card = ft.Card()
                in_progress_card.content = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(task_text, size=13, expand=True),
                            ft.Button("إنهاء", on_click=lambda _: move_to_done(in_progress_card))
                        ]
                    ),
                    padding=10
                )
                in_progress_tasks_column.controls.append(in_progress_card)
                page.update()

            todo_card = ft.Card()
            todo_card.content = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(task_text, size=13, expand=True),
                        ft.Button("بدء", on_click=lambda _: move_to_in_progress(todo_card))
                    ]
                ),
                padding=10
            )

            todo_tasks_column.controls.append(todo_card)
            task_input.value = ""
            page.update()

        add_button = ft.Button("إضافة", on_click=add_task_click)

        # حاويات متكيفة العرض تلقائياً بدون عرض ثابت
        col_todo = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=10,
            padding=12,
            content=ft.Column(
                controls=[
                    ft.Text("لم أبدأ بعد", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row(controls=[task_input, add_button]),
                    ft.Divider(),
                    todo_tasks_column
                ],
                spacing=8
            )
        )

        col_in_progress = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=10,
            padding=12,
            content=ft.Column(
                controls=[
                    ft.Text("قيد التنفيذ ⏳", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    in_progress_tasks_column
                ],
                spacing=8
            )
        )

        col_done = ft.Container(
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=10,
            padding=12,
            content=ft.Column(
                controls=[
                    ft.Text("مكتملة ✅", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    done_tasks_column
                ],
                spacing=8
            )
        )

        # التغيير الجوهري: استخدام Column بدلاً من Row وتفعيل التمرير الرأسي
        page.add(
            ft.Text("مهامك", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Column(
                controls=[col_todo, col_in_progress, col_done],
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
        )

    page.add(
        ft.Text("مرحبا في المنظم", size=22, weight=ft.FontWeight.BOLD),
        ft.Button("ابدأ التنظيم", on_click=go_to_kanban)
    )

ft.run(main)