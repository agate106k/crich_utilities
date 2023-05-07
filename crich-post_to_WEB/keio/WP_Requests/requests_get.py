import requests
import json

if __name__ == '__main__':
    url = 'https://crich-media.com/keio/wp-json/wp/v2/subject/'
    res = requests.get(url).json()
    # for data in res:
    #     print(data["title"])
    print(res[0])

    res_n = {
        'id': 5005,
        'date': '2021-03-28T14:49:52',
        'date_gmt': '2021-03-28T05:49:52',
        'guid': {'rendered': 'http://crichmediadev.local/?post_type=subject&#038;p=5005'},
        'modified': '2021-03-28T14:49:52',
        'modified_gmt': '2021-03-28T05:49:52',
        'slug': '%e8%8b%b1%e8%aa%9e%e7%ac%ac%e2%85%b1%ef%bc%8d%e3%83%ac%e3%83%99%e3%83%ab%ef%bc%92-6',
        'status': 'publish',
        'type': 'subject',
        'link': 'http://crichmediadev.local/subject/list/%e8%8b%b1%e8%aa%9e%e7%ac%ac%e2%85%b1%ef%bc%8d%e3%83%ac%e3%83%99%e3%83%ab%ef%bc%92-6/',
        'title': {'rendered': '英語第Ⅱ－レベル２'},
        'excerpt': {'rendered': '<p>履修情報は会員限定のコンテンツです。 閲覧するには下記よりログインをしてください。 会員登録をすると、口コミが満載の履修情報がご覧いただけます。 履修情報のサンプルはこちら ユーザー名またはメールアドレスパスワード&nbsp;ログイン状態を &#8230; </p>\n', 'protected': False},
        'author': 5,
        'featured_media': 0,
        'parent': 0,
        'template': '',
        'subject_faculty': [105, 148, 104, 144],
        'subject_feature': [204, 194, 198, 201, 192],
        'subject_teacher': [882],
        'acf': {
            'subject_term': '通年',
            'subject_eval': '3.5',
            'subject_module': '3',
            'subject_record': '5',
            'subject_interest': '5',
            'subject_hw': {
                'subject_hw_opinion': '毎回\t<br />\r\nエッセイ \t',
                'subject_hw_easy': '',
                'subject_hw_average': '1',
                'subject_hw_hard': ''
            },
            'subject_exam': {
                'subject_exam_opinion': '期末試験\t<br />\r\n論述・記述\t<br />\r\n持ち込み・参照不可',
                'subject_exam_easy': '',
                'subject_exam_average': '1',
                'subject_exam_hard': ''
            },
            'subject_class': {
                'subject_class_type': ['オンライン授業と対面授業の併用'],
                'subject_class_other': ''
            },
            'subject_attendance': ['オンライン講義への参加', '点呼（対面授業）'],
            'subject_mini_test': {
                'subject_mini_test_count': ['なし'],
                'subject_mini_test_difficulty': []
            },
            'subject_material': ['教科書', '配布資料（スライド、PDFなど）']
        },
        'data': {
            'subject_wom_item': ['2020年度は春オンデマンド(リスニング、リーディング中心)、秋対面とZOOM併用(ライティング中心)だったが、春は多忙で秋の負担は普通だったと思う。授業中に行うライティングアクティビティの配点がそこそこ高いが、資料は事前に.jpでアップロードされるため、英語が苦手な生徒は事前に取り組むことで対処出来る。毎回の課題がそこそこ時間を食うので楽とは言えないが、課題にさえ真面目に取り組めばA以上は来る印象(試験の配点が軽いため)。授業が英語で行われるので、課題が何か分からなかった！ということにはならないように注意。授業の内容は英語の技能を総合的に磨く上で有用と言えるものだと思った。'],
            'subject_advice_item': ['']
        },
        '_links': {
            'self': [{'href': 'http://crichmediadev.local/wp-json/wp/v2/subject/5005'}],
            'collection': [{'href': 'http://crichmediadev.local/wp-json/wp/v2/subject'}],
            'about': [{'href': 'http://crichmediadev.local/wp-json/wp/v2/types/subject'}],
            'author': [{'embeddable': True, 'href': 'http://crichmediadev.local/wp-json/wp/v2/users/5'}],
            'version-history': [{'count': 1, 'href': 'http://crichmediadev.local/wp-json/wp/v2/subject/5005/revisions'}],
            'predecessor-version': [{'id': 5006, 'href': 'http://crichmediadev.local/wp-json/wp/v2/subject/5005/revisions/5006'}],
            'wp:attachment': [{'href': 'http://crichmediadev.local/wp-json/wp/v2/media?parent=5005'}],
            'wp:term': [{
                'taxonomy': 'subject_faculty',
                'embeddable': True,
                'href': 'http://crichmediadev.local/wp-json/wp/v2/subject_faculty?post=5005'
            },
            {
                'taxonomy': 'subject_feature',
                'embeddable': True,
                'href': 'http://crichmediadev.local/wp-json/wp/v2/subject_feature?post=5005'
            },
            {
                'taxonomy': 'subject_teacher',
                'embeddable': True, 'href': 'http://crichmediadev.local/wp-json/wp/v2/subject_teacher?post=5005'
            }],
            'curies': [{'name': 'wp', 'href': 'https://api.w.org/{rel}', 'templated': True}]
        }
    }
