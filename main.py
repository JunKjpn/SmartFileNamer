import FreeSimpleGUI as sg
import popup

# DBファイルのパス
# db_path = r"\\swd19023\BC58_基盤技術\3520&3530共有\30_共通資料\ナレッジマネジメント\themes.db"
db_path = r"themes.db"

layout = [
    [sg.Button("ファイル名変更")],
    [sg.Button("ファイル名作成")],
    [sg.Button("テーマ追加")],
]
window = sg.Window("SmartFileNamer", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "テーマ追加":
        popup.input_themes(path=db_path)
window.close()
