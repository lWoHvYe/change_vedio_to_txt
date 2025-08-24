def read_cert_base64(path):
    with open(path, "r") as f:
        lines = f.readlines()
    # 去掉头尾标记行
    lines = [line.strip() for line in lines if not line.startswith("-----")]
    return "".join(lines)

cert_str = read_cert_base64("ca.crt")
print(cert_str)
