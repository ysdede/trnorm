# pip3 install transformers
# python3 deepseek_tokenizer.py
import transformers

chat_tokenizer_dir = "./"

tokenizer = transformers.AutoTokenizer.from_pretrained( 
        chat_tokenizer_dir, trust_remote_code=True
        )

result = tokenizer.encode("7c2f1501d857c1de2667120b2545607c9acdcf19a229cff8cb5a4fe956e7954d: Programımdaki konuları işliyorum ama bu, birilerinin işlerine gelmediği zaman beni aşağıya vuruyorlar. Annene giriyor, babana giriyor, nihayetinde ben tek başıma değilim, annem kaç yaşında bir kadın niye muhatap olsun bu insanlarla? Niye üzülsün?")
print(result, "\n" , len(result))
