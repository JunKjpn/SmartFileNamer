import FreeSimpleGUI as sg
import theme_repository

def input_themes(path):
    layout = [
        [sg.Text("追加するテーマ名を入力してください")],
        [sg.InputText(key="-theme-")],
        [sg.Text("登録されているテーマ一覧:")],
        [sg.Listbox(values=theme_repository.fetch_all(path=path), size=(30, 8), key="theme_list")],
        [sg.Button("Ok"), sg.Button("Cancel")],
    ]
    window = sg.Window("InputThemes", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            break

        elif event == "Ok":
            theme_name = values["-theme-"]
            if not theme_name:
                sg.popup("テーマ名が入力されていません。")
                continue

            try:
                theme_repository.add(path=path, name=theme_name)
                sg.popup("登録しました！")
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    sg.popup("同じ名前のテーマが既に登録されています")
                else:
                    sg.popup_error("DBエラー:", e)

            window["theme_list"].update(theme_repository.fetch_all(path=path))

    window.close()
