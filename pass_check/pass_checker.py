import hashlib
import sys
import requests 


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    
    if res.status_code != 200:
        raise RuntimeError(f'fetched error: {res.status_code}, check the code and run again. Thank you!')
    return res

def get_pass_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    # print(hashlib.sha1(password.encode('utf_8')).hexdigest())
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    
    response = request_api_data(first5_char)
    return get_pass_leak_count(response, tail)

def main(passwords):
        
    with open('pass_slot.txt', mode='r') as hacked:
        my_file = hacked.read()
        for passwords in my_file:
            check_hacked = pwned_api_check(passwords)
            length_of_password = len(my_file) * '*'
            # print(length_of_password)
            if check_hacked:
                print(f'your password {length_of_password} was hacked {check_hacked} times. you should probably change it.')
                break
            
        return 'you are secured!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[:]))
# request_api_data('123')
 