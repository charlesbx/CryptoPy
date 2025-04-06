import numpy as np
from src.utils import hex_to_bytes, bytes_to_hex, break_into_blocks

class AES:
    def __init__(self, key):
        self.key = key
        self.key_size = len(key)
        self.block_size = 16
        self.rounds = 10
        self.aes_sbox = np.array([
            [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
            [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
            [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
            [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
            [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
            [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
            [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
            [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
            [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
            [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
            [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
            [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
            [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
            [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
            [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
            [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]], dtype=np.uint16)
        
        self.aes_inv_sbox = np.array([
            [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
            [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
            [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
            [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
            [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
            [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
            [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
            [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
            [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
            [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
            [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
            [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
            [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
            [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
            [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
            [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]], dtype=np.uint16)
        
        self.aes_rcon = np.array([
            [0x01, 0x00, 0x00, 0x00],
            [0x02, 0x00, 0x00, 0x00],
            [0x04, 0x00, 0x00, 0x00],
            [0x08, 0x00, 0x00, 0x00],
            [0x10, 0x00, 0x00, 0x00],
            [0x20, 0x00, 0x00, 0x00],
            [0x40, 0x00, 0x00, 0x00],
            [0x80, 0x00, 0x00, 0x00],
            [0x1b, 0x00, 0x00, 0x00],
            [0x36, 0x00, 0x00, 0x00]], dtype=np.uint16)
        
        self.key_schedule = np.zeros((self.rounds + 1, 4, 4), dtype=np.uint16)
        
        self.KeyExpansion()
        
    def KeyExpansion(self):
        key = hex_to_bytes(self.key)
        if len(key) != 16:
            raise Exception('ERROR: invalid key length')
        key = key.reshape((4, 4))
        for i in range(4):
            for j in range(4):
                self.key_schedule[0][i][j] = key[i][j]
        for i in range(1, self.rounds + 1):
            for j in range(4):
                if j == 0:
                    temp = self.key_schedule[i - 1][3]
                    temp = np.roll(temp, -1)
                    temp = np.array([self.aes_sbox[temp[i]//16][temp[i]%16] for i in range(4)], dtype=np.uint16)
                    temp = temp ^ self.aes_rcon[i - 1]
                    self.key_schedule[i][j] = self.key_schedule[i - 1][j] ^ temp
                else:
                    self.key_schedule[i][j] = self.key_schedule[i - 1][j] ^ self.key_schedule[i][j - 1]
            
    def AddRoundKey(self, block, key):
        block = np.array(block, dtype=np.uint16)
        block = block.reshape((4, 4))
        key = np.array(key, dtype=np.uint16)
        key = key.reshape((4, 4))
        return (block ^ key).flatten()

    def SubBytes(self, block):
        block = np.array(block, dtype=np.uint16)
        block = block.reshape((4, 4))
        for i in range(4):
            for j in range(4):
                block[i][j] = self.aes_sbox[block[i][j]//16][block[i][j]%16]
        return block.flatten()
    
    def ShiftRows(self, block):
        block = np.array(block, dtype=np.uint16)
        block = block.reshape((4, 4))
        new_block = np.zeros((4, 4), dtype=np.uint16)
        # 1st row
        new_block[0][0] = block[0][0]
        new_block[0][1] = block[1][1]
        new_block[0][2] = block[2][2]
        new_block[0][3] = block[3][3]
        # 2nd row
        new_block[1][0] = block[1][0]
        new_block[1][1] = block[2][1]
        new_block[1][2] = block[3][2]
        new_block[1][3] = block[0][3]
        # 3rd row
        new_block[2][0] = block[2][0]
        new_block[2][1] = block[3][1]
        new_block[2][2] = block[0][2]
        new_block[2][3] = block[1][3]
        # 4th row
        new_block[3][0] = block[3][0]
        new_block[3][1] = block[0][1]
        new_block[3][2] = block[1][2]
        new_block[3][3] = block[2][3]
        return new_block.flatten()
    
    def MixColumns(self, block):
        block = np.array(block, dtype=np.uint16)
        block = block.reshape((4, 4))
        new_block = np.zeros((4, 4), dtype=np.uint16)
        for i in range(4):
            new_block[i] = self.MixColumn(block[i])
        return new_block.flatten()

    def gmul2(self, byte):
        s = byte << 1
        s &= 0xff
        if (byte & 128) != 0:
            s ^= 0x1b
        return s
    
    def gmul3(self, byte):
        return self.gmul2(byte) ^ byte
    
    def MixColumn(self, col):
        r = np.zeros(4, dtype=np.uint16)
        r[0] = self.gmul2(col[0]) ^ self.gmul3(col[1]) ^ col[2] ^ col[3]
        r[1] = self.gmul2(col[1]) ^ self.gmul3(col[2]) ^ col[3] ^ col[0]
        r[2] = self.gmul2(col[2]) ^ self.gmul3(col[3]) ^ col[0] ^ col[1]
        r[3] = self.gmul2(col[3]) ^ self.gmul3(col[0]) ^ col[1] ^ col[2]
        return r
    
    def InvSubBytes(self, block):
        block = np.array(block, dtype=np.uint16)
        block = block.reshape((4, 4))
        for i in range(4):
            for j in range(4):
                block[i][j] = self.aes_inv_sbox[block[i][j]//16][block[i][j]%16]
        return block.flatten()

    def InvShiftRows(self, block):
        block = np.array(block, dtype=np.uint16)
        block = block.reshape((4, 4))
        new_block = np.zeros((4, 4), dtype=np.uint16)
        # 1st row
        new_block[0][0] = block[0][0]
        new_block[0][1] = block[3][1]
        new_block[0][2] = block[2][2]
        new_block[0][3] = block[1][3]
        # 2nd row
        new_block[1][0] = block[1][0]
        new_block[1][1] = block[0][1]
        new_block[1][2] = block[3][2]
        new_block[1][3] = block[2][3]
        # 3rd row
        new_block[2][0] = block[2][0]
        new_block[2][1] = block[1][1]
        new_block[2][2] = block[0][2]
        new_block[2][3] = block[3][3]
        # 4th row
        new_block[3][0] = block[3][0]
        new_block[3][1] = block[2][1]
        new_block[3][2] = block[1][2]
        new_block[3][3] = block[0][3]
        return new_block.flatten()
    
    def InvMixColumns(self, block):
        block = np.array(block, dtype=np.uint16)
        block = block.reshape((4, 4))
        new_block = np.zeros((4, 4), dtype=np.uint16)
        for i in range(4):
            new_block[i] = self.InvMixColumn(block[i])
        return new_block.flatten()

    def InvMixColumn(self, col):
        r = np.zeros(4, dtype=np.uint16)
        r[0] = self.gmul14(col[0]) ^ self.gmul11(col[1]) ^ self.gmul13(col[2]) ^ self.gmul9(col[3])
        r[1] = self.gmul9(col[0]) ^ self.gmul14(col[1]) ^ self.gmul11(col[2]) ^ self.gmul13(col[3])
        r[2] = self.gmul13(col[0]) ^ self.gmul9(col[1]) ^ self.gmul14(col[2]) ^ self.gmul11(col[3])
        r[3] = self.gmul11(col[0]) ^ self.gmul13(col[1]) ^ self.gmul9(col[2]) ^ self.gmul14(col[3])
        return r

    def gmul9(self, byte):
        return self.gmul2(self.gmul2(self.gmul2(byte))) ^ byte

    def gmul11(self, byte):
        return self.gmul2(self.gmul2(self.gmul2(byte))) ^ self.gmul2(byte) ^ byte
    
    def gmul13(self, byte):
        return self.gmul2(self.gmul2(self.gmul2(byte))) ^ self.gmul2(self.gmul2(byte)) ^ byte

    def gmul14(self, byte):
        return self.gmul2(self.gmul2(self.gmul2(byte))) ^ self.gmul2(self.gmul2(byte)) ^ self.gmul2(byte)
    
    def decipher_block(self, message):
        message = hex_to_bytes(message)
        message = self.AddRoundKey(message, self.key_schedule[self.rounds])
        for i in range(self.rounds - 1, 0, -1):
            message = self.InvShiftRows(message)
            message = self.InvSubBytes(message)
            message = self.AddRoundKey(message, self.key_schedule[i])
            message = self.InvMixColumns(message)
        message = self.InvShiftRows(message)
        message = self.InvSubBytes(message)
        message = self.AddRoundKey(message, self.key_schedule[0])
        return bytes_to_hex(message)
        
    def cipher_block(self, message):
        message = hex_to_bytes(message)
        message = self.AddRoundKey(message, self.key_schedule[0])
        for i in range(1, self.rounds):
            message = self.SubBytes(message)
            message = self.ShiftRows(message)
            message = self.MixColumns(message)
            message = self.AddRoundKey(message, self.key_schedule[i])
        message = self.SubBytes(message)
        message = self.ShiftRows(message)
        message = self.AddRoundKey(message, self.key_schedule[self.rounds])
        return bytes_to_hex(message)
    
    def cipher(self, message):
        message = message.replace('\n', '')
        blocks = [message]
        if len(message) > self.block_size * 2:
            blocks = break_into_blocks(message)
        if len(blocks[-1]) < self.block_size * 2:
            blocks[-1] = hex_to_bytes(blocks[-1])
            blocks[-1] = np.pad(blocks[-1], (0, self.block_size - len(blocks[-1])), 'constant', constant_values=(0, 0))
            blocks[-1] = bytes_to_hex(blocks[-1])
        cipher = ''
        for block in blocks:
            cipher += self.cipher_block(block)
        return cipher
    
    def decipher(self, message):
        blocks = [message]
        if len(message) > self.block_size * 2:
            blocks = break_into_blocks(message)
        decipher = ''
        for block in blocks:
            decipher += self.decipher_block(block)
        decipher = hex_to_bytes(decipher)
        for elem in decipher[::-1]:
            if elem == 0:
                decipher = decipher[:-1]
            else:
                break
        decipher = bytes_to_hex(decipher)
        return decipher