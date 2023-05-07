import requests
import json
import csv
import ast
import base64

if __name__ == '__main__':
    ### 投稿に必要な情報 ###
    # ユーザーID
    user_id = "Crich"
    # # APIパスワード
    # password = '45Td hJot DJ3s gPfo wS0i h6Cc'
    # # リクエストURL
    # end_point_url = 'http://crichmediadev.local/wp-json/wp/v2/subject'

    # # dev用
    password = 'kzzg 5bHt TjDq v30U 6Bvk msYH'
    end_point_url = 'https://localhost:10008/wp-json/wp/v2/subject/'
    # 本番用
    # password = "VdGK Xi5y Fnym UDBY 9BJK d1tZ"
    # end_point_url = "https://crich-media.com/waseda/wp-json/wp/v2/subject/"

    surveies = []
    with open('classified/classified_survey_dev.csv') as f:
        reader = csv.reader(f)
        surveies = [row for row in reader]

    for survey in surveies:
        ### パラメータ ###
        # タイトル
        title = survey[1] + survey[3]

        # 公開状態
        status = 'publish'

        # コメントの状態
        comment_status = 'closed'

        payload = {
            "title": title,
            "terms": {
                # 各タクソノミーのidをintで
                "subject_faculty": ast.literal_eval(survey[17]),
                "subject_feature": ast.literal_eval(survey[18]),
                "subject_teacher": ast.literal_eval(survey[16])
            },
            "data": {
                "subject_wom_item": ast.literal_eval(survey[15]),
                "subject_advice_item": []
            },
            "status": status,
            "comment_status": comment_status
        }

        # 投稿
        headers = {'content-type': "Application/json"}
        res = requests.post(end_point_url, data=json.dumps(payload) , headers=headers, auth=(user_id, password))
        post_id = str(json.loads(json.dumps(json.loads(res.content.decode('utf8').replace("'", '"'))))['id'])

        # 201が表示されれば成功
        print(res.status_code)
        if res.status_code == 201:
            print('post id is ' + post_id)
            # acf_end_point_url = f'http://crichmediadev.local/wp-json/acf/v3/subject/{post_id}'
            acf_end_point_url = f'https://localhost:10008/wp-json/acf/v3/subject/{post_id}'
            # r = requests.get(acf_end_point_url).json()
            # print(r)

            # subject_term
            ##################
            # sprint : 春
            # fall : 秋
            # all-year : 通年
            # intensive : 集中
            ##################
            hw_num = ast.literal_eval(survey[11]).index(max(ast.literal_eval(survey[11])))
            exam_num = ast.literal_eval(survey[13]).index(max(ast.literal_eval(survey[13])))
            hw = ''
            exam = ''
            if hw_num == 0:
                hw = '課題(問題演習や小レポート、プレゼンテーションなど)'
            elif hw_num == 1:
                hw = '小テスト'
            elif hw_num == 2:
                hw = 'リアクションペーパー'
            elif hw_num == 3:
                hw = 'なし'
            if exam_num == 0:
                exam = 'ペーパーテスト'
            elif exam_num == 1:
                exam = 'オンラインテスト'
            elif exam_num == 2:
                exam = '期末レポート'
            elif exam_num == 3:
                exam = 'なし'
            payload = {
                'fields': {
                    'subject_term': 'sprint',
                    # 評価はintではなくstrで
                    'subject_eval': str(survey[6]),
                    'subject_module': str(survey[7]),
                    'subject_record': str(survey[8]),
                    'subject_interest': str(survey[9]),
                    'subject_hw': {
                        'subject_hw_opinion': hw,
                        'subject_hw_easy': ast.literal_eval(survey[12])[0],
                        'subject_hw_average': ast.literal_eval(survey[12])[1],
                        'subject_hw_hard': ast.literal_eval(survey[12])[2]
                    },
                    'subject_exam': {
                        'subject_exam_opinion': exam,
                        'subject_exam_easy': ast.literal_eval(survey[14])[0],
                        'subject_exam_average': ast.literal_eval(survey[14])[1],
                        'subject_exam_hard': ast.literal_eval(survey[14])[2]
                    },
                    'subject_attendance': str(survey[10])
                }
            }

            # acfの中身を更新
            headers = {'content-type': "Application/json"}
            res = requests.post(acf_end_point_url, data=json.dumps(payload) , headers=headers, auth=(user_id, password))
        else:
            print('failed post title is ' + title)
