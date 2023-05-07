import csv
import operator
import pandas as pd
import re
# 無駄なものの排除
with open('original/早稲田 履修情報入力フォーム 2022.csv') as f:
    reader = csv.reader(f)
    l = [row for row in reader]
m = []
for row in l:
    n = [r.replace('（易しい、面白い）', '').replace('（難しい、つまらない）', '').replace('課題(問題演習や小レポートなど), 小テスト, リアクションペーパー', '7').replace('課題(問題演習や小レポートなど), 小テスト', '4').replace('課題(問題演習や小レポートなど), リアクションペーパー', '5').replace('小テスト, リアクションペーパー', '6').replace('課題(問題演習や小レポートなど), なし', '8').replace('小テスト, なし', '8').replace(' ', '').replace('　', '') for r in row]
    # n = [re.sub('\A[a-z\d]{8,100}\Z(?i)','') for r in row if r!= '']
    # [k.replace('"課題(問題演習や小レポートなど), なし"', '8').replace('"小テスト, なし"', '8').replace('"リアクションペーパー, なし"', '8').replace('"課題(問題演習や小レポートなど), 小テスト, なし"', '8').replace('"課題(問題演習や小レポートなど), リアクションペーパー, なし"', '8').replace('"小テスト, リアクションペーパー, なし"', '8').replace('"課題(問題演習や小レポートなど), 小テスト, リアクションペーパー, なし"', '8') for k in bow if k != '']
    n = [r for i, r in enumerate(n) if i > 0]
    m.append(n)

print(m[-1])
with open('cleansed/Book1_cleansed.csv', 'w') as f:
    writer = csv.writer(f)
    for x in m:
        writer.writerow(x)



#
#
# # 教授の名前のフォーマット
# default_list = []
# with open('cleansed/Book1_cleansed.csv') as f:
#     reader = csv.reader(f)
#     default_list = [row for row in reader]
#
# for row in default_list:
#     old_names = row[1].split("／")
#     new_names = []
#     for old_name in old_names:
#         new_name = ""
#         if("，" in old_name):
#             arr = old_name.split("，")
#             if(arr[1].startswith(" ")):
#                 arr[1] = arr[1].replace(" ", "", 1)
#             if(" " in arr[1]):
#                 arr[1] = arr[1].replace(" ", "・")
#             if("　" in arr[0]):
#                 arr[0] = arr[0].replace("　", "・")
#             new_name = arr[1] + "・" + arr[0]
#         elif("　" in old_name):
#             new_name = old_name.replace("　", "・", 3)
#         else:
#             new_name = old_name.replace(" ", "")
#         new_names.append(new_name)
#     # lecturer
#     name = "／".join(new_names)
#     row[1] = name
#
# with open('cleansed/Book1_cleansed.csv', 'w') as f:
#     writer = csv.writer(f)
#     for x in default_list:
#         writer.writerow(x)


# 年度,総合評価列追加
m = []
with open('cleansed/Book1_cleansed.csv') as f:
    reader = csv.reader(f)
    m = [row for row in reader]

for row in m:
    # row.insert(2, round((int(row[2]) + int(row[3]) + int(row[4]))/3))
    row.insert(0, '2021')

with open('cleansed/Book1_cleansed.csv', 'w') as f:
    writer = csv.writer(f)
    for x in m:
        writer.writerow(x)

#
# # 分類分け
# syllabus = []
# with open('syllabusのコピー.csv') as f:
#     reader = csv.reader(f)
#     syllabus = [row for row in reader]
# m = []
# with open('cleansed/Book1_cleansed.csv') as f:
#     reader = csv.reader(f)
#     m = [row for row in reader]
# for row in m:
#     for subject in syllabus:
#         if row[1] == subject[2] and row[2] == subject[5]:
#             row.insert(3, subject[6])
#             row.insert(4, subject[7])
#             break
# with open('cleansed/Book1_cleansed.csv', 'w') as f:
#     writer = csv.writer(f)
#     for x in m:
#         writer.writerow(x)
#
# SQLからexportしたもの用
# with open('original/wp_subject_survey.csv') as f:
#     reader = csv.reader(f)
#     l = [row for row in reader]
# m = []
# for row in l:
#     n = [r.replace('"', '') for r in row]
#     n = [r for i, r in enumerate(n) if i > 0]
#     m.append(n)
# with open('cleansed/wp_subject_survey.csv', 'w') as f:
#     writer = csv.writer(f)
#     for x in m:
#         writer.writerow(x)

# id振る
m = []
with open('cleansed/Book1_cleansed.csv') as f:
    reader = csv.reader(f)
    m = [row for row in reader]
for i, row in enumerate(m):
    # del row[0]
    row.insert(0, i)
with open('cleansed/total.csv', 'w') as f:
    writer = csv.writer(f)
    for x in m:
        writer.writerow(x)


m = []
with open('cleansed/total.csv') as f:
    reader = csv.reader(f)
    m = [row for row in reader]
result = sorted(m, key=operator.itemgetter(1))
with open('cleansed/total.csv', 'w') as f:
    writer = csv.writer(f)
    for x in result:
        writer.writerow(x)

# 科目名→講師名でソート
df = pd.read_csv('cleansed/total.csv', header=None, dtype=object)
result = df.sort_values([3, 4])
result.to_csv('cleansed/total.csv', header=False, index=False)
