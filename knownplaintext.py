import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

plaintext  = "Mad cow in mad space, Guten tag"
knowPlainText = "Guten t"
key="secret1"
KEY_LEN=len(key)


def cipher_xor(text,key):
    c = []

    lStr1 = len(text)
    lStr2 = len(key)
    log.debug("al = %d, bl = %d" % (lStr1, lStr2))

    if lStr1 > lStr2:
        i = 0
        z = 0
        while i < lStr1:
            if z == lStr2:
                z=0
            else:
                z=z+1
            key += key[z]
            i += 1

    elif lStr1 < lStr2:
        text += text.zfill(lStr2-lStr1)


    log.debug("al = %d, bl = %d cStr=%d" % (lStr1, lStr2, len(text)))

    for a , b in zip(text, key):
        log.debug(" %s | %s" % (a,b))
        c.append(ord(a) ^ ord(b))

    return "".join([ chr(x) for x in c])


def printMsg(message,text):
    print(message.ljust(10), end="|")

    for k in text:
        if isinstance(k,int):
            val = chr(k)
        else:
            val = k
        print("{:8s}".format(val), end=" | ")
    print()


def toBin(message,text):
    m = message.ljust(10)

    for k in text:
        if isinstance(k,str):
            m += '|' + "{:08b}".format(ord(k))
        else:
            m += '|' + "{:08b}".format(k)

    return m

def printBin(message,text):
    print(toBin(message,text))


def knowPT(cipherT,known,pl):
    i = 0
    lk = len(known) - 1
    while i < len(cipherT):
        chunck = cipherT[i:i+lk+1]
        p = pl[i:i+lk+1]
        v = cipher_xor(chunck,known)
        if p == known:
            log.info(toBin("Plaintext",p))
            log.info("----------------------------------------------")
            log.info(toBin("Cipher", chunck))
            log.info(toBin("known", known))
            log.info(toBin("XOR", v))
            log.info("Key found : [%s]" % v)
            log.info("String was %s" % cipher_xor(cipherT,v))
            break
        i += 1

cText = cipher_xor(plaintext,key)
log.info("key=" + key)
log.info("Plaintext: " + plaintext )
log.info("Ciphered : " + cText)
log.info("Unciphered : " +  cipher_xor(cText,key))
log.info("---------------------------------------")
log.info("Zig zag")
log.info("Will try to recover text from '%s' from '%s'" % (knowPlainText,cText))
knowPT(cText,knowPlainText,plaintext)



