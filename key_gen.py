import base64

from Crypto.Hash import SHA1, SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util.asn1 import DerSequence, DerObjectId, DerNull, DerOctetString
from Crypto.Util.number import ceil_div
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


# noinspection PyTypeChecker
def pkcs15_encode(msg_hash, emLen, with_hash_parameters=True):
    """
    Implement the ``EMSA-PKCS1-V1_5-ENCODE`` function, as defined
    :param msg_hash: hash object
    :param emLen: int
    :param with_hash_parameters: bool
    :return: An ``emLen`` byte long string that encodes the hash.
    """
    digestAlgo = DerSequence([DerObjectId(msg_hash.oid).encode()])

    if with_hash_parameters:
        digestAlgo.append(DerNull().encode())

    digest = DerOctetString(msg_hash.digest())
    digestInfo = DerSequence([
        digestAlgo.encode(),
        digest.encode()
    ]).encode()

    # We need at least 11 bytes for the remaining data: 3 fixed bytes and
    # at least 8 bytes of padding).
    if emLen < len(digestInfo) + 11:
        raise TypeError("Selected hash algorithm has a too long digest (%d bytes)." % len(digest))
    PS = b'\xFF' * (emLen - len(digestInfo) - 3)
    return b'\x00\x01' + PS + b'\x00' + digestInfo

# 这里是自己生成的证书 ca.crt
certBase64 = ""
cert = x509.load_der_x509_certificate(base64.b64decode(certBase64))
public_key = cert.public_key()
sign = int.from_bytes(cert.signature, byteorder="big", )
print(f"sign:{sign}")

modBits = public_key.key_size
digest_cert = SHA256.new(cert.tbs_certificate_bytes)
r = int.from_bytes(pkcs15_encode(digest_cert, ceil_div(modBits, 8)), byteorder='big', signed=False)
print(f"result:{r}")

licenseId = 'I1EKS18DABCM4KU'
licensePart = '{"licenseId":"I1EKS18DABCM4KU","licenseeName":"lWoHvYe","licenseeType":"PERSONAL","assigneeName":"","assigneeEmail":"","licenseRestriction":"","checkConcurrentUse":false,"products":[{"code":"PCWMP","fallbackDate":"2030-12-21","paidUpTo":"2030-12-21","extended":true},{"code":"CL","fallbackDate":"2030-12-21","paidUpTo":"2030-12-21","extended":false},{"code":"PSI","fallbackDate":"2030-12-21","paidUpTo":"2030-12-21","extended":true}],"metadata":"0220240701PSAX000005X","hash":"12345678/0321581538","gracePeriodDays":7,"autoProlongated":false,"isAutoProlongated":false,"trial":false,"aiAllowed":true}'

digest = SHA1.new(licensePart.encode('utf-8'))

with open('ca.key') as prifile:
    private_key = RSA.import_key(prifile.read())
    # 使用私钥对HASH值进行签名
    signature = pkcs1_15.new(private_key).sign(digest)

    sig_results = base64.b64encode(signature)
    licensePartBase64 = base64.b64encode(bytes(licensePart.encode('utf-8')))
    public_key.verify(
        base64.b64decode(sig_results),
        base64.b64decode(licensePartBase64),
        padding=padding.PKCS1v15(),
        algorithm=hashes.SHA1(),
    )
    result = licenseId + "-" + licensePartBase64.decode('utf-8') + "-" + sig_results.decode('utf-8') + "-" + certBase64
    print(result)
