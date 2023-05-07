import csv

# master
faculties = []
features = []
teachers = []
name_list = []

# その他のidは1127-1132まで経商理法政法法文の順
with open('master/faculty_master.csv') as f:
    reader = csv.reader(f)
    faculties = [row for row in reader]
with open('master/feature_master.csv') as f:
    reader = csv.reader(f)
    features = [row for row in reader]
with open('master/teacher_master.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        teachers.append(row)
        name_list.append(row[0])
    # teachers = [row for row in reader]
    # name_list = [row[0] for row in reader]

surveies = []
with open('calculated/calculated.csv') as f:
    reader = csv.reader(f)
    surveies = [row for row in reader]

id_list = []

for survey in surveies:
    if len(survey) == 16:
        row_3 = survey[3].split("／")
        row_4 = survey[4].split("／")
        row_5 = survey[5].split("／")
        # subject_teacher
        teacher_list = []
        for row in row_3:
            for teacher in teachers:
                if row == teacher[0]:
                    teacher_list.append(teacher[1])
            if not row in name_list:
                if not survey[0] in id_list:
                    id_list.append(survey[0])
        # subject_faculty
        faculty_list = []
        for row in row_4:
            for faculty in faculties:
                if row == faculty[0]:
                    faculty_list.append(faculty[1])
        for i, row in enumerate(row_5):
                # 以下の三つはマスタが重複しているため個別で対応
                if row == 'その他':
                    if row_4[i] == '経済学部':
                        faculty_list.append(1127)
                    elif row_4[i] == '商学部':
                        faculty_list.append(1128)
                    elif row_4[i] == '理工学部':
                        faculty_list.append(1129)
                    elif row_4[i] == '法学部政治学科':
                        faculty_list.append(1130)
                    elif row_4[i] == '法学部法律学科':
                        faculty_list.append(1131)
                    elif row_4[i] == '文学部':
                        faculty_list.append(1132)
                elif row == '必修・選択必修':
                    if row_4[i] == '経済学部':
                        faculty_list.append(138)
                    elif row_4[i] == '商学部':
                        faculty_list.append(130)
                    elif row_4[i] == '理工学部':
                        faculty_list.append(150)
                    elif row_4[i] == '法学部政治学科':
                        faculty_list.append(146)
                    elif row_4[i] == '法学部法律学科':
                        faculty_list.append(142)
                    elif row_4[i] == '文学部':
                        faculty_list.append(99)
                elif row == '言語' or row == '語学':
                    if row_4[i] == '経済学部':
                        faculty_list.append(140)
                    elif row_4[i] == '商学部':
                        faculty_list.append(132)
                    elif row_4[i] == '理工学部':
                        faculty_list.append(152)
                    elif row_4[i] == '法学部政治学科':
                        faculty_list.append(148)
                    elif row_4[i] == '法学部法律学科':
                        faculty_list.append(144)
                    elif row_4[i] == '文学部':
                        faculty_list.append(5)
                else:
                    for secondary_faculty in faculties:
                        if row in secondary_faculty[0]:
                            faculty_list.append(secondary_faculty[1])
        # subject_feature
        feature_list = []
        if float(survey[6]) >= 4 and float(survey[7]) == 5 and float(survey[8]) == 5 and float(survey[9]) == 5:
            feature_list.append(202)
        elif float(survey[6]) >= 4 and float(survey[7]) >= 4 and float(survey[8]) >= 4:
            feature_list.append(203)
        elif float(survey[7]) <= 2 and float(survey[8]) <= 2:
            feature_list.append(205)
        elif float(survey[7]) == 1 and float(survey[8]) == 1:
            feature_list.append(191)
        else:
            feature_list.append(204)
        if survey[10] == 'あり':
            feature_list.append(192)
        else:
            feature_list.append(193)
        if '面白い' in survey[15] or 'おもしろい' in survey[15]:
            feature_list.append(283)
        if 'タメにな' in survey[15] or 'ためにな' in survey[15]:
            feature_list.append(302)

        survey.extend([teacher_list, faculty_list, feature_list])

print(id_list)

with open('classified/classified_survey.csv', 'w') as f:
    writer = csv.writer(f)
    for row in surveies:
        writer.writerow(row)
