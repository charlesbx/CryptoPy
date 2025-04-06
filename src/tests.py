from src.aes import AES

def test_AES():
    from src.utils import hex_to_bytes, bytes_to_hex
    import numpy as np
    aes = AES('1050a92515d65555d450eb456821e981')
    # cipher by hand
    message = aes.AddRoundKey(aes.key_schedule[0], np.array([0x14,0x15,0x16,0x17,0x10,0x11,0x12,0x13,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1F,0x20]).reshape((4, 4)))
    message = aes.SubBytes(message)
    message = aes.ShiftRows(message)
    message = aes.MixColumns(message)
    message = aes.AddRoundKey(message, aes.key_schedule[1])
    for i in range(2, 10):
        message = aes.SubBytes(message)
        message = aes.ShiftRows(message)
        message = aes.MixColumns(message)
        message = aes.AddRoundKey(message, aes.key_schedule[i])
    print("\n|-----------CIPHER BEFORE FINAL HEX STRING-----------|\n")
    print("Got: ", bytes_to_hex(message))
    print("Expecting: ", bytes_to_hex(np.array([8, 57, 71, 243, 158, 131, 41, 188, 68, 232, 158, 26, 173, 103, 167, 213])))
    print("\n|-------------CIPHER BEFORE FINAL BYTES--------------|\n")
    print("Got: ", message)
    print("Expecting: ", np.array([8, 57, 71, 243, 158, 131, 41, 188, 68, 232, 158, 26, 173, 103, 167, 213]))    

    # cipher
    message = aes.cipher(bytes_to_hex(np.array([0x14,0x15,0x16,0x17,0x10,0x11,0x12,0x13,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1F,0x20])))
    print("\n|-----------------CIPHER HEX STRING------------------|\n")
    print("Got: ", message)
    print("Expecting: ", bytes_to_hex(np.array([236, 75, 229, 151, 119, 84, 163, 44, 80, 170, 210, 33, 124, 90, 104, 198])))
    print("\n|-------------------CIPHER BYTES---------------------|\n")
    print("Got: ", hex_to_bytes(message))
    print("Expecting: ", np.array([236, 75, 229, 151, 119, 84, 163, 44, 80, 170, 210, 33, 124, 90, 104, 198]))

    # decipher
    message = aes.decipher(message)
    print("\n|----------------DECIPHER HEX STRING-----------------|\n")
    print("Got: ", message)
    print("Expecting: ", bytes_to_hex(np.array([0x14,0x15,0x16,0x17,0x10,0x11,0x12,0x13,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1F,0x20])))
    print("\n|------------------DECIPHER BYTES--------------------|\n")
    print("Got: ", hex_to_bytes(message))
    print("Expecting: ", np.array([0x14,0x15,0x16,0x17,0x10,0x11,0x12,0x13,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1F,0x20]))
    print("\n|----------------------------------------------------|")