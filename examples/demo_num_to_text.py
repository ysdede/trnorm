"""
Demo script for num_to_text.py functionality.
This script demonstrates Turkish number-to-text conversion capabilities.
"""

from trnorm.num_to_text import convert_numbers_to_words_wrapper
from trnorm.ordinals import normalize_ordinals


def print_section(title):
    """Print a section title with decorative lines."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def demo_number_conversion():
    """Demonstrate number to text conversion with various examples."""
    print_section("Number to Text Conversion")
    
    examples = [
        "Savaş boyunca 66 İspanyol ticaret gemisi, Alman U-botları tarafından batırılırken 100'den fazla",
        "Osmanlı arşivlerine göre, 1864-1879 yılları arasında yaklaşık 1,5 milyon Çerkes, Osmanlı topraklarına",
        "Yani bu da demek oluyor ki 250 bin lira içerdeyiz.",
        "ve bu birliğe moral sağlamak için III. Aleksios şahsen bu kulenin",
        "ve bu birliğe moral sağlamak için 3. Aleksios şahsen bu kulenin",
        "Enstitü yaklaşık 7 bin kemikten veri topladı.",
        "Enstitü yaklaşık 7000 kemikten veri topladı.",
        "II. Dünya Savaşı sonrası ABD, lojistik ihtiyacının farkına varmış ve 1960'lı yıllarda",
        "2. Dünya Savaşı sonrası ABD, lojistik ihtiyacının farkına varmış ve 1960'lı yıllarda",
        "Bu olaydan 2 gün sonra",
        "Bu olaydan iki gün sonra",
        "Kuasarlar 10 milyar yıl boyunca beslenebilirler",
        "1/2 kalitede",
        "Hayvancılık kuzu yapar. İşte yaptıktan 2 ay sonra, kuzularımız 2 aya kadar içer sütünü annesinin. 2-2,5 aya kadar içer.",
        "Yardım, 1. gün yoktu, 2. gün de yoktu.",
        "Yardım birinci gün yoktu, ikinci gün de yoktu.",
        "13, 14 ve 15 Eylül günleri, Stalingrad için çok zor günlerdi.",
        "Ateşi otuz beş derece, ph değeri yedi nokta yirmi sekiz.",
        "Ateşi 35 derece, pH değeri 7.28.",
        "Çünkü Amerika'daki çoğu okul 6,5-7 puan istiyor IELTS'den ve ben 6 puana sahiptim.",
        "Sultan III. Selim, ülkenin her bir yanından Mısır'a takviye kuvvet gönderilmesini emretti.",
        "Marie de France'ın 12. yüzyılda yazdığı"
    ]
    
    print("Original Text".ljust(60) + "Converted Text")
    print("-" * 120)
    
    for example in examples:
        converted = convert_numbers_to_words_wrapper(example)
        print(f"{example[:57] + '...' if len(example) > 57 else example.ljust(60)}{converted}")


def demo_ordinal_conversion():
    """Demonstrate ordinal number conversion."""
    print_section("Ordinal Number Conversion")
    
    examples = [
        "Bu olaydan 2 gün sonra",
        "Yardım, 1. gün yoktu, 2. gün de yoktu.",
        "II. Dünya Savaşı sonrası ABD, lojistik ihtiyacının farkına varmış",
        "2. Dünya Savaşı sonrası ABD, lojistik ihtiyacının farkına varmış",
        "Sultan III. Selim, ülkenin her bir yanından Mısır'a takviye kuvvet gönderilmesini emretti.",
        "Marie de France'ın 12. yüzyılda yazdığı",
        "1960'lı yıllarda 3. Dünya ülkelerine yardım programları başlatıldı.",
        "XX. yüzyılın en önemli buluşlarından biri internettir.",
        "Toplantı 3. katta, 2. odada yapılacak."
    ]
    
    print("Original Text".ljust(60) + "Converted Text")
    print("-" * 120)
    
    for example in examples:
        converted = normalize_ordinals(example)
        print(f"{example[:57] + '...' if len(example) > 57 else example.ljust(60)}{converted}")


def demo_combined_conversion():
    """Demonstrate combined number and ordinal conversion."""
    print_section("Combined Number and Ordinal Conversion")
    
    examples = [
        "Yardım, 1. gün yoktu, 2. gün de yoktu.",
        "II. Dünya Savaşı sonrası ABD, lojistik ihtiyacının farkına varmış ve 1960'lı yıllarda",
        "2. Dünya Savaşı sonrası ABD, lojistik ihtiyacının farkına varmış ve 1960'lı yıllarda",
        "Hayvancılık kuzu yapar. İşte yaptıktan 2 ay sonra, kuzularımız 2 aya kadar içer sütünü annesinin. 2-2,5 aya kadar içer.",
        "Ateşi 35 derece, pH değeri 7.28.",
        "Sultan III. Selim, ülkenin her bir yanından Mısır'a takviye kuvvet gönderilmesini emretti.",
        "Ancak 67'nin son günlerinde trafiğin yoğun olduğu bir saatte üstündeki 100'lerce araçla birlikte çöktü. "
    ]
    
    print("Original Text".ljust(60) + "Converted Text")
    print("-" * 120)
    
    for example in examples:
        # First normalize ordinals, then convert remaining numbers to text
        converted = normalize_ordinals(example)
        converted = convert_numbers_to_words_wrapper(converted)
        print(f"{example[:57] + '...' if len(example) > 57 else example.ljust(60)}{converted}")


def main():
    """Run all demos."""
    print("TURKISH NUMBER NORMALIZATION DEMO")
    demo_number_conversion()
    demo_ordinal_conversion()
    demo_combined_conversion()


if __name__ == "__main__":
    main()
