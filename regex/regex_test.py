from os import name
import re
import json

# print(f_file)
# question = re.findall(r"^[1-9]{1,2}", f_file, re.M)
# options = re.findall(r"(?<=\n)[ABCD]\.[\n\s\w\W]*(?=\n.*[ABCD]\.)",f_file)
# passage = re.findall(r"\[\s?Paragraph\s?[1-9]{0,2}\][\w\W\s\n]+?(?=[ABCD0-9]{1,2}\.)",f_file)
# print(question)
# print(passage)
def remove_text(input_path, output_path):
    with open(input_path,'r',encoding='utf-8') as f:
        f_file = f.read()
    questions = re.sub(r"\[\s{0,2}Paragraph\s{0,2}[1-9]{0,2}\s?\][\w\W\s\n]+?(?=\n[ABCD0-9]{1,2}\.)",'',f_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        for i in questions:
            f.writelines(i);
    print('done')

def seperate_passage(input_path, output_path_list):
    with open(input_path,'r',encoding='utf-8') as f:
        f_file = f.read()
    f_file += '\n1.'
    questions = re.findall(r"1.[\w\W\n\s]*?(?=\n1\.)",f_file)
    for i,output_path in enumerate(output_path_list):
        with open(output_path, 'w',encoding='utf-8') as f:
            f.writelines(questions[i]);
            f.writelines('\n1.')
    print('done')

def seperate_questions(input_path, output_path_list=None):
    question_list = []
    with open(input_path,'r',encoding='utf-8') as f:
        f_file = f.read()
    questions = re.findall(r"[0-9]+\.[\W\w\s\n]*?(?=\n[1-9][0-9]*\.)",f_file)
    for question_string in questions:
        question_string += '\nF.'
        match_pos = re.search(r"[0-9]{1,2}\.[\W\w\s\n]*?(?=[A-F]\.)",question_string).span()
        description = question_string[match_pos[0]:match_pos[1]]
        options = re.findall(r"(?<=\n[A-F]\.\s)[\w\W\n\s]*?(?=\n[A-F]\.)",question_string)
        description = description.replace('\n','')
        for i in range(len(options)):
            options[i] = options[i].replace('\n','')
        question_dict = {'type':'multiple','question':description, 'options':options, 'anchor':[0]}
        highlight_criterion = (re.search(r"essential information in the highlighted",question_string) != None) or (re.search(r"closest in meaning",question_string) != None)
        if (re.search(r"ook at the four squares",question_string) != None):
            question_dict['type'] = 'insertion'
        elif highlight_criterion:
            question_dict['type'] = 'highlight'
        elif re.search(r"\n14\.\s", question_string)!=None:
            question_dict['type'] = 'structure'
        if re.search(r"(?<=[P|p]aragraph\s)[1-9](?=\s)", question_string) != None:
            anchor = re.findall(r"(?<=[P|p]aragraph\s)[1-9](?=[\s,])", question_string)
            question_dict['anchor'] = list(map(lambda x: x-1 ,map(int,anchor)))
        question_list.append(question_dict)
    return question_list

if __name__ == '__main__':
    
    # remove_text('raw_reading.txt','remove_text.txt')
    # seperate_passage('remove_text.txt',['passage1.txt','passage2.txt','passage3.txt'])
    with open('passage3_question.txt','w',encoding='utf-8') as f:
        f.write(seperate_questions('passage3.txt').__str__())