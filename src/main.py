#!/usr/bin/env python3
from sys import argv
from src.args import Args
from src.xor import XOR
from src.aes import AES
from src.rsa import RSA
from src.pgp import PGP

from tests import test_AES

def main():
    arg_manager = Args(argv)
    if arg_manager.args['help']:
        arg_manager.help()
    elif arg_manager.args['xor'] and arg_manager.args['key']:
        message = input()
        arg_manager.args['message'] = message
        xor = XOR()
        if arg_manager.args['cipher'] and arg_manager.args['block']:
            print(xor.cipher_block(arg_manager.args['message'], arg_manager.args['key']))
        elif arg_manager.args['decipher'] and arg_manager.args['block']:
            print(xor.decipher_block(arg_manager.args['message'], arg_manager.args['key']))
        elif arg_manager.args['cipher']:
            print(xor.cipher(arg_manager.args['message'], arg_manager.args['key']))
        elif arg_manager.args['decipher']:
            print(xor.decipher(arg_manager.args['message'], arg_manager.args['key']))
        else:
            raise Exception('ERROR: invalid arguments')
        return
    elif arg_manager.args['aes'] and arg_manager.args['key']:
        message = input()
        arg_manager.args['message'] = message
        aes = AES(arg_manager.args['key'])
        if arg_manager.args['cipher'] and arg_manager.args['block']:
            print(aes.cipher_block(arg_manager.args['message']))
        elif arg_manager.args['decipher'] and arg_manager.args['block']:
            print(aes.decipher_block(arg_manager.args['message']))
        elif arg_manager.args['cipher']:
            print(aes.cipher(arg_manager.args['message']))
        elif arg_manager.args['decipher']:
            print(aes.decipher(arg_manager.args['message']))
        return
    elif arg_manager.args['rsa']:
        if arg_manager.args['generate']:
            rsa = RSA(arg_manager.args['p'], arg_manager.args['q'])
            rsa.generate_keys()
        elif arg_manager.args['key']:
            message = input()
            arg_manager.args['message'] = message
            rsa = RSA()
            if arg_manager.args['cipher']:
                print(rsa.cipher(arg_manager.args['message'], arg_manager.args['key']))
            elif arg_manager.args['decipher']:
                print(rsa.decipher(arg_manager.args['message'], arg_manager.args['key']))
            else:
                raise Exception('ERROR: invalid arguments')
        else:
            raise Exception('ERROR: invalid arguments')
    elif arg_manager.args['pgp'] and arg_manager.args['key']:
            message = ''
            while True:
                try:
                    message += input() + '\n'
                except EOFError:
                    break
            arg_manager.args['message'] = message
            pgp = PGP()
            if arg_manager.args['cipher']:
                print(pgp.cipher(arg_manager.args['message'], arg_manager.args['key']))
            elif arg_manager.args['decipher']:
                print(pgp.decipher(arg_manager.args['message'], arg_manager.args['key']))
            else:
                raise Exception('ERROR: invalid arguments')
    else:
        arg_manager.help()
    
if __name__ == '__main__':
    main()
    exit(0)