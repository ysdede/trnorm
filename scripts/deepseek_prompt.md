# ASR Metin Düzeltme ve Hizalama Görevi

ASR (Otomatik Konuşma Tanıma) sisteminden elde ettiğim hipotez cümleyi ve referans cümleyi vereceğim. Referans cümlede etiketleme veya hizalama (alignment) hatalarından dolayı başta veya sonda eksik/fazla kelimeler olabilir. Ayrıca, referans cümlede imla, yazım, Türkçe dil bilgisi veya noktalama hataları bulunabilir.

## Görevin:

1. **Hizalama (Alignment) İçin Hipotezi Kullan:**
   - Hipotezdeki kelimeleri referans cümleyle karşılaştırarak, eksik veya yanlış hizalanmış kelimeleri düzelt.
   - Hipotezdeki kelimeler, referans cümlede alignment hatası nedeniyle eksik veya yanlış yerleştirilmiş olabilir. Bu durumda, hipotezdeki doğru kelimeleri referans cümleye ekle veya düzelt.
   - Hipotezdeki bir ifade referans cümlede eksikse, ancak ses etiketinde olması gereken bir ifadeyse, bu ifadeyi referans cümleye dikkatlice ekle.
   - Hipotezdeki ekstra kelimeler veya ipuçları, referans cümlede eksik olan bilgileri tamamlamak için kullanılabilir.

2. **Dikkat Edilmesi Gerekenler:**
   - Hipotez cümlede ASR'den kaynaklanan WER/CER hataları olabileceğini unutma.
   - Hipoteze aşırı güvenme ve referans cümlede gereksiz yoğun değişiklikler yapma.
   - Hipotezdeki hatalı kelimeleri referans cümleye ekleme.
   - Cümlenin anlam bütünlüğünü koru. Alignment düzeltmeleri yaparken, cümlenin anlamını bozma.

3. **Dil ve Yazım Düzeltmeleri:**
   - Referans cümledeki imla, yazım, noktalama ve Türkçe dil bilgisi hatalarını düzelt.
   - Türkçe yerelleşmeyi koru, gerekirse düzelt. Türkçe'de ondalık basamakları virgül ile ayrılır (3,14 gibi).
   - Nokta ile ayrılmış binler basamaklarını düzelt (1.000.000 → 1000000 gibi).
   - Yüzde işareti sayıdan önce gelir (%3 gibi).
   - Para birimleri sayıdan sonra gelir (100 TL, 50 $ gibi).
   - Şapkalı harfleri düzleştirme, koru (mali gelir anlamındaki "kâr" gibi).

4. **Stopword'leri Koru:**
   - "Yani", "hani", "ya", "tabii" vb. kelimeleri silme.
   - Bu kelimeler cümlenin akışını ve anlamını korumak için önemlidir.

5. **Tamamen Hatalı Etiketleri Tespit Et:**
   - Referans ve hipotez arasında hiçbir anlamsal/kelime benzerliği yoksa, "Hatalı etiketleme" olarak işaretle.

## Örnekler:

**Örnek 1:**
Referans: "İşte bir kolejler var, Katolik. Bir de belediye okulları var. Burada seçmeli din dersleri var."
Hipotez: "İşte bir kolejler var, katolik. Bir de normal belediye, community school dediğimiz belediye okulları var. Burada seçmeli din dersleri var."

Çıkış:
"İşte bir kolejler var, Katolik. Bir de normal belediye, community school dediğimiz belediye okulları var. Burada seçmeli din dersleri var."

**Örnek 2:**
Referans: "Hollanda, yüz ölçümü olarak Konya kadar bir yer."
Hipotez: "Hollanda %3 olarak Konya kadar bir yer. Buna rağmen..."

Çıkış:
"Hollanda, yüz ölçümü olarak Konya kadar bir yer. Buna rağmen..."

**Örnek 3:**
Referans: "Töre, namus cinayetlerinin."
Hipotez: "Namus cinayetlerinin."

Çıkış:
"Namus cinayetlerinin."

**Örnek 4: Hatalı Etiketleme**
Referans: "Birçok şehirde gösteriler düzenlendi."
Hipotez: "İhanet belgesi olduğunu söyleyerek Libra yönetimini eleştirmek."

Çıkış:
"Hatalı etiketleme"

## Sonuç Formatı:
Düzeltilmiş referans cümlesini ver. Sadece düzeltilmiş referans cümlesini döndür. Açıklama yapma!
Referans ve Hipotez arasında fark yok ise: referans cümlesindeki imla, yazım, noktalama ve Türkçe dil bilgisi hatalarını düzelt.