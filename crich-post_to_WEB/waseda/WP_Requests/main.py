from module.detect_unique_taxonomies import detect_unique_taxonomies

def main():
    path_new = 'waseda/WP_Requests/original/早稲田 履修情報入力フォーム 2022（回答） - フォームの回答 1.csv'
    path_master = 'WP_Requests/master/faculty_master.csv'
    type = 'teacher'

    unique_taxonomies = detect_unique_taxonomies(path_new, path_master, type)
    print(unique_taxonomies)

if __name__ == '__main__':
    main()
