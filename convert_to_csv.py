# coding: UTF-8
from datetime import datetime
import re
import os
import csv
import sys

args = sys.argv
txt_data = args[1]

re_date = r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d+/\d+/\d{4}$"
re_time = r"^\d{2}:\d{2}\t"


def make_filename(line):
    export_day = line.split(" ")[2][:-1]
    export_time = line.split(" ")[3]
    export_date = datetime.strptime(export_day + " " + export_time, '%m/%d/%Y %H:%M\n')
    return export_date.strftime('chat_data_%Y_%m_%d.csv')


def main():
    i=0 #行数カウント
    k=0 #最初にタイムスタンプを検出した時は書き込みをしない
    id=0 #コメントにidを付与
    comment = ""
    return_or_dayChange = 1 #日付が変わったことによる改行なのか、コメント内での改行なのかを判定

    f = open(txt_data, encoding="utf-8")
    line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)

    while line:
        if i < 3:
            if i == 1:
                filename = make_filename(line)
                if os.path.isfile(filename):
                    os.remove(filename)
                g = open(filename, 'w')
                writer = csv.writer(g)
                writer.writerow(["id","timestamp","sender","comment"])

            i += 1
            line = f.readline()
            continue

        if re.match(re_date, line): #日付列かどうかの判定
            date = datetime.strptime(line.split(" ")[1], '%m/%d/%Y\n')
            if return_or_dayChange == 0:
                comment = comment.rstrip("\n")
        elif re.match(re_time, line): #タイムスタンプかどうかの判定
            if k: #タイムスタンプと確定した時点でそれまでのコメントを出力
                writer.writerow([str(id),timestamp,sender,str(comment)])
                id+=1
            k=1
            time = datetime.strptime(line.split("\t")[0], '%H:%M')
            timestamp = datetime.strptime(str(date.year)+" "+str(date.month)+" "+str(date.day)\
                                            +" "+str(time.hour)+" "+str(time.minute), '%Y %m %d %H %M')
            sender = line.split("\t")[1]
            comment = line.split("\t")[2].rstrip("\n")
            
        else:
            if comment == "":
                comment = line
            else:
                if line == "\n":
                    return_or_dayChange = -1            
                comment = comment+"\n"+line.rstrip("\n")


        i += 1 
        return_or_dayChange += 1
        line = f.readline()
    f.close


if __name__ == '__main__':
    main()
