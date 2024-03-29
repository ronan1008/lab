import hmac, base64, struct, hashlib, time

def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    token = str(get_hotp_token(secret, intervals_no=int(time.time())//30))
    if len(token) == 5:
        token = '0{}'.format(token)

    return token



#print(get_totp_token('6RJFVNCMKMOG62SU'))
