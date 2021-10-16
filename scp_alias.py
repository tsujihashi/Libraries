import subprocess as sp

enc = 'utf-8'

file = 'alias.csv'
targets = ['tjvm1']
aliases = []
with open(file, 'r', encoding='utf-8') as f:
    aliases = f.readlines()
for target in targets:
    for alias in aliases:
        pass
        #split = alias.strip().replace('\n','').split(',')
        #print("ssh {0} alias {1}=\'{2}\'".format(target, split[0], split[1]))
        #sp.call("ssh {0} alias {1}=\'{2}\'".format(target, split[0], split[1]))
    # bash_profileの編集も必要
    #sp.check_output('grep -nHR \"User specific\"')
    # sp.call('ssh {} rm -f res.txt'.format(target))
    #print('ssh {} grep -nHR "User specific" .bashrc --exclude=res.txt > res.txt'.format(target))
    #sp.call('ssh {} grep -nHR "User\ specific\ aliases" --exclude=res.txt > res.txt'.format(target))
    #sp.call('scp {}:~/res.txt ./'.format(target))
    sp.call('scp {}:~/.bashrc ./'.format(target))
    flg = True
    current_aliases = []
    with open('.bashrc', 'r', encoding='utf-8') as f:
        while 'User specific aliases' not in f.readline():
            continue
        current_aliases = [line.replace('\n', '') for line in f.readlines()]
    for alias in aliases:
        if '.csv' in file:
            alias = 'alias ' + alias.replace(',', '=\'').strip().replace('\n', '') + '\''
        else:
            alias = alias.replace('\n', '').strip()
        if alias not in current_aliases:
            with open('.bashrc', 'a', encoding='utf-8', newline='\n') as f:
                f.write(alias + '\n')
    sp.call('scp .bashrc {}:~/'.format(target))


        

