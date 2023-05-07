import csv

def detect_unique_taxonomies(path_new, path_master, type):
    """
    新しく集めた履修情報とデータベースに登録してあるParams[type]のタクソノミーの差分を検出しまとめる。

    Parameters
    ----------
    path : str
        新しく集めた履修情報のpath
    type : 'faculty' | 'teacher'
        タイプによって検出するタクソノミーを分ける

    Returns
    -------
    unique_taxonomies : list
        データベースにあるものと重複しない新しいParams[type]のタクソノミー

    Attributes
    ----------
    new_taxonomies : list<str>
        履修情報にあるParams[type]のリスト
    taxonomy_master : list<list<str>>
        既に登録されているParams[type]と対応するidのタクソノミーマスター

    """

    new_taxonomies = []
    taxonomy_master = []
    unique_taxonomies = []

    # 新規新規履修情報のParams[type]読み込み
    with open(path_new) as f:
        reader = csv.reader(f)
        # Google Formの場合はheaderを飛ばす
        header = next(reader)

        if type == 'faculty':
            new_taxonomies = list({row[4] for row in reader if row[4] != '' and len(row) > 15})
        elif type == 'teacher':
            new_taxonomies = list({row[3] for row in reader if row[3] != '' and len(row) > 15})

        f.close()

    # 既存のParams[type]タクソノミー読み込み
    with open(path_master) as f:
        reader = csv.reader(f)

        taxonomy_master = [row[0] for row in reader if row[0] != '']

        f.close()

    # setを用いるとデータベースにのみあるタクソノミーも含まれるのでfor文で
    for taxonomiy in new_taxonomies:
        if taxonomiy not in taxonomy_master:
            unique_taxonomies.append(taxonomiy)


    return unique_taxonomies