import genanki
import pandas as pd
import random


my_model = genanki.Model(
    1189457427,
    "Shanghainese",
    fields=[
        {"name": "Chinese"},
        {"name": "Shanghainese"},
        {"name": "Pinyin"},
        {"name": "Audio"},
    ],
    templates=[
        {
            "name": "Shanghainese Card",
            "qfmt": "{{Audio}}{{Audio}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Shanghainese}}<br>{{Chinese}}<br>{{Pinyin}}',
        },
    ],
)

my_deck = genanki.Deck(1660578516, "沪语")

audio_str = "SHA - F1 - {:04d}.mp3"
audio = []
for i in range(1, 1000):
    name = audio_str.format(i)
    audio.append(f"./SHA-F1/{name}")

package = genanki.Package(my_deck)
package.media_files = audio


df = pd.read_excel("./0-1000.xlsx")
# print(df.head())


count = 1
for index, row in df.iterrows():
    # print(row["普通话"], row["沪语"], row["拼音"])
    audio_name = audio_str.format(count)

    my_note = genanki.Note(
        model=my_model,
        fields=[
            str(row["普通话"]),
            str(row["沪语"]),
            str(row["拼音"]),
            f"[sound:{audio_name}]",
        ],
    )

    my_deck.add_note(my_note)

    count += 1


package.write_to_file("./shanghainese.apkg")
