import pandas as pd
import cv2
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import numpy as np

df = pd.read_excel(r"test.xlsx")
print("\n\noring:\n", df.head())

df = df.replace(r"\r+|\n+|\t+", "", regex=True)
# print("\n\nsorted\n", df.head())

df1 = df[df.isna().any(axis=1)]
df1.to_csv("brakuje_danych_o_cert.csv")

fillna_values = {"Certificate": "Nie"}
df = df.fillna(value=fillna_values)
df = df[df["Certificate"].str.contains("Tak")]
print("\n\nOnly yes: \n", df.head())

df = df.drop_duplicates(subset=["E-mail"], keep="first")
df = df.sort_values(by="Name", key=lambda x: x.str.len())
df.to_csv("lista_do_wysyłki.csv")

# TODO: dynamic font size
# max_name_len = df.Name.str.len().max()
# min_name_len = df.Name.str.len().min()
# print("long name", max_name_len)
# print("short name", min_name_len)

# test_name = "MW" * 8 or 36


# min_x = 150
# max_x = 1800
# min_y = 540
# max_y = 640
font = ImageFont.truetype("./font/calibril.ttf", 48)

for index, row in df.iterrows():
    pil_im = Image.open("certificate.png")

    draw = ImageDraw.Draw(pil_im)

    draw.text(
        (1000, 580),
        row["Name"],
        font=font,
        align="center",
        fill=(2, 12, 90),
        anchor="mm",
    )
    email = row["E-mail"]
    pil_im.save(f"./certs/{email}.png")
