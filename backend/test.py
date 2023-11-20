import re

text = "ukTJ0BixlREz@yooutu.vip----KbKilybdZdEw----2XL8RjDrlPyh@rdddre.com" \
       "JMY2i3v9koNk@yooutu.vip----ztlCjNft28hr----0gBgn7C9K83B@tedfwe.com" \
       "Ird0pGu6wIhA@yooutu.vip----dINVMp67A8qg----vXH7jONSQhjP@yjyqwe.com" \
       "owmmGQjzljQ6@yooutu.vip----Q7cB634OXSL5----0PZSo4sQo0lE@wugfeq.com" \
       "fVK3rOZ6zLhQ@yooutu.vip----lefALv1xZWeT----4IrHLaBOMeQA@rdddre.com" \
       "Hq3IKvI9j0RP@yooutu.vip----ud1JtK36KutZ----lnXOdEk7NBZJ@tedfwe.com" \
       "bXtlwh7RY6ih@yooutu.vip----0uwE75zzEGlv----Q5dYA27cxiew@yjyqwe.com" \
       "wEtZCkQlciPE@yooutu.vip----nzKDUPnwh5Y9----h73Enh4FkTWQ@wugfeq.com" \
       "zdN3Z4mSgwSj@yooutu.vip----UBCgogupeyId----zaIZ3EoEhvC4@rdddre.com" \
       "da998YyupiBU@yooutu.vip----shKwwP8yfYxy----RaciPdqYDtef@tedfwe.com" \
       "H8DiKqlAVttb@yooutu.vip----80QNMzDaQa2N----oiV0hoBGWZXu@yjyqwe.com"


# 使用正则表达式匹配多行文本
pattern = r"([^\-]+)----([^\-]+)----([^@]+@[^@]+)"
matches = re.findall(pattern, text)

if matches:
    # 遍历匹配的结果
    for match in matches:
        # 提取匹配的部分并存入列表
        email = match[0]
        password = match[1]
        related_email = match[2]

        # 打印提取的值
        print("Email:", email)
        print("Password:", password)
        print("Related Email:", related_email)
else:
    print("No matches found.")