import base64

original_bytes = b'Hello, world! \xe4\xbd\xa0\xe5\xa5\xbd' # 包含中文“你好”的UTF-8编码bytes
image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...' # 模拟图片二进制数据

encoded_bytes = base64.b64encode(original_bytes)  #编码之后照样是bytes对象，包含的是Base64编码后的ASCII字符
encoded_string = encoded_bytes.decode('utf-8') #解码之后，变成string对象

print("原始二进制数据:", original_bytes)
print("Base64 编码后的字符串:", encoded_string)
print("编码后字符串长度:", len(encoded_string))
print("原始二进制数据长度:", len(original_bytes))
print(f"数据大小增加比例: {(len(encoded_string) - len(original_bytes)) / len(original_bytes):.2%}")


# --- 解码 (Base64 string -> bytes) ---
# base64.b64decode 需要 bytes-like object 作为输入，所以需要 .encode('utf-8')
decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))

print("\nBase64 解码回的二进制数据:", decoded_bytes)
print("解码后的数据与原始数据是否一致:", original_bytes == decoded_bytes)

# 带有填充的例子
print("\n--- 填充示例 ---")
data_len_1 = b'A'
data_len_2 = b'AB'
data_len_3 = b'ABC'

print(f"'{data_len_1.decode()}' Base64编码: {base64.b64encode(data_len_1).decode()}") # QQ== (两个等号)
print(f"'{data_len_2.decode()}' Base64编码: {base64.b64encode(data_len_2).decode()}") # QUI= (一个等号)
print(f"'{data_len_3.decode()}' Base64编码: {base64.b64encode(data_len_3).decode()}") # QUJD (无等号)