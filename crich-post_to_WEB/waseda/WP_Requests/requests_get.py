import requests
import json
import csv
import ast
import base64
m = []
if __name__ == '__main__':
    url = 'https://crich-media.com/waseda/wp-json/wp/v2/subject/'
    res = requests.get(url).json()
    m.append(res)
    # for data in res:
    #     print(data["title"])
with open('original/webdata.csv', 'w') as f:
    writer = csv.writer(f)
    for x in m:
        writer.writerow(x)
    #
    # res_sample = {
    #     'id': 5098,
    #     'date': '2021-03-26T01:42:04',
    #     'date_gmt': '2021-03-25T16:42:04',
    #     'guid': {'rendered': 'http://crich-media.com/waseda/?post_type=subject&#038;p=5098'},
    #     'modified': '2021-03-26T01:42:04',
    #     'modified_gmt': '2021-03-25T16:42:04',
    #     'slug': '%e5%81%a5%e5%ba%b7%e3%82%b9%e3%83%9d%e3%83%bc%e3%83%84%e8%ab%9601',
    #     'status': 'publish',
    #     'type': 'subject',
    #     'link': 'https://crich-media.com/waseda/subject/list/%e5%81%a5%e5%ba%b7%e3%82%b9%e3%83%9d%e3%83%bc%e3%83%84%e8%ab%9601/',
    #     'title': {'rendered': '健康スポーツ論01'},
    #     'excerpt': {'rendered': '<p>履修情報は会員限定のコンテンツです。 閲覧するには下記よりログインをしてください。 会員登録をすると、口コミが満載の履修情報がご覧いただけます。 履修情報のサンプルはこちら ユーザー名またはメールアドレスパスワード&nbsp;ログイン状態を &#8230; </p>\n', 'protected': False},
    #     'author': 5,
    #     'featured_media': 0,
    #     'parent': 0,
    #     'template': '',
    #     'subject_faculty': [1060],
    #     'subject_feature': [55, 58, 60, 62, 68],
    #     'subject_teacher': [175],
    #     'acf': {
    #         'subject_term': '秋',
    #         'subject_eval': '2.5',
    #         'subject_module': '3',
    #         'subject_record': '3',
    #         'subject_interest': '2',
    #         'subject_hw': {
    #             'subject_hw_opinion': '毎回<br />\r\nレポート',
    #             'subject_hw_easy': '',
    #             'subject_hw_average': '1',
    #             'subject_hw_hard': ''
    #         },
    #         'subject_exam': {
    #             'subject_exam_opinion': 'レポート型の試験<br />\r\n記述・論述<br />\r\n持ち込み・参照可',
    #             'subject_exam_easy': '',
    #             'subject_exam_average': '1',
    #             'subject_exam_hard': ''
    #         },
    #         'subject_class': {
    #             'subject_class_type': ['オンデマンド配信'],
    #             'subject_class_other': ''
    #         },
    #         'subject_attendance': ['オンデマンド動画の視聴', 'オンライン上でのレビューシートへの回答'],
    #         'subject_mini_test': {
    #             'subject_mini_test_count': ['毎回'],
    #             'subject_mini_test_difficulty': ['普通']
    #         },
    #         'subject_material': ['配布資料（スライド、PDFなど）']
    #     },
    #     'data': {
    #         'subject_wom_item': ['毎回課題出してきてだるい', '内容がちょっと難しい'],
    #         'subject_advice_item': ['とりあえず期限内にレポート']
    #     },
    #     '_links': {
    #         'self': [{'href': 'https://crich-media.com/waseda/wp-json/wp/v2/subject/5098'}],
    #         'collection': [{'href': 'https://crich-media.com/waseda/wp-json/wp/v2/subject'}],
    #         'about': [{'href': 'https://crich-media.com/waseda/wp-json/wp/v2/types/subject'}],
    #         'author': [{'embeddable': True, 'href': 'https://crich-media.com/waseda/wp-json/wp/v2/users/10'}],
    #         'version-history': [{'count': 1, 'href': 'https://crich-media.com/waseda/wp-json/wp/v2/subject/5098/revisions'}],
    #         'predecessor-version': [{'id': 5102, 'href': 'https://crich-media.com/waseda/wp-json/wp/v2/subject/5098/revisions/5102'}],
    #         'wp:attachment': [{'href': 'https://crich-media.com/waseda/wp-json/wp/v2/media?parent=5098'}],
    #         'curies': [{'name': 'wp', 'href': 'https://api.w.org/{rel}', 'templated': True}]
    #     }
    # }
