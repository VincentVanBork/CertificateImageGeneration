import pandas as pd
from PIL import ImageFont, ImageDraw, Image


df = pd.read_excel(r"rejestracja.xlsx")
print("\n\noring:\n", df.head())

df = df.replace(r"\r+|\n+|\t+", "", regex=True)
# print("\n\nsorted\n", df.head())

df1 = df[df.isna().any(axis=1)]
df1.to_csv("brakuje_danych_o_cert.csv", index=False)

fillna_values = {"Certificate": "Nie"}
df = df.fillna(value=fillna_values)

df2 = df[df["Certificate"].str.contains("nie|Nie")]
df2.to_csv("brak_zgody_na_cert.csv", index=False)

df = df[df["Certificate"].str.contains("tak|TAK")]
print("\n\nOnly yes: \n", df.head())


def choose_longer(series):
    return max(series, key=len)


df = df.groupby("E-mail")["Name"].agg(choose_longer).reset_index()
# df = df.drop_duplicates(subset=["E-mail"], keep="first")

df3 = df[~df["Name"].str.strip().str.contains(" ")]
df3.to_csv("brak_nazwiska.csv", index=False)

df = df.sort_values(by="Name", key=lambda x: x.str.len())
df["Name"] = df["Name"].str.title()
df.to_csv("lista_do_wysyłki.csv", index=False)

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
    pil_im: Image.Image = Image.open("certificate.png")

    draw = ImageDraw.Draw(pil_im)

    draw.text(
        (1004, 803),
        # (pil_im.width - 600, pil_im.height - 810),
        row["Name"],
        font=font,
        align="center",
        fill=(2, 12, 90),
        anchor="mm",
        stroke_width=2,
    )
    email = row["E-mail"]
    if email:
        pil_im.save(f"./certs/{email}.png")
    else:
        print(row["Name"], "NIE PODAŁO EMAILA")
