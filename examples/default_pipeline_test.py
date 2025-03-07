"""
Test the default pipeline in the normalize function.

This script demonstrates how to use the normalize function with the default pipeline.
"""

from trnorm import normalize

# Test cases for the default pipeline
test_cases = [
    "Turner'ın 'Köle Gemisi' isimli tablosuna bakıyoruz.",
    "Odanın boyutları 2x3x4 metre.",
    "Halının boyutu 120x180cm.",
    "Ağırlığı 5 kg. ve uzunluğu 10 metre.",
    "Sıcaklık 25 °C ve nem %60.",
    "Saat 14:30'da %25 indirimli ürünler satışa çıkacak.",
    "Ürün fiyatı 1.250,75 TL'dir.",
    "1. sınıfta 23 öğrenci var.",
    "Dün 3x4 metre halı aldım.",
    "II. Wilhelm, Almanya imparatoruydu.",
    "V. Karl, Kutsal Roma İmparatoru'ydu.",
    "1'inci sınıf 1inci kat",
    "2. Mahmud ya da II. Mahmud.",
    "1.000 ₺",
    "$500",
    "600 $",
    "kâğıt ve kalem",
    "Âdem ile Havva",
    "îmanın kimde",
    "Îman büyük harfle şapkalı",
    "hûr ne",
    "Yavru ile kâtip",
    "Python 2.7 - 2.4 ASA - Pi sayısı 3.14",
    "Bu kitap 1990'ların en iyi eserleri arasında.",
    "Toros ile hamile",
    "Hayat sana limon verdi ise limonata yap",
    "Hâl böyle iken böyle dedi adam.",
    # Alphanumeric test cases
    "Kısa vadeli kredilerin notu ise F3.",
    "B1 olan döviz kuru notu ise değişmedi.",
    "F16 savaş uçakları tatbikata katıldı.",
    "A400M nakliye uçağı Türk Hava Kuvvetleri'ne teslim edildi."
]

print("=" * 80)
print("DEFAULT PIPELINE TEST")
print("=" * 80)
print("\nTesting the normalize function with the default pipeline:")
print("-" * 60)

for i, text in enumerate(test_cases, 1):
    normalized = normalize(text)
    print(f"{i}. Original: {text}")
    print(f"   Normalized: {normalized}")
    print()

print("=" * 80)
print("Test completed!")
print("=" * 80)
