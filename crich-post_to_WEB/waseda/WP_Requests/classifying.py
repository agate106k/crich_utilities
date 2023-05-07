import csv
import ast

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
        row_4 = survey[4].split("/")
        row_5 = survey[5].split("/")
        # subject_teacher
        teacher_list = []
        for row in row_4:
            for teacher in teachers:
                if row == teacher[0]:
                    teacher_list.append(teacher[1])
            if not row in name_list:
                if not survey[0] in id_list:
                    id_list.append(survey[0])
        # subject_faculty
        faculty_list = []
        # for row in row_5:
        #     for faculty in faculties:
        #         if row == faculty[0]:
        #             faculty_list.append(faculty[1])
        for i, row in enumerate(row_5):
                # 以下の三つはマスタが重複しているため個別で対応
                    if row_5[i] == '政治経済学部':
                        faculty_list.append(41)
                    elif row_5[i] == '法学部':
                        faculty_list.append(43)
                    elif row_5[i] == '商学部':
                        faculty_list.append(42)
                    elif row_5[i] == '社会科学部':
                        faculty_list.append(48)
                    elif row_5[i] == '文学部':
                        faculty_list.append(40)
                    elif row_5[i] == '文化構想学部':
                        faculty_list.append(40)
                    elif row_5[i] == '教育学部':
                        faculty_list.append(47)
                    elif row_5[i] == '国際教養学部':
                        faculty_list.append(589)
                    elif row_5[i] == 'グローバルエデュケーションセンター（GEC)':
                        faculty_list.append(799)
                    elif row_5[i] == '基幹理工学部':
                        faculty_list.append(46)
                    elif row_5[i] == '創造理工学部':
                        faculty_list.append(44)
                    elif row_5[i] == '先進理工学部':
                        faculty_list.append(45)
                    elif row_5[i] == '人間科学部':
                        faculty_list.append(994)
                    elif row_5[i] == 'スポーツ科学部':
                        faculty_list.append(1060)


        # subject_feature
        feature_list = []
        if float(survey[6]) >= 4 and float(survey[7]) == 5 and float(survey[8]) == 5 and float(survey[9]) == 5 and ast.literal_eval(survey[14])[2] == 0 and ast.literal_eval(survey[12])[2] == 0 and ast.literal_eval(survey[12])[1] == 0 and ast.literal_eval(survey[14])[1] == 0:
            feature_list.append(53)
        elif float(survey[6]) >= 4 and float(survey[7]) >= 4 and float(survey[8]) >= 4 and ast.literal_eval(survey[14])[2] == 0 and ast.literal_eval(survey[12])[2] == 0:
            feature_list.append(54)
        elif float(survey[7]) <= 2 and float(survey[8]) <= 2 and ast.literal_eval(survey[14])[0] == 0 and ast.literal_eval(survey[12])[0] == 0:
            feature_list.append(56)
        elif float(survey[7]) == 1 and float(survey[8]) == 1 and ast.literal_eval(survey[14])[0] == 0 and ast.literal_eval(survey[12])[0] == 0 and ast.literal_eval(survey[14])[1] == 0 and ast.literal_eval(survey[12])[1] == 0:
            feature_list.append(57)
        else:
            feature_list.append(55)
        if survey[10] == 'あり':
            feature_list.append(68)
        else:
            feature_list.append(69)

        if '面白い' in survey[15] or 'おもしろい' in survey[15]:
            feature_list.append(64)
        if 'タメにな' in survey[15] or 'ためにな' in survey[15]:
            feature_list.append(65)
        if '分かりや' in survey[15] or 'わかりや' in survey[15]:
            feature_list.append(257)

        survey.extend([teacher_list, faculty_list, feature_list])
print(id_list)
print(faculty_list)
with open('classified/classified_survey.csv', 'w') as f:
    writer = csv.writer(f)
    for row in surveies:
        writer.writerow(row)
