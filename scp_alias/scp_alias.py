import subprocess as sp
import time

def print_call(command):
    # 実行するコマンドをログに出力する
    import subprocess as sp
    print('[command]', command)
    sp.call(command)

def scp_alias(file, targets):
    ext = file.split('.')[-1]
    if ext != 'csv':
        print('エラー：対応していないファイル形式です。選択可能な形式：.csv')
        return
    aliases = []
    with open(file, 'r', encoding='utf-8') as f:
        aliases = f.readlines()
        #参考 f.read().splitlines()で改行を入れないこともできる
    for target in targets:
        remote_bashrc = f'{target}:~/.bashrc'
        local_bashrc = f'./bashrc_{target}'
        print_call(f'scp {remote_bashrc} {local_bashrc}')
        new_bashrc_lines = []
        with open(local_bashrc, 'r', encoding='utf-8') as f:
            current_bashrc_lines = f.readlines()
            for line in current_bashrc_lines:
                if not line.startswith('alias'):
                    new_bashrc_lines.append(line)
        cmd_shorts = []
        for alias in aliases:
            if len(alias.split(',')) != 2:
                # 不要な行は無視
                continue
            # 変換
            if ext == 'csv':
                cmd_short, cmd = [c.strip() for c in alias.split(',')]
                same_alias_flg = False
                if cmd_short in cmd_shorts:
                    print(f'エラー：重複したエイリアス：{cmd_short}')
                    same_alias_flg = True
                cmd_shorts.append(cmd_short)
                alias = f'alias {cmd_short}=\'{cmd}\'\n'
            new_bashrc_lines.append(alias)
        if same_alias_flg:
            return
        with open(local_bashrc, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(new_bashrc_lines)   
        print_call(f'scp {local_bashrc} {remote_bashrc}')
        #reload_cmd = 'source\ ~\/.bashrc'
        #profile = '~/.bash_profile'
        #print_call(f'ssh {target} sed -i \'s/{reload_cmd}//g\' {profile};echo {reload_cmd} >> {profile}')

if __name__ == '__main__':
    s_time = time.time()
    file = 'alias_common.csv'
    targets = ['tjvm1']
    scp_alias(file, targets)
    f_time = time.time()
    e_time = f_time - s_time
    print(f'経過時間: {e_time:.1f}秒')
        

