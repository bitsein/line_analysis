import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

args = sys.argv
csv_file = args[1]
chatData = pd.read_csv(csv_file)
chatData = chatData.set_index("id")


chatData.loc[:,"timestamp"] = pd.to_datetime(chatData["timestamp"])
chatData.loc[:,"comment_length"] = [len(str(i)) for i in chatData["comment"]]
chatData.loc[:,"date"] = [i.date() for i in chatData["timestamp"]]
chatData.loc[:,"time"] = [i.time() for i in chatData["timestamp"]]

df_groupedBy_date = chatData.groupby("date").count()
df_groupedBy_time = chatData.groupby("time").count()
df_groupedBy_comment_length = chatData.groupby("comment_length").count()


# ファイルを開く
pdf = PdfPages('result2.pdf')

date_size = len(df_groupedBy_date.index)
plt.figure(figsize=(date_size/10, 6))
plt.bar(df_groupedBy_date.index, df_groupedBy_date["time"], color="black")
plt.xlabel("date")
plt.ylabel("comments")
plt.xticks(df_groupedBy_date.index)
plt.xticks(rotation=90, fontsize=5)
plt.tight_layout()
pdf.savefig()
plt.close()

time_size = len(df_groupedBy_time.index)
plt.figure(figsize=(time_size/10, 6))
plt.bar(df_groupedBy_time.index, df_groupedBy_time["date"], color="black", width=50.0)
plt.xlabel("time")
plt.ylabel("comments")
plt.xticks(df_groupedBy_time.index)
plt.xticks(rotation=90, fontsize=5)
plt.tight_layout()
pdf.savefig()
plt.close()

'''
comment_size = len(df_groupedBy_comment_length.index)
comment_length_max = df_groupedBy_comment_length.index.max()
plt.figure(figsize=(comment_size/10, comment_length_max/50))
plt.bar(df_groupedBy_comment_length.index, df_groupedBy_comment_length["date"], color="black", width=1.2)
plt.xlabel("comment_size")
plt.ylabel("number")
plt.xticks(df_groupedBy_comment_length.index)
plt.xticks(rotation=90, fontsize=1)
plt.tight_layout()
pdf.savefig()
plt.close()
'''

pdf.close()