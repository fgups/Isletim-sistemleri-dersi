class FileSystemNode:
    def __init__(self, isim, parent=None):
        self.isim = isim
        self.parent = parent

class Dosya(FileSystemNode):
    def __init__(self, isim, parent=None):
        super().__init__(isim, parent)

class Dizin(FileSystemNode):
    def __init__(self, isim, parent=None):
        super().__init__(isim, parent)
        self.cocuklar = {}

class DosyaSistemiSim:
    def __init__(self):
        self.kok = Dizin("/")
        self.mevcut_dizin = self.kok

    def calistir(self):
        print("--- Python Dosya Sistemi Simülatörü (Sade Versiyon) ---")
        print("Aşağıdaki komutları kullanarak sistemi yönetebilirsiniz:")
        print("\n--- Komut Listesi ---")
        print("  ls           -> Mevcut dizin içeriğini listeler")
        print("  mkdir <isim> -> Yeni bir dizin (klasör) oluşturur")
        print("  touch <isim> -> Yeni, boş bir dosya oluşturur")
        print("  cd <isim>    -> 'isim' adlı dizine gider (örn: cd belgeler, cd ..)")
        print("  rm <isim>    -> 'isim' adlı dosyayı veya dizini siler")
        print("  mv <eski> <yeni> -> Dosya/dizinin adını 'eski'den 'yeni'ye değiştirir")
        print("  exit         -> Simülatörden çıkış yapar")
        print("---------------------------------------------------------\n")

        while True:
            yol = []
            current = self.mevcut_dizin
            while current.parent:
                yol.append(current.isim)
                current = current.parent
            prompt_yol = "/" + "/".join(reversed(yol))
            prompt = f"[{prompt_yol.replace('//','/')}] > "

            try:
                komut_satiri = input(prompt).strip()
                if not komut_satiri:
                    continue
                
                parcalar = komut_satiri.split()
                komut_adi = parcalar[0]
                args = parcalar[1:]

                if komut_adi == "exit":
                    print("Çıkış yapılıyor...")
                    break
                elif komut_adi == "ls":
                    self.ls(args)
                elif komut_adi == "mkdir":
                    self.mkdir(args)
                elif komut_adi == "touch":
                    self.touch(args)
                elif komut_adi == "cd":
                    self.cd(args)
                elif komut_adi == "rm":
                    self.rm(args)
                elif komut_adi == "mv":
                    self.mv(args)
                else:
                    print(f"Hata: '{komut_adi}' tanınmayan bir komut.")
            except Exception as e:
                print(f"Bir hata oluştu: {e}")

    def ls(self, args):
        if not self.mevcut_dizin.cocuklar:
            return
        
        for isim, node in sorted(self.mevcut_dizin.cocuklar.items()):
            isim_str = isim + "/" if isinstance(node, Dizin) else isim
            print(isim_str, end="   ")
        print()

    def mkdir(self, args):
        if not args:
            print("Hata: mkdir: eksik argüman.")
            return
        isim = args[0]
        if isim in self.mevcut_dizin.cocuklar:
            print(f"Hata: '{isim}' zaten var.")
        else:
            yeni_dizin = Dizin(isim, parent=self.mevcut_dizin)
            self.mevcut_dizin.cocuklar[isim] = yeni_dizin

    def touch(self, args):
        if not args:
            print("Hata: touch: eksik argüman.")
            return
        isim = args[0]
        if isim not in self.mevcut_dizin.cocuklar:
            yeni_dosya = Dosya(isim, parent=self.mevcut_dizin)
            self.mevcut_dizin.cocuklar[isim] = yeni_dosya

    def cd(self, args):
        if not args:
            print("Hata: cd: eksik argüman.")
            return
        
        isim = args[0]
        
        if isim == "..":
            if self.mevcut_dizin.parent:
                self.mevcut_dizin = self.mevcut_dizin.parent
        elif isim == "/":
            self.mevcut_dizin = self.kok
        elif isim in self.mevcut_dizin.cocuklar and isinstance(self.mevcut_dizin.cocuklar[isim], Dizin):
            self.mevcut_dizin = self.mevcut_dizin.cocuklar[isim]
        else:
            print(f"Hata: cd: '{isim}' dizini bulunamadı.")

    def rm(self, args):
        if not args:
            print("Hata: rm: eksik argüman.")
            return
        isim = args[0]
        if isim not in self.mevcut_dizin.cocuklar:
            print(f"Hata: rm: '{isim}' bulunamadı.")
        else:
            del self.mevcut_dizin.cocuklar[isim]
            print(f"'{isim}' silindi.")
    
    def mv(self, args):
        if len(args) != 2:
            print("Hata: mv: kullanımı: mv <eski_isim> <yeni_isim>")
            return
        
        eski_isim, yeni_isim = args[0], args[1]
        
        if eski_isim not in self.mevcut_dizin.cocuklar:
            print(f"Hata: mv: '{eski_isim}' bulunamadı.")
            return
        
        if yeni_isim in self.mevcut_dizin.cocuklar:
            print(f"Hata: mv: '{yeni_isim}' zaten var.")
            return
            
        node = self.mevcut_dizin.cocuklar.pop(eski_isim)
        node.isim = yeni_isim
        self.mevcut_dizin.cocuklar[yeni_isim] = node
        print(f"'{eski_isim}' -> '{yeni_isim}' olarak adlandırıldı.")

if __name__ == "__main__":
    sim = DosyaSistemiSim()
    sim.calistir()