import pandas as pd
import sys

movielist=sys.argv[1]
readfilename=sys.argv[2]
encoding=sys.argv[3]

if not movielist or  not readfilename or not encoding:
    print('python3 py_filename movielist readfilename encoding')
f=open(movielist)
data=pd.read_csv(readfilename, encoding=encoding)
new_row={}
movie_info={}
size=len(data['MOVIENAME'])
#print(data)

sums = [[0]*2 for i in range(4)]
count = [[0]*2 for i in range(4)]
pos_count = [[0]*2 for i in range(4)]
neg_count = [[0]*2 for i in range(4)]
prop=[[0]*2 for i in range(4)]

df_idx=0
col_names=[
'MOVIENAME',
'facebook_pos_count_before', 'facebook_pos_count_after',
'facebook_neg_count_before', 'facebook_neg_count_after',
'facebook_pos_neg_ratio_before', 'facebook_pos_neg_ratio_after',
'twitter_pos_count_before', 'twitter_pos_count_after',
'twitter_neg_count_before', 'twitter_neg_count_after',
'twitter_pos_neg_ratio_before', 'twitter_pos_neg_ratio_after',
'naver_pos_count_before', 'naver_pos_count_after',
'naver_neg_count_before', 'naver_neg_count_after',
'naver_pos_neg_ratio_before', 'naver_pos_neg_ratio_after',
'daum_pos_count_before', 'daum_pos_count_after',
'daum_neg_count_before', 'daum_neg_count_after',
'daum_pos_neg_ratio_before', 'daum_pos_neg_ratio_after'
]
df=pd.DataFrame(columns=col_names)
line=f.readline()
for x in range(size):
    if x%1000==0:
        print('x:'x)
    row=data[x:x+1]
    li=line.split("\t")

    moviename=li[0]
    released_date=li[1]
    #print(row['MOVIENAME'][x])
    if row['MOVIENAME'][x]!=moviename or x==size-1:
        new_row['MOVIENAME']=[moviename]
        for i in range(4):
            for j in range(2):

                try:
                    prop[i][j]=float(sums[i][j]/count[i][j])
                except:
                    prop[i][j]=''

        '''
        df = pd.DataFrame(data={'MOVIENAME':moviename,
        'facebook_pos_count_before':pos_count[0][0], 'facebook_pos_count_after':pos_count[0][1],
        'facebook_neg_count_before':neg_count[0][0], 'facebook_neg_count_after':neg_count[0][1],
        'facebook_pos_neg_ratio_before':prop[0][0], 'facebook_pos_neg_ratio_after':prop[0][1],
        'twitter_pos_count_before':pos_count[1][0], 'twitter_pos_count_after':pos_count[1][1],
        'twitter_neg_count_before':neg_count[1][0], 'twitter_neg_count_after':neg_count[1][1],
        'twitter_pos_neg_ratio_before':prop[1][0], 'twitter_pos_neg_ratio_after':prop[1][1],
        'naver_pos_count_before':pos_count[2][0], 'naver_pos_count_after':pos_count[2][1],
        'naver_neg_count_before':neg_count[2][0], 'naver_neg_count_after':neg_count[2][1],
        'naver_pos_neg_ratio_before':prop[2][0], 'naver_pos_neg_ratio_after':prop[2][1],
        'daum_pos_count_before':pos_count[3][0], 'daum_pos_count_after':pos_count[3][1],
        'daum_neg_count_before':neg_count[3][0], 'daum_neg_count_after':neg_count[3][1],
        'daum_pos_neg_ratio_before':prop[3][0], 'daum_pos_neg_ratio_after':prop[3][1]
        }, index=[0])
        '''


        df.loc[df_idx]=[moviename,
        pos_count[0][0],pos_count[0][1],
        neg_count[0][0], neg_count[0][1],
        prop[0][0], prop[0][1],
        pos_count[1][0],pos_count[1][1],
        neg_count[1][0], neg_count[1][1],
        prop[1][0], prop[1][1],
        pos_count[2][0], pos_count[2][1],
        neg_count[2][0], neg_count[2][1],
        prop[2][0], prop[2][1],
        pos_count[3][0], pos_count[3][1],
        neg_count[3][0], neg_count[3][1],
        prop[3][0], prop[3][1]
        ]

        df_idx=df_idx+1


        for i in range(4):
            for j in range(2):
                sums[i][j]=count[i][j]=pos_count[i][j]=neg_count[i][j]=prop[i][j]=0

        line=f.readline()

    #idx 0: 개봉전, idx 1: 개봉 후
    #sns 0:facebook, 1:twitter, 2:naver, 3: daum
    if row['POS_NEG_RATIO'][x]>=0:

        idx=0
        sns=0
        if row['DATE'][x].split('  ')[0]<released_date:
            idx=0
            #print('개봉전', row['DATE'][x].split(' ')[0])
        else:
            idx=1
            #print('개봉후', row['DATE'][x].split(' ')[0])

        if row['SNS'][x]=='facebook':
            sns=0
        elif row['SNS'][x]=='twitter':
            sns=1
        elif row['SNS'][x]=='naver':
            sns=2
        else:
            sns=3

        sums[sns][idx]=sums[sns][idx]+row['POS_NEG_RATIO'][x]
        count[sns][idx]=count[sns][idx]+1
        if row['POS_NEG_RES'][x]=='POS':
            pos_count[sns][idx]=pos_count[sns][idx]+1
        elif row['POS_NEG_RES'][x]=='NEG':
            neg_count[sns][idx]=neg_count[sns][idx]+1

    else:
        print('null')

    if x==size-1:
        new_row['MOVIENAME']=[moviename]
        for i in range(4):
            for j in range(2):

                try:
                    prop[i][j]=float(sums[i][j]/count[i][j])
                except:
                    prop[i][j]=''

        df.loc[df_idx]=[moviename,
        pos_count[0][0],pos_count[0][1],
        neg_count[0][0], neg_count[0][1],
        prop[0][0], prop[0][1],
        pos_count[1][0],pos_count[1][1],
        neg_count[1][0], neg_count[1][1],
        prop[1][0], prop[1][1],
        pos_count[2][0], pos_count[2][1],
        neg_count[2][0], neg_count[2][1],
        prop[2][0], prop[2][1],
        pos_count[3][0], pos_count[3][1],
        neg_count[3][0], neg_count[3][1],
        prop[3][0], prop[3][1]
        ]
        df.to_csv(readfilename.split('.')[0]+'posneg_summary.csv',encoding='cp949')
