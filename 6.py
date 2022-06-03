import os
import argparse
myfile = open("111.txt", "w+")
with open("111.txt", "a") as f:
    f.write('111')
myfile.close()
parser = argparse.ArgumentParser(description='A tutorial of argparse')
parser.add_argument('-n', '--name', nargs='?', default='Аноним', help="Имя пользователя")
parser.add_argument('-p', '--path', help="Путь к файлу")
parser.add_argument('-nQ', '--noQ', action="store_true", help="Подавление вопростов пользователю")
args = parser.parse_args()
print(f'Привет {args.name}!')
print(args)

if os.path.exists(args.path):
    ag = input(f'\n{args.name}, Вы действительно хотите удалить файл? ').capitalize()
    if ag[0] == 'y':
        os.remove(args.path)
        print(("\nвсе"))
else:
    print("\nТакого файла нет")