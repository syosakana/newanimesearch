from janome.tokenizer import Tokenizer

# 極性辞書の作成
dict_polarity = {}
with open('./pn_ja.txt', 'r') as f:
    line = f.read()
    lines = line.split('\n')
    for i in range(len(lines)):
        line_components = lines[i].split(':')
        dict_polarity[line_components[0]] = line_components[3]



# ネガポジ分析用の関数の作成
def judge_polarity(text):
    t = Tokenizer()
    #形態素解析
    tokens = t.tokenize(text)
    pol_val = 0
    for token in tokens:
        word = token.surface
        pos = token.part_of_speech.split(',')[0]
        if word in dict_polarity:
            pol_val = pol_val + float(dict_polarity[word])

    if pol_val > 0.3:
        #極性値の程度が0.3以下だった場合
        print("Positive. Score:"+str(pol_val))
    elif pol_val < -0.3:
        print("Negative. Score:"+str(pol_val))
    else:
        print("Neutral. Score:"+str(pol_val))