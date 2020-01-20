# 必要なものをインポート
import glob
import os
import sys

# 文字に色をつけて表示する関数(RED or GREEN)
def c_print(string,color):
    if color=="RED":
        print("\033[31m"+string+"\033[0m")
    elif color=="GREEN":
        print("\033[32m"+string+"\033[0m")
    else:
        print(string)
    return 0

# 日/月/年 -> 年/月/日 にする関数 (月は数へ)
def e2j(string):
    MONTH={ "Jan":"01","Feb":"02","Mar":"03","Apr":"04",
            "May":"05","Jun":"06","Jul":"07","Aug":"08",
            "Sep":"09","Oct":"10","Nov":"11","Dec":"12" }
    s=string.split("/")
    s[1]=MONTH[s[1]]
    s=s[::-1]
    return "/".join(s)

# リストのバイト数を計算する関数
def l2b(_list):
    r=0
    for l in _list:
        r+=len(l.encode())
    return r

# アクセス件数を出力する関数
def output(host,date):
    print("\n・時刻 -> アクセス件数"*(len(date)!=0))
    d_set=sorted(set(date),key=date.index)
    for i in range(len(d_set)):
        print("  "+d_set[i]+" -> "+str(date.count(d_set[i]))+"件")

    h_dict={}
    print("\n・ホスト名 -> アクセス件数"*(len(host)!=0))
    h_set=sorted(set(host),key=host.index)
    for i in range(len(h_set)):
        h_dict[h_set[i]]=host.count(h_set[i])
    h_dict_sorted=sorted(h_dict.items(),key=lambda x:x[1],reverse=True)
    [print("  "+l[0]+" -> "+str(l[1])+"件") for l in h_dict_sorted]
    print("")
    return 0

# 引数(ファイル名)を受け取る
c_print("\nアクセス件数を集計します．","GREEN")
c_print("集計するファイル名を入力してください．ワイルドカード「*」が使用できます．","GREEN")
c_print("集計するファイル名を全て入力し終えたら next と入力してください．","GREEN")
c_print("(終了する場合は exit と入力してください．)","GREEN")
p_list=[]
flg=0
while True:
    f_name=input(">> ")
    if f_name=="exit":
        sys.exit()
    elif flg==0 and f_name=="":
        c_print("\nファイル名は1つ以上入力してください．","RED")
    elif f_name=="next":
        break
    elif "*" in f_name:
        p_list.extend(glob.glob(f_name))
        flg=1
    else:
        p_list.append(f_name)
        flg=1

# 引数(期間)を受け取る
c_print("\n集計する期間を入力してください．","GREEN")
c_print(" 2017/04/01-2017/04/30 のように入力してください．","GREEN")
c_print("全期間で検索する場合はエンターキーを入力してください．","GREEN")
c_print("(終了する場合は exit と入力してください．)","GREEN")
while True:
    try:
        arg=input("\n>> ")
        if (arg=="" or arg=="exit" or
            (len(arg)==21 and
            arg[:4].isdigit() and
            arg[4]=="/" and
            arg[5:7].isdigit() and
            arg[7]=="/" and
            arg[8:10].isdigit() and
            arg[10]=="-" and
            arg[11:15].isdigit() and
            arg[15]=="/" and
            arg[16:18].isdigit() and
            arg[18]=="/" and
            arg[19:].isdigit())):
            break
    except:
        pass
    c_print("\n入力が間違っています．","RED")
    c_print("期間を指定する場合は 2017/04/01-2017/04/30 のように入力してください．","RED")
    c_print("全期間で検索する場合はエンターキーを入力してください．","RED")
    c_print("終了する場合は exit と入力してください．","RED")

# 引数(期間)に応じた処理
if arg=="exit":
    sys.exit()
elif arg=="":
    d_period=0
    d_start="0"
    d_end="9999/99/99"
else:
    d_period=1
    d_start=arg.split("-")[0]
    d_end=arg.split("-")[1]

MAX_BYTE=2*1024**3-50# 2GB-50MB を処理できる最大のバイト数に設定
host=[]# 要素1つは7~15B
date=[]# 要素1つは25B
b=0# 読み込んだファイルのバイト数

# ファイル読み込み
if len(p_list)==0:
    print("ファイルが見つかりませんでした．")
    sys.exit()
for path in p_list:
    if os.path.exists(path):
        with open(path) as file:
            for line in file:
                b=l2b(host)+l2b(date)
                if b>MAX_BYTE:
                    output(host,date)
                    host=[]
                    date=[]
                l=list(line.split())
                ymd=e2j(l[3][1:12])
                if d_start<=ymd<=d_end:
                    host.append(l[0])
                    date.append(ymd+" "+l[3][13:]+" "+l[4][:-1])
    else:
        c_print("ファイル %s は存在しません．"%path,"RED")
if b!=MAX_BYTE+1:
    output(host,date)