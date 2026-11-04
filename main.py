# © 2026 mirrder
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0.

import webview
import re
import os

# ==========================================
# АЛГОРИТМ BINC
# ==========================================
_k_val = 18861113 
_err_msg_x = "no."

_TBL_A = [
    ['a','b','c','d'], ['e','f','g','h'], ['i','j','k','l'],
    ['m','n','o','p'], ['q','r','s','t'], ['u','v','w','x'],
    ['y','z',' ',' ']
]
_TBL_B = [
    ['а','б','в','г','д','е'], ['ё','ж','з','и','й','к'], ['л','м','н','о','п','р'],
    ['с','т','у','ф','х','ц'], ['ч','ш','щ','ъ','ы','ь'], ['э','ю','я',' ', ' ', ' ']
]
_map_a = {ch: (c+1, r+1) for r, row in enumerate(_TBL_A) for c, ch in enumerate(row) if ch != ' '}
_map_b = {ch: (c+1, r+1) for r, row in enumerate(_TBL_B) for c, ch in enumerate(row) if ch != ' '}
_punc = ['.', ',', '!', '?', ';', ':', '-', '"', "'"]

class BinCAPI:
    def encrypt(self, text):
        lang = 'RU' if any('а' <= ch.lower() <= 'я' or ch.lower() == 'ё' for ch in text) else 'EN'
        _dict = _map_b if lang == 'RU' else _map_a
        fake_tag = 'EN' if lang == 'RU' else 'RU'
        out = [f'<{fake_tag}><[/]=']
        idx = 0
        for ch in text:
            if ch == ' ': out.append('%-%'); continue
            if ch in _punc: out.append(f"['{ch}']"); continue
            low = ch.lower()
            if low not in _dict: continue
            c, r = _dict[low]
            sh = (_k_val % 1000) + (idx * 13) 
            if lang == 'RU':
                c = ((c - 1 + sh) % 6) + 1
                r = ((r - 1 + sh) % 6) + 1
                truth_code = 300 + (idx % 100)
            else:
                c = ((c - 1 + sh) % 4) + 1
                r = ((r - 1 + sh) % 7) + 1
                truth_code = 400 + (idx % 100)
            if ch.isupper(): out.append('=^=')
            out.append(f"{{{c},{r},{sh}/[{truth_code}]}}")
            idx += 1
        return ''.join(out) + " [encrypted on BinC by mirrder]"

    def decrypt(self, encoded):
        if encoded == _err_msg_x or not encoded: return encoded
        truth_match = re.search(r'\[(\d)\d\d\]', encoded)
        if not truth_match: return "Ошибка: поврежденный шифр"
        real_lang = 'RU' if truth_match.group(1) == '3' else 'EN'
        tbl = _TBL_B if real_lang == 'RU' else _TBL_A
        body = re.sub(r'<[A-Z]+><HK\w+><\[/]=|<[A-Z]+><\[/]=', '', encoded)
        res = []
        is_next_up = False
        idx = 0
        i = 0
        while i < len(body):
            if body.startswith('=^=', i): is_next_up = True; i += 3; continue
            if body.startswith('%-%', i): res.append(' '); i += 3; continue
            if body.startswith("['", i):
                j = body.find("']", i)
                if j != -1:
                    res.append(body[i+2:j]); i = j + 2; continue
            if body[i] == '{':
                j = body.find('}', i)
                m = re.match(r'(\d+),\s*(\d+),\s*(\d+)', body[i+1:j])
                if m:
                    c = int(m.group(1)); r = int(m.group(2)); sh = int(m.group(3))
                    if real_lang == 'EN':
                        c = ((c - 1 - sh) % 4) + 1
                        r = ((r - 1 - sh) % 7) + 1
                    else:
                        c = ((c - 1 - sh) % 6) + 1
                        r = ((r - 1 - sh) % 6) + 1
                    try:
                        char = tbl[r-1][c-1]
                    except IndexError:
                        char = '?'
                    if char != ' ':
                        if is_next_up:
                            char = char.upper(); is_next_up = False
                        res.append(char)
                i = j + 1; continue
            i += 1
        return ''.join(res)

    def open_file(self):
        file_path = window.create_file_dialog(webview.OPEN_DIALOG, file_types=('Text Files (*.txt)', 'All files (*.*)'))
        if file_path:
            try:
                with open(file_path[0], 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                return f"Ошибка: {e}"
        return ""

    def save_file(self, text):
        file_path = window.create_file_dialog(webview.SAVE_DIALOG, file_types=('Text Files (*.txt)',))
        if file_path:
            try:
                with open(file_path[0], 'w', encoding='utf-8') as f:
                    f.write(text)
                return "Файл успешно сохранен!"
            except Exception as e:
                return f"Ошибка: {e}"
        return ""

if __name__ == '__main__':
    api = BinCAPI()
    window = webview.create_window('BinC Encryptor', 'index.html', js_api=api, width=700, height=650, background_color='#0d1117')
    webview.start()
