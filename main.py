import hashlib

import requests


def request_provider(query):
    url = "https://api.pwnedpasswords.com/range/" + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('Error fetching the results... Try again')
    return res


def password_api_check(password):
    shaKey = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5char, tail = shaKey[:5], shaKey[5:]
    response = request_provider(first5char)
    return password_leak_counts(response, tail)


def password_leak_counts(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def main():
    argument = []
    n = int(input("Enter number of passwords you wanna try: "))
    for i in range(0, n):
        ele = input()
        argument.append(ele)

    for passwords in argument:
        count_pass = password_api_check(passwords)
        if count_pass:
            print(f' {passwords} found {count_pass} times')
        else:
            print("{passwords} found 0 times")

    return "done"


if __name__ == '__main__':
    main()
