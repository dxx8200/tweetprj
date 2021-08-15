import tweepy

def search(api, text, count=20):
    all_results = []
    left_count = count
    if left_count <= 100:
        new_results = do_search(api, text, left_count)
    else:
        new_results = do_search(api, text, 100)
    while len(new_results) > 0:
        all_results.extend(new_results)
        left_count = left_count - len(new_results)
        if left_count <= 0:
            break
        if left_count <= 100:
            new_results = do_search(api, text, left_count, all_results[-1].id-1)
        else:
            new_results = do_search(api, text, 100, all_results[-1].id-1)
    return all_results

def do_search(api, text, count = -1, max_id = -1):
    if count > 0:
        if max_id > 0:
            return api.search(q=text, count=count, max_id=max_id)
        else:
            return api.search(q=text, count=count)
    else:
        if max_id > 0:
            return api.search(q=text, max_id=max_id)
        else:
            return api.search(q=text)
