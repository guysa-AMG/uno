import socket as sk

inst=sk.socket(sk.AF_INET6,sk.SOCK_STREAM)

inst.bind((sk.gethostbyaddr(sk.gethostname())[2][0],7777))

inst.listen()
i