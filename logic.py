import FreeSimpleGUI as sg

def check_update(version):
    version_file = r"\\swd19023\BC58_基盤技術\3520&3530共有\30_共通資料\ナレッジマネジメント\ファイル名統一\latest_version.txt"
    try:
        with open(version_file, encoding="utf-8") as f:
            latest_version = f.read().strip()
        if latest_version != version:
            sg.popup(f"新しいバージョン（{latest_version}）があります！\n現在のバージョン: {version}")
    except Exception as e:
        # ファイルが見つからない、権限がない等は無視
        pass


def combine_values(values):
    return {
        "date": values.get("-date-", ""),
        "report": values.get("-report-", ""),
        "targets": values.get("-target-", []),
        "theme": values.get("-theme-", ""),
        "ver": values.get("-ver-", ""),
    }


def validate_values(values):
    if values["date"] == "" or values["report"] == "" or not values["targets"] or values["theme"] == "" or values["ver"] == "":
        return False, "すべての項目を入力・選択してください"
    if not (values["ver"].isdigit() or values["ver"].lower() == "vf"):
        return False, "バージョンは数字または 'vf' のみ入力してください"
    return True, ""


def make_filename(values):
    targets_str = "#" + "#".join(values["targets"]) if values["targets"] else ""
    return f"{values["date"]}_{values["report"]}_{targets_str}_{values["theme"]}_{values["ver"]}"


def get_filename(values):
    values = combine_values(values=values)
    valid, msg = validate_values(values=values)
    if not valid:
        return None, msg
    filename = make_filename(values=values)
    return filename, None
