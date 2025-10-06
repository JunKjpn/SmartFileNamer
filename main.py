import FreeSimpleGUI as sg
import popup, logic, db

# DBファイルのパス
db_path = r"\\swd19023\BC58_基盤技術\3520&3530共有\30_共通資料\ナレッジマネジメント\ファイル名統一\smartFileName.db"

_version_ = "1.0.0"
logic.check_update(version=_version_)
db.check(path=db_path)

layout = [
    [sg.Text("処理を選択してください。")],
    [sg.Button("ファイル名変更")],
    [sg.Button("ファイル名作成")],
    [sg.Button("性能ターゲット追加")],
]
window = sg.Window("SmartFileNamer", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "ファイル名変更":
        popup.rename_file(path=db_path)
    elif event == "ファイル名作成":
        popup.create_filename(path=db_path)
    elif event == "性能ターゲット追加":
        popup.input_targets(path=db_path)
window.close()
