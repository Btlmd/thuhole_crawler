import requests
import json
import time
import random

headers = {
        'Referer': 'https://web.thuhole.com/',
        'TE': 'trailers',
        'TOKEN': '',
        'User-Agent': ''
}

headers_without_te = headers

proxies = {
        'http': 'socks5h://127.0.0.1:1080',
        'https': 'socks5h://127.0.0.1:1080'
}


def req_page(page:int):
    return requests.get(f"https://tapi.thuhole.com/v3/contents/post/attentions?page={page}&device=0&v=v3.0.6-455338", headers=headers, proxies=proxies)


def get_attention_pages():
    i = 1
    while True:
        with open(f'attention_page_{i}.json', 'wb') as f:
            res = req_page(i).content
            js = json.loads(str(res, encoding='utf-8'))
            f.write(res)
            print('page', i, 'done')
        if len(js['data']) == 0:
            break
        else:
            i += 1
            time.sleep(1)

def get_detail(pid):
    return requests.get(f'https://tapi.thuhole.com/v3/contents/post/detail?pid={pid}&device=0&v=v3.0.6-455338',
                        headers=headers, proxies=proxies)

def get_all_details(prefix, begin, pages):
    for i in range(begin, pages + 1):
            print('Now begin page', i)
            with open(f'{prefix}{i}.json', 'r', encoding='utf-8') as f:
                res = json.load(f)
            for hole in res['data']:
                with open(f"{hole['pid']}.json", 'wb') as f:
                    try:
                        f.write(get_detail(hole['pid']).content)
                    except:
                        time.sleep(15)
                        f.write(get_detail(hole['pid']).content)
                    print('hole', hole['pid'], 'done')
                    time.sleep(1 + random.uniform(0, 0.8))



def req_key(page, key):
    return requests.get(f'https://tapi.thuhole.com/v3/contents/search?pagesize=50&page={page}&keywords={key}&device=0&v=v3.0.6-455338', headers=headers_without_te, proxies=proxies)


def get_search_pages(key):
    i = 1
    while True:
        time.sleep(1)
        with open(f'search_page_{i}.json', 'wb') as f:
            res = req_key(i, key).content
            js = json.loads(str(res, encoding='utf-8'))
            f.write(res)
            print('page', i, 'done len', len(str(res, encoding='utf-8')))
            if len(js['data']) == 0:
                break
            else:
                i += 1
                time.sleep(1)


