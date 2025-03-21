Görev Tanımı:
ASR (Otomatik Konuşma Tanıma) sisteminden elde edilen hipotez cümleyi ve referans cümleyi kullanarak aşağıdaki adımları uygula:

Hizalama (Alignment) Düzeltmeleri:

Hipotezdeki kelimeleri referans cümleyle karşılaştır.

Eksik veya yanlış hizalanmış kelimeleri hipotezden referans cümleye ekle/düzelt.

ASR Hatalarını Dikkate Al: Hipotezdeki hatalı kelimeleri referans cümleye ekleme.

Anlam Bütünlüğünü Koru: Cümlenin akışını ve anlamını bozma.

Dil ve Yazım Düzeltmeleri:

Referans cümledeki imla, yazım, noktalama ve Türkçe dil bilgisi hatalarını düzelt.

Stopword'leri Silme: "Yani", "hani", "tabii" gibi kelimeleri koru.

Tamamen Hatalı Etiketleri Tespit Et:

Referans ve hipotez arasında hiçbir anlamsal/kelime benzerliği yoksa, "Hatalı etiketleme" olarak işaretle.

Adım Adım Talimatlar:
A. Hizalama (Alignment) İşlemleri:
Eksik/Yanlış Kelimeleri Tamamla:

Örn: Hipotezde "community school" varsa, referansa ekle.

ASR Hatalarını Göz Ardı Et:

Örn: Hipotezde "%3" yazıyorsa, referanstaki "yüz ölçümü" ifadesini koru.

Ses Metin Uyumsuzluğunu Çöz:

Örn: Hipotezde "Buna rağmen" varsa ve referansta eksikse, ekle.

B. Hatalı Etiketleme Tespiti:
Ölçüt: Referans ve hipotez arasında hiçbir kelime veya anlam örtüşmesi yoksa (örnek: "gösteriler" vs "ihanet belgesi"), düzeltme yapma.

Örnek Senaryolar:
Senaryo 1: Alignment Düzeltme
Referans: "İşte bir kolejler var, Katolik. Bir de belediye okulları var."

Hipotez: "İşte bir kolejler var, katolik. Bir de normal belediye, community school dediğimiz belediye okulları var."

Çıktı:
"İşte bir kolejler var, Katolik. Bir de normal belediye, community school dediğimiz belediye okulları var."

Açıklama:
"community school" hipotezden eklendi; "katolik" düzeltildi.

Senaryo 2: Hatalı Etiketleme
Referans: "Birçok şehirde gösteriler düzenlendi."

Hipotez: "İhanet belgesi olduğunu söyleyerek Libra yönetimini eleştirmek."

Çıktı:
"Hatalı etiketleme: Referans ve hipotez arasında hiçbir benzerlik yok."

Sonuç Formatı:
Düzeltilmiş referans cümlesini ver. Sadece düzeltilmiş referans cümlesini döndür. Açıklama yapma!

Referans ve Hipotez arasında fark yoksa referans cümlesindeki imla, yazım, noktalama ve Türkçe dil bilgisi hatalarını düzelt. Çıktı yine girdi ile aynı "-1111-" kodunu döndür.