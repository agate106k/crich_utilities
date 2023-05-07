import csv

surveies = []
with open('cleansed/total.csv') as f:
    reader = csv.reader(f)
    surveies = [row for row in reader]

index = 0
calculated_surveies = []
current_title = ''
current_name = ''
semester_name = ''
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
    if survey[3] != current_title or survey[4] != current_name:
        if current_title != '':
            if attendance > 0:
                str_attendance = 'あり'

            else:
                str_attendance = 'なし'

            calculated_surveies.append([index, surveies[i-1][1], surveies[i-1][2],current_title, current_name, surveies[i-1][5], str(round(subject_eval/count, 1)),
            str(round(subject_module/count, 1)), str(round(subject_record/count, 1)), str(round(subject_interest/count, 1)), str_attendance, hw, hw_burden, exam, exam_burden, woms])
        index += 1
        current_title = survey[3]
        current_name = survey[4]
        semester_name = survey[2]
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
    if survey[14] == 'あり':
        attendance += 1
    else:
        attendance -= 1
    # hw
    if "課題(問題演習や小レポートなど)" in survey[10]:
        hw[0] += 1
    if '小テスト' in survey[10]:
        hw[1] += 1
    if 'リアクションペーパー' in survey[10]:
        hw[2] += 1
    if "4" in survey[10]:
        hw[0] += 1
        hw[1] += 1
    if "5" in survey[10]:
        hw[0] += 1
        hw[2] += 1
    if "6" in survey[10]:
        hw[1] += 1
        hw[2] += 1
    if "7" in survey[10]:
        hw[0] += 1
        hw[1] += 1
        hw[2] += 1
    if "8" in survey[10]:
        hw[3] += 1
    if 'なし' in survey[10]:
        hw[3] += 1
    # hw_burden
    if not 'なし' in survey[10]:
        if survey[11] == '楽':
            hw_burden[0] += 1
        elif survey[11] == '普通' or survey[11] == 'ふつう':
            hw_burden[1] += 1
        elif survey[11] == 'きつい':
            hw_burden[2] += 1
        else: hw_burden[2] += 1

    # exam
    if "ペーパーテスト" in survey[12]:
        exam[0] += 1
    if 'オンラインテスト' in survey[12]:
        exam[1] += 1
    if '期末レポート' in survey[12]:
        exam[2] += 1
    if 'なし' in survey[12]:
        exam[3] += 1
    # exam_burden
    if not 'なし' in survey[12]:
        if survey[13] == '楽':
            exam_burden[0] += 1
        elif survey[13] == '普通' or survey[13] == 'ふつう':
            exam_burden[1] += 1
        elif survey[13] == 'きつい':
            exam_burden[2] += 1
        else: exam_burden [1] +=1
    # wom
    if survey[15] != '':
        woms.append(survey[15])
    count += 1
    if attendance > 0:
        str_attendance = 'あり'
    else:
        str_attendance = 'なし'
# 最後要改善
calculated_surveies.append([index, survey[1], survey[2], current_title, current_name, survey[5],str(round(subject_eval/count, 1)), str(round(subject_module/count, 1)),
                           str(round(subject_record/count, 1)), str(round(subject_interest/count, 1)), str_attendance, survey[10],survey[11], survey[12], survey[13], woms])

with open('calculated/calculated.csv', 'w') as f:
    writer = csv.writer(f)
    for row in calculated_surveies:
        writer.writerow(row)
