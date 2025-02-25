"""
Vasıta eki & İle bağlacı    https://tr.wikipedia.org/wiki/Vas%C4%B1ta_eki
Düzeltme işareti            https://tr.wikipedia.org/wiki/D%C3%BCzeltme_i%C5%9Fareti

Büyük ünlü uyumu:           https://tr.wikipedia.org/wiki/B%C3%BCy%C3%BCk_%C3%BCnl%C3%BC_uyumu
Son ünlüleri kalın harf olmasına karşın ince şekilde telaffuz edilen bazı alıntı kelimeler,
ince ünlü ile başlayan ekler alır çünkü kelimenin son ünsüzü ince söylenir:[3]

alkol > alkolü, hakikat > hakikati, kabul > kabulü, kontrol > kontrolü, saat > saate vb.
alkolle, hakikatle, kabulle, kontrolle, saatle vb. 😤

"""

kalin_sesliler = "aıouûâ"
ince_sesliler = "eiöüîêô"
sesli_harfler = kalin_sesliler + ince_sesliler

turkce_buyuk_kucuk_mapping = {
    "İ": "i",
    "I": "ı",
    "Ç": "ç",
    "Ş": "ş",
    "Ğ": "ğ",
    "Ü": "ü",
    "Ö": "ö",
    "Â": "â",
    "Î": "î",
    "Û": "û",
    "Ê": "ê",
    "Ô": "ô",
}

turkish_hatted = {"â": "a", "Â": "A", "î": "i", "Î": "İ", "û": "u", "Û": "U"}

def sapkasiz(kelime):
    for sapka, duz in turkish_hatted.items():
        kelime = kelime.replace(sapka, duz)

    return kelime


def turkish_lower(kelime):
    for buyuk, kucuk in turkce_buyuk_kucuk_mapping.items():
        kelime = kelime.replace(buyuk, kucuk)

    return kelime.lower()


def son_harf(kelime):
    return kelime[-1]


def sesli_ile_bitiyor(kelime):
    return turkish_lower(kelime[-1]) in sesli_harfler


def son_sesli_harf(kelime):
    for harf in kelime[::-1]:
        if turkish_lower(harf) in sesli_harfler:
            return turkish_lower(harf)


def son_sesli_harf_kalin(kelime):
    return turkish_lower(son_sesli_harf(kelime)) in kalin_sesliler

from istisnalar import ek_istisnalar_unlu_uyumu, suffix_tuple

def ek_uret(kelime):
    # Beklenen girdi tek kelime ancak bazı durumlarda birden fazla kelime verilebilir
    kelime = kelime.split(" ")[-1]

    # Kelimede sesli harf yoksa ek oluşturulamaz, "kelime + \s + ile"
    if not any(turkish_lower(harf) in sesli_harfler for harf in kelime):
        return f"{kelime} ile"
    
    duz_kucuk_kelime = sapkasiz(turkish_lower(kelime))
    if duz_kucuk_kelime in ek_istisnalar_unlu_uyumu.keys():
        return f"{kelime}{ek_istisnalar_unlu_uyumu[duz_kucuk_kelime][0]}"


    ek = ""

    if sesli_ile_bitiyor(kelime):
        ek = ek + "y"

    ek = ek + "l"

    if son_sesli_harf_kalin(kelime):
        ek = ek + "a"
    else:
        ek = ek + "e"

    return f"{kelime}{ek}"


from test_strings import sapka_test_sentences

for input, expected in sapka_test_sentences.items():
    print(sapkasiz(input))
    assert sapkasiz(input) == expected


from test_strings import ile_test_words, istisnalar_test_words

for kelime, beklenen in ile_test_words.items():
    print(f"{kelime:<16} {beklenen:<16} --> {ek_uret(kelime):<16}")
    assert ek_uret(kelime) == beklenen

for kelime, beklenen in istisnalar_test_words.items():
    print(f"{kelime:<16} {beklenen[0]:<16} --> {ek_uret(kelime):<16}")
    assert ek_uret(kelime) == beklenen[0]

sozluk_tsv = "TDK_Sozluk-Turkish.tsv"

import csv

with open(sozluk_tsv, "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    sozluk = list(reader)
    kelimeler = [satir[0].strip() for satir in sozluk]

set_kelimeler = set(kelimeler)
print(f"Len kelimeler: {len(kelimeler)}, len set kelimeler: {len(set_kelimeler)}")

ekli_kelimeler = []

for kelime in set_kelimeler:
    try:
        print(f"{kelime:<16} --> {ek_uret(kelime):<16}")
        ekli_kelimeler.append(ek_uret(kelime))
    except Exception as e:
        print(f"{kelime:<16} --> {e}")
        exit(1)

with open("ile_ekli_kelimeler.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(ekli_kelimeler))
