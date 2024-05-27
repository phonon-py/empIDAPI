import flet as ft
import requests

def main(page: ft.Page):
    page.title = "名前の入力"

    def on_submit(e):
        name = name_input.value
        response = requests.post("http://localhost:8000/submit", json={"name": name})
        if response.status_code == 200:
            result_text.value = "名前をデータベースに保存しました"
            update_names_list()
        else:
            result_text.value = "エラーが発生しました"
        page.update()

    def update_names_list():
        response = requests.get("http://localhost:8000/names")
        if response.status_code == 200:
            names = response.json()
            names_list.controls = [ft.Text(name["name"]) for name in names]
        else:
            names_list.controls = [ft.Text("エラーが発生しました")]
        page.update()

    name_input = ft.TextField(label="氏名")
    submit_button = ft.ElevatedButton(text="送信", on_click=on_submit)
    result_text = ft.Text()
    names_list = ft.Column()

    page.add(ft.Column([name_input, submit_button, result_text, ft.Text("データベース内の名前一覧:"), names_list]))

    update_names_list()

ft.app(target=main, view=ft.WEB_BROWSER)  # Webブラウザで起動