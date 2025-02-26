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

def ekle(kelime: str = "", ek: str = ""):
    ekler = ["ile", "ise", "iken"]

    if len(kelime) == 0:
        return ""

    if ek == "" or ek not in ekler:
        raise ValueError(f"Ek {ek} not in {ekler}")

    # Beklenen girdi tek kelime ancak bazı durumlarda birden fazla kelime verilebilir
    kelime = kelime.split(" ")[-1]

    yeni_ek = ""

    if sesli_ile_bitiyor(kelime):
        yeni_ek = yeni_ek + "y"
    
    # Hepsi büyük harf ise ve uzunluğu <= 3 ise ek oluşturulamaz
    if is_turkish_upper(kelime) and len(kelime) <= 3:
        return f"{kelime} {ek}"

    # Kelimede sesli harf yoksa ek oluşturulamaz, "kelime + \s + ile"
    if not any(turkish_lower(harf) in sesli_harfler for harf in kelime):
        return f"{kelime} {ek}"
    
    if ek == "iken":
        yeni_ek = yeni_ek + "ken"
        return f"{kelime}{yeni_ek}"

    duz_kucuk_kelime = sapkasiz(turkish_lower(kelime))

    from trnorm.istisnalar import ek_istisnalar_unlu_uyumu, suffix_tuple

    if duz_kucuk_kelime in ek_istisnalar_unlu_uyumu.keys():
        # Use index 0 for "ile" and index 1 for "ise"
        if ek == "ile":
            return f"{kelime}{ek_istisnalar_unlu_uyumu[duz_kucuk_kelime][0]}"
        else:  # ek == "ise"
            return f"{kelime}{ek_istisnalar_unlu_uyumu[duz_kucuk_kelime][1]}"

    yeni_ek = yeni_ek + ek[1]

    if son_sesli_harf_kalin(kelime):
        yeni_ek = yeni_ek + "a"
    else:
        yeni_ek = yeni_ek + "e"

    return f"{kelime}{yeni_ek}"
