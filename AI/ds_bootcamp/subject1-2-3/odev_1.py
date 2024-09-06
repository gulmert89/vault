ilk_deger = 1000
faiz = 0.12
f_deger = ilk_deger*((1+faiz)**7)    # faizli değer

print(f"""
Hafta başında {ilk_deger} dolarlık bitcoin aldığımızda günde ortalama %{int(faiz*100)} kazançla,
bir hafta sonunda {f_deger:.2f} dolar kazanırdık.
""")    # "f-strings" kullanıldı. (Python 3.6+)

dosya_adi = input("Dosyayı hangi isimle kaydetmek istersiniz? ")
print("Dosya ismi: " + dosya_adi + ".py")
