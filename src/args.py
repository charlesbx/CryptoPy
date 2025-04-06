from sys import stderr, exit
from src.utils import is_prime

class Args:
    def __init__(self, argv):
        try:
            self.argv = argv
            self.args = {
                'help': False,
                'xor': False,
                'aes': False,
                'rsa': False,
                'pgp': False,
                'cipher': False,
                'decipher': False,
                'block': False,
                'generate': False,
                'p': None,
                'q': None,
                'key': None,
                'message': None
            }
            self.parse()
            self.check_inconsistencies()
            self.check_values()
        except Exception as e:
            print(e, file=stderr)
            exit(84)
            
    def check_values(self):
        if self.args['p'] != None:
            p = self.args['p']
            try:
                p = bytearray.fromhex(p)
                p = int.from_bytes(p, byteorder='little')
                if is_prime(p) == False:
                    raise Exception()
            except:
                raise Exception('Invalid argument: P must be a prime number in a hexadecimal format')
        if self.args['q'] != None:
            q = self.args['q']
            try:
                q = bytearray.fromhex(q)
                q = int.from_bytes(q, byteorder='little')
                if is_prime(q) == False:
                    raise Exception()
            except:
                raise Exception('Invalid argument: Q must be a prime number in a hexadecimal format')
        if self.args['key'] != None:
            key = self.args['key']
            try:
                key = bytearray.fromhex(key)
            except:
                try:
                    part1, part2 = key.split('-')
                    part1 = bytearray.fromhex(part1)
                    part2 = bytearray.fromhex(part2)
                except:
                    raise Exception('Invalid argument: KEY must be a hexadecimal string')
        if self.args['message'] != None:
            message = self.args['message']
            try:
                message = bytearray.fromhex(message)
                print(message)
            except:
                raise Exception('Invalid argument: MESSAGE must be a hexadecimal string')
            
    def parse(self):
        argv = self.argv[1:]
        for arg in argv:
            if arg == '-h' or arg == '--help':
                self.args['help'] = True
            elif arg == '-xor':
                self.args['xor'] = True
            elif arg == '-aes':
                self.args['aes'] = True
            elif arg == '-rsa':
                self.args['rsa'] = True
            elif arg == '-pgp':
                self.args['pgp'] = True
            elif arg == '-c':
                self.args['cipher'] = True
            elif arg == '-d':
                self.args['decipher'] = True
            elif arg == '-b':
                self.args['block'] = True
            elif arg == '-g':
                self.args['generate'] = True
            elif self.args['p'] == None and self.args['generate']:
                self.args['p'] = arg
            elif self.args['q'] == None and self.args['generate']:
                self.args['q'] = arg
            elif self.args['key'] == None:
                self.args['key'] = arg
            else:
                raise Exception('Invalid argument: ' + arg)

    def check_inconsistencies(self):
        if self.args['xor']:
            if self.args['aes'] or self.args['rsa'] or self.args['pgp']:
                raise Exception('Invalid argument: -xor can\'t be used with -aes, -rsa or -pgp')
            if not self.args['cipher'] and not self.args['decipher']:
                raise Exception('Invalid argument: -xor must be used with -c or -d')
            if self.args['cipher'] and self.args['decipher']:
                raise Exception('Invalid argument: -xor must be used with -c or -d')
            if self.args['generate']:
                raise Exception('Invalid argument: -xor can\'t be used with -g')
        elif self.args['aes']:
            if self.args['xor'] or self.args['rsa'] or self.args['pgp']:
                raise Exception('Invalid argument: -aes can\'t be used with -xor, -rsa or -pgp')
            if not self.args['cipher'] and not self.args['decipher']:
                raise Exception('Invalid argument: -aes must be used with -c or -d')
            if self.args['cipher'] and self.args['decipher']:
                raise Exception('Invalid argument: -aes must be used with -c or -d')
            if self.args['generate']:
                raise Exception('Invalid argument: -aes can\'t be used with -g')
        elif self.args['rsa']:
            if self.args['xor'] or self.args['aes'] or self.args['pgp']:
                raise Exception('Invalid argument: -rsa can\'t be used with -xor, -aes or -pgp')
            if not self.args['cipher'] and not self.args['decipher'] and not self.args['generate']:
                raise Exception('Invalid argument: -rsa must be used with -c or -d')
            if self.args['cipher'] and self.args['decipher']:
                raise Exception('Invalid argument: -rsa must be used with -c or -d')
            if self.args['block']:
                raise Exception('Invalid argument: -rsa can\'t be used with -b')
        elif self.args['pgp']:
            if self.args['xor'] or self.args['aes'] or self.args['rsa']:
                raise Exception('Invalid argument: -pgp can\'t be used with -xor, -aes or -rsa')
            if not self.args['cipher'] and not self.args['decipher']:
                raise Exception('Invalid argument: -pgp must be used with -c or -d')
            if self.args['cipher'] and self.args['decipher']:
                raise Exception('Invalid argument: -pgp must be used with -c or -d')
            if self.args['block']:
                raise Exception('Invalid argument: -pgp can\'t be used with -b')
            if self.args['generate']:
                raise Exception('Invalid argument: -pgp can\'t be used with -g')
        else:
            raise Exception('Invalid argument: no algorithm selected')
        if self.args['generate']:
            if self.args['p'] == None or self.args['q'] == None:
                raise Exception('Invalid argument: -g must be used with P and Q')
            if self.args['key'] != None:
                raise Exception('Invalid argument: -g can\'t be used with KEY')
        else:
            if self.args['p'] != None or self.args['q'] != None:
                raise Exception('Invalid argument: P and Q can\'t be used without -g')
            if self.args['key'] == None:
                raise Exception('Invalid argument: KEY must be used')

    def help(self):
        print('USAGE\n\t./mypgp [-xor | -aes | -rsa | -pgp] [-c | -d] [-b] KEY\n\tthe MESSAGE is read from the standard input')
        print('DESCRIPTION\n\t-xor\tcomputation using the XOR algorithm\n\t-aes\tcomputation using the AES algorithm\n\t-rsa\tcomputation using the RSA algorithm\n\t-pgp\tcomputation using the PGP algorithm')
        print('\t-c\tMESSAGE is clear and we want to cipher it\n\t-d\tMESSAGE is ciphered and we want to decipher it')
        print('\t-b\tblock mode: for xor and aes, only works on one block MESSAGE and KEY must be of the same size')
        print('\t-g P Q\tfor RSA only: generate a public and private key pair from the prime number P and Q')