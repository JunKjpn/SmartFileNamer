import os
import datetime
import FreeSimpleGUI as sg
import db, logic


def make_labels():
    label_width = 13
    return [
        [sg.Text("日付選択:", size=(label_width, 1))],
        [sg.Text("報告会名:", size=(label_width, 1))],
        [sg.Text("ターゲット性能:", size=(label_width, 5))],
        [sg.Text("テーマ名:", size=(label_width, 1))],
        [sg.Text("バージョン:", size=(label_width, 1))]
    ]


def make_inputs(path):
    themes = db.fetch_all_targets(path=path)
    today = datetime.date.today().strftime("%Y%m%d")
    input_width = 30
    return [
        [sg.Input(today, key="-date-", size=(input_width, 1)),
         sg.CalendarButton("カレンダー", target="-date-", format="%Y%m%d")],
        [sg.InputText(key="-report-", size=(input_width, 1))],
        [sg.Listbox(values=themes, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(input_width, 5),
                    key="-target-")],
        [sg.InputText(key="-theme-", size=(input_width, 1)), sg.Button("過去テーマ参照")],
        [sg.InputText(key="-ver-", size=(input_width, 1))]
    ]


# 複数のファイル名を変更
def rename_file(path):
    # ファイル選択ダイアログ
    file_paths = sg.popup_get_file(
        "ファイルを選択してください(複数可)",
        file_types=(("すべてのファイル", "*.*"),),
        multiple_files=True
    )
    if not file_paths:
        return

    if isinstance(file_paths, str):
        file_paths = file_paths.split(";")

    for file_path in file_paths:
        labels = make_labels()
        inputs = make_inputs(path=path)
        layout = [
            [sg.Text(f"選択ファイル: {os.path.basename(file_path)}")],
            [sg.Column(labels, element_justification="right"), sg.Column(inputs)],
            [sg.Button("ファイル名変更"), sg.Button("Cancel")]
        ]
        window = sg.Window("ファイル名変更", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Cancel"):
                break
            elif event == "過去テーマ参照":
                selected = select_theme(path=path)
                if selected:
                    window["-theme-"].update(selected)
            elif event == "ファイル名変更":
                filename, error  = logic.get_filename(values=values)
                if error:
                    sg.popup(error)
                    continue
                ext = os.path.splitext(file_path)[1]  # 元ファイルの拡張子
                new_filename = f"{filename}{ext}"

                # ファイル名変更
                new_path = os.path.join(os.path.dirname(file_path), new_filename)
                try:
                    os.rename(file_path, new_path)
                    sg.popup(f"ファイル名を変更しました！\n{new_filename}")
                    break
                except Exception as e:
                    sg.popup_error("ファイル名変更に失敗しました:", e)
        window.close()


# 生成したファイル名を表示し、コピー
def show_filename(filename):
    layout = [
        [sg.Text("ファイル名を生成しました「Copy」ボタンからコピーしてください:")],
        [sg.InputText(filename, key="-filename-", size=(50,1), readonly=True)],
        [sg.Button("Copy"), sg.Button("Close")]
    ]
    window = sg.Window("ShowFileName", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Close"):
            break
        elif event == "Copy":
            sg.clipboard_set(filename)  # クリップボードにコピー
            sg.popup("コピーしました！")
            break
    window.close()


# ファイル名を生成
def create_filename(path):
    labels = make_labels()
    inputs = make_inputs(path=path)
    layout = [
        [sg.Column(labels, element_justification="right"), sg.Column(inputs)],
        [sg.Button("ファイル名生成"), sg.Button("Cancel")]
    ]
    window = sg.Window("ファイル名作成", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            break
        elif event == "過去テーマ参照":
            selected = select_theme(path=path)
            if selected:
                window["-theme-"].update(selected)
        elif event == "ファイル名生成":
            filename, error  = logic.get_filename(values=values)
            if error:
                sg.popup(error)
                continue
            db.add_themes(path=path, text=values["-theme-"])
            show_filename(filename=filename)
    window.close()


# ターゲット性能をDBに登録
def input_targets(path):
    admin_password = "0253"
    layout = [
        [sg.Text("追加するテーマ名を入力してください")],
        [sg.InputText(key="-theme-", size=(30, 8))],
        [sg.Text("管理用パスワードを入力してください")],
        [sg.InputText(key="-password-", password_char="*", size=(30, 8))],
        [sg.Text("登録されているテーマ一覧:")],
        [sg.Listbox(values=db.fetch_all_targets(path=path), size=(30, 8), key="theme_list")],
        [sg.Button("Ok"), sg.Button("Cancel")],
    ]
    window = sg.Window("InputThemes", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            break

        elif event == "Ok":
            theme_name = values["-theme-"]
            password = values["-password-"]
            if not theme_name:
                sg.popup("テーマ名が入力されていません。")
                continue
            if not password:
                sg.popup("パスワードが入力されていません。")
                continue
            if password != admin_password:
                sg.popup("パスワードが間違っています。")
                continue

            try:
                db.add_targets(path=path, name=theme_name)
                sg.popup("登録しました！")
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    sg.popup("同じ名前のテーマが既に登録されています")
                else:
                    sg.popup_error("DBエラー:", e)

            window["theme_list"].update(db.fetch_all_targets(path=path))
            window["-theme-"].update("")

    window.close()

def select_theme(path):
    themes = db.fetch_all_themes(path=path)
    if not themes:
        sg.popup("登録されているテーマはありません。")
        return None

    layout = [
        [sg.Text("入力するテーマを選択してください")],
        [sg.Listbox(values=themes, size=(30, 10), key="-THEME-", enable_events=True)],
        [sg.Button("OK"), sg.Button("Cancel")]
    ]
    window = sg.Window("テーマ選択", layout)

    selected_theme = None
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            break
        elif event == "OK":
            if values["-THEME-"]:
                selected_theme = values["-THEME-"][0]  # 選択されたテーマ
                break
            else:
                sg.popup("テーマを選択してください")
    window.close()
    return selected_theme

if __name__ == "__main__":
    db_path = r"\\swd19023\BC58_基盤技術\3520&3530共有\30_共通資料\ナレッジマネジメント\ファイル名統一\smartFileName.db"
    create_filename(path=db_path)
