import csv

surveies = []
with open('cleansed/total.csv') as f:
    reader = csv.reader(f)
    surveies = [row for row in reader]

index = 0
calculated_surveies = []
current_title = ''
current_name = ''
subject_eval = 0
subject_module = 0
subject_record = 0
subject_interest = 0
attendance = 0
hw = [0, 0, 0, 0]
hw_burden = [0, 0, 0]
exam = [0, 0, 0, 0]
exam_burden = [0, 0, 0]
woms = []
count = 0
for i, survey in enumerate(surveies):
    if survey[2] != current_title or survey[3] != current_name:
        if current_title != '':
            if attendance < 0:
                str_attendance = 'あり'
            else:
                str_attendance = 'なし'
            calculated_surveies.append([str(index), surveies[i-1][1], current_title, current_name, surveies[i-1][4], surveies[i-1][5], str(round(subject_eval/count, 1)), str(round(
                subject_module/count, 1)), str(round(subject_record/count, 1)), str(round(subject_interest/count, 1)), str_attendance, hw, hw_burden, exam, exam_burden, woms])
        index += 1
        current_title = survey[2]
        current_name = survey[3]
        subject_eval = 0
        subject_module = 0
        subject_record = 0
        subject_interest = 0
        attendance = 0
        hw = [0, 0, 0, 0]
        hw_burden = [0, 0, 0]
        exam = [0, 0, 0, 0]
        exam_burden = [0, 0, 0]
        woms = []
        count = 0
    subject_eval += int(survey[6])
    subject_module += int(survey[7])
    subject_record += int(survey[8])
    subject_interest += int(survey[9])
    # attendance
    if survey[10] == 'あり':
        attendance += 1
    else:
        attendance -= 1
    # hw
    if "課題(問題演習や小レポートなど)" in survey[11] or "課題(問題演習や小レポート、プレゼンテーションなど)" in survey[11]:
        hw[0] += 1
    if '小テスト' in survey[11]:
        hw[1] += 1
    if 'リアクションペーパー' in survey[11]:
        hw[2] += 1
    if 'なし' in survey[11]:
        hw[3] += 1
    # hw_burden
    if not 'なし' in survey[11]:
        if survey[12] == '楽':
            hw_burden[0] += 1
        elif survey[12] == '普通' or survey[12] == 'ふつう':
            hw_burden[1] += 1
        elif survey[12] == 'きつい':
            hw_burden[2] += 1
    # exam
    if "ペーパーテスト" in survey[13]:
        exam[0] += 1
    if 'オンラインテスト' in survey[13]:
        exam[1] += 1
    if '期末レポート' in survey[13]:
        exam[2] += 1
    if 'なし' in survey[13]:
        exam[3] += 1
    # exam_burden
    if not 'なし' in survey[13]:
        if survey[14] == '楽':
            exam_burden[0] += 1
        elif survey[14] == '普通' or survey[14] == 'ふつう':
            exam_burden[1] += 1
        elif survey[14] == 'きつい':
            exam_burden[2] += 1
    # wom
    if survey[15] != '':
        woms.append(survey[15])
    count += 1
if attendance < 0:
    str_attendance = 'あり'
else:
    str_attendance = 'なし'
# 最後要改善
calculated_surveies.append([str(index), survey[1], current_title, current_name, survey[4], survey[5], str(round(subject_eval/count, 1)), str(round(subject_module/count, 1)),
                           str(round(subject_record/count, 1)), str(round(subject_interest/count, 1)), str_attendance, survey[11], survey[12], survey[13], survey[14], woms])

with open('calculated/calculated.csv', 'w') as f:
    writer = csv.writer(f)
    for row in calculated_surveies:
        writer.writerow(row)
