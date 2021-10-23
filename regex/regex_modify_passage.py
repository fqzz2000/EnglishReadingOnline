import re

def modify_content(input,output):
    with open(input,'r') as f:
        f_file = f.read()
    f_file += '</p>'
    f_file = "<p>" + f_file
    string = re.sub(r'\n','',f_file)
    string = re.sub(r'"','\"',string)
    string = re.sub(r'\[\s?[P|a]aragraph\s1\s?\]','',string)
    string = re.sub(r'\[\s?[P|a]aragraph\s[2-9]\s?\]','</p><p>',string)
    with open(output, 'w') as f:
        f.write(string)
    return None

if __name__ == '__main__':
    modify_content('raw_passage.txt', 'passage_content.txt')
