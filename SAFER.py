import math
  
def discrete_log(b, a=45, m=257):
    '''DISCRETE LOGARITHM'''
    n = int(math.sqrt (m) + 1) 
    an = 1
    
    for i in range(n): 
        an = (an * a) % m
        
    value = [0] * m  
    cur = an
    
    for i in range(1, n + 1): 
        if (value[ cur ] == 0): 
            value[ cur ] = i
        cur = (cur * an) % m
      
    cur = b
    
    for i in range(n + 1): 
        if (value[cur] > 0): 
            ans = value[cur] * n - i
            if (ans < m): 
                return ans
        cur = (cur * a) % m
  
    return -1

def init_list_of_objects(size):
    '''GENERATES LISTS WITH AS MANY LISTS AS REQUIRED'''
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append( list() )
        
    return list_of_objects

def binary_rotation_by_three(rounds, obj):
    '''<<<3'''
    for i in range(rounds):
        obj = obj[3:9] + obj[0:3]
        i += 1
        
    return int(obj, 2)

def get_binar(obj):
    '''GET BINAR AND ORD LISTS FROM CHARACTERS'''
    list_of_ord = []
    list_of_binar = []

    for i in obj:
        temp = '{0:08b}'.format(ord(i))
        list_of_ord.append(ord(i))
        list_of_binar.append('{0:08b}'.format(ord(i)))
        
    return list_of_binar, list_of_ord


def encryption_constant(rounds, bits=8):
    constants_arr = init_list_of_objects(rounds*2)
    for i in range(1, rounds*2+1):
        for j in range(bits):
            constant = 45**((45**((9*(i+1)+j+1)%256))%257)%257
            constants_arr[i-1].insert(j, constant)
            
    return constants_arr
           

def key_generator(rounds, list_of_key_binar, constants_arr):
    list_of_generated_keys = init_list_of_objects(rounds*2)
    for i in range(len(constants_arr)):
        for j in range(len(list_of_key_binar)):
            rotated_key_int = binary_rotation_by_three(i+1, list_of_key_binar[j])
            result_key = (rotated_key_int + constants_arr[i][j])%256
            list_of_generated_keys[i].insert(j, result_key)
            
    return list_of_generated_keys

def ord_to_chr(list_of_ords):
    string_of_chrs = str()
    for i in range(len(list_of_ords)):
        string_of_chrs += chr(list_of_ords[i])

    return string_of_chrs


def encryptor(message, key, rounds):
    '''MAIN ENCRYPTOR'''
    list_of_message_binar, list_of_message_ord = get_binar(message)
    list_of_key_binar, list_of_key_ord = get_binar(key)
    encrypt_const = encryption_constant(rounds)
    list_of_generated_key = key_generator(rounds, list_of_key_binar, encrypt_const)
    list_of_generated_key.insert(0, list_of_key_ord)
    temp_result = []
    temp_result2 = []

    #Print user key
    print("\n->User Key:")
    print('\t\t'.join(list(key)))
    print('\t\t'.join(str(i) for i in list_of_key_ord))
    print('\t'.join(str(i) for i in list_of_key_binar))

    #find encryption constants
    print("\n->Encryption Constants:")
    for j in range(len(encrypt_const)):
        print("B"+str(j+1)+"\t" + '\t'.join(str(i) for i in encrypt_const[j]))

    #find keys
    print("\n->Keys:")
    for j in range(1, len(list_of_generated_key)):
        print("Key-"+str(j+1)+"\t" + '\t'.join(str(i) for i in list_of_generated_key[j]))    
    

    print("\nEncryption")
    round_number = 1
    for r in range(0, rounds*2-1, 2):
        print("Round #" + str(round_number))
        
        #1st phase
        for i in range(len(list_of_message_ord)):
            if i in(0,3,4,7):
                temp = list_of_message_ord[i] ^ list_of_generated_key[r][i]
            else:
                temp = (list_of_message_ord[i] + list_of_generated_key[r][i])%256
            temp_result.append(temp)
        print("->1st phase results:")
        print("Mess\t" + '\t'.join(str(i) for i in list_of_message_ord))
        print("Oper\tXOR\tSUM\tSUM\tXOR\tXOR\tSUM\tSUM\tXOR")
        print("Key-"+str(r+1)+"\t" + '\t'.join(str(i) for i in list_of_generated_key[r]))
        print("RESL\t" + '\t'.join(str(i) for i in temp_result))
            
        #2nd phase
        for i in range(len(temp_result)):
            if i in(0,3,4,7):
                if temp_result[i] == 128:
                    temp = 0
                else:
                    temp = (45 ** temp_result[i])%257
            else:
                if temp_result[i] == 0:
                    temp = 128
                else:
                    temp = discrete_log(temp_result[i])
            temp_result2.append(temp)
        print("\n->2nd phase results:")
        print("Mess\t" + '\t'.join(str(i) for i in temp_result))
        print("Oper\tPOW\tLOG\tLOG\tPOW\tPOW\tLOG\tLOG\tPOW")
        print("RESL\t" + '\t'.join(str(i) for i in temp_result2))
        temp_result = []

        #3rd phase
        for i in range(len(temp_result2)):
            if i in(0,3,4,7):
                temp = (temp_result2[i] + list_of_generated_key[r+1][i])%256
            else:
                temp = temp_result2[i] ^ list_of_generated_key[r+1][i]
            temp_result.append(temp)
        print("\n->3rd phase results:")
        print("Mess\t" + '\t'.join(str(i) for i in temp_result2))
        print("Oper\tSUM\tXOR\tXOR\tSUM\tSUM\tXOR\tXOR\tSUM")
        print("Key-"+str(r+2)+"\t" + '\t'.join(str(i) for i in list_of_generated_key[r+1]))
        print("RESL\t" + '\t'.join(str(i) for i in temp_result))
        temp_result2 = []

        #4th phase - Hadamard
        print("\n->4th phase results:")
        print("Mess\t" + '\t'.join(str(i) for i in temp_result))
        for i in range(3):
            for j in range(len(temp_result)):
                if j%2==0:
                    temp1 = (2*temp_result[j] + temp_result[j+1]) % 256
                    temp2 = (temp_result[j] + temp_result[j+1]) % 256
                    temp_result[j] = temp1
                    temp_result[j+1] = temp2
            
            print(i+1, "rnd\t" + '\t'.join(str(i) for i in temp_result))
        list_of_message_ord = temp_result
        temp_result = []
        round_number += 1
        print("")

    #Final phase
    for i in range(len(list_of_message_ord)):
        if i in(0,3,4,7):
            temp = list_of_message_ord[i] ^ list_of_generated_key[-1][i]
        else:
            temp = (list_of_message_ord[i] + list_of_generated_key[-1][i])%256
        temp_result.append(temp)
    print("\nFINAL PHASE RESULTS:")
    print("Mess\t" + '\t'.join(str(i) for i in list_of_message_ord))
    print("Oper\tXOR\tSUM\tSUM\tXOR\tXOR\tSUM\tSUM\tXOR")
    print("Key-" + str(len(list_of_generated_key)) +"\t" + '\t'.join(str(i) for i in list_of_generated_key[-1]))
    print("RESL\t" + '\t'.join(str(i) for i in temp_result))

    #Result message
    encoded_message = ord_to_chr(temp_result)
    print("\nEncoded message based on result from above:\n" + encoded_message)
        

message = str(input('Message: '))
key = str(input('Key: '))
rounds = int(input('# of rounds: '))

encryptor(message, key, rounds)
