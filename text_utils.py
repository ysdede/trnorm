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

turkce_kucuk_buyuk_mapping = {v: k for k, v in turkce_buyuk_kucuk_mapping.items()}

turkish_hatted = {"â": "a", "Â": "A", "î": "i", "Î": "İ", "û": "u", "Û": "U"}

def sapkasiz(kelime):
    for sapka, duz in turkish_hatted.items():
        kelime = kelime.replace(sapka, duz)

    return kelime

def turkish_upper(kelime):
    for kucuk, buyuk in turkce_kucuk_buyuk_mapping.items():
        kelime = kelime.replace(kucuk, buyuk)

    return kelime.upper()

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

def is_turkish_upper(s):
    return s == turkish_upper(s)

def turkish_capitalize(s):
    if not s:
        return s
    return turkish_upper(s[0]) + s[1:]
    