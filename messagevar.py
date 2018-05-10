# Contact Variable
adminEmail = "dimas.rizky.hp@gmail.com"
hotdropGithub = "github.com/"

# Error Code
_22 = "Exception pada saat register"
_23 = "Exception pada saat cek sudah register atau belum"
_24 = "Exception pada saat menambahkan sensor"

# Text Message Reply
chatRoomFailed = "Silahkan chat melalui private room."
regSuccess = "Registrasi berhasil, " \
                "token anda : {} Harap " \
                "disimpan dengan aman. "\
                "Token digunakan untuk "\
                "autentikasi pada sensor "\
                "OWASP Securetea."
addSensorSuccess = "Penambahan sensor {} berhasil !"
illegalCharSensor = "Penamaan sensor hanya boleh menggunakan " \
                        "alphanumeric [A-Z | a-z | 0-9], underscore(_) " \
                        "dan dash(-)."
alreadyRegistered = "Kamu sudah melakukan registrasi, " \
                        "lanjutkan dengan menambahkan sensor " \
                        "atau melihat daftar sensor kamu " \
                        "reply /help untuk melihat daftar command."
unregisteredMsg = "Kamu belum melakukan registrasi, " \
                "lakukan registrasi terlebih dahulu " \
                "dengan reply /register. "
exceptionMsg = "Terjadi kesalahan error={}, hubungi admin di {}, " \
                "Sertakan error code yang terjadi"
helpMsg = "List of command \n" \
            "/help : Untuk menampilkan " \
            "menu ini.\n" \
            "/register : Untuk melakukan " \
            "registrasi dan mendapatkan token. \n" \
            "/addsensor [nama sensor] : Untuk " \
            "melakukan penambahan sensor. Argumen " \
            "nama sensor yang diberikan dibutuhkan " \
            "dalam penambahan sensor. Penamaan sensor " \
            "hanya menggunakan karakter alphanumeric.\n" \
            "/about : Menampilkan sekilas tentang bot ini."
aboutMsg = "OWASP HotDrop adalah notification gateway " \
            "melalui line dari sensor OWASP SecureTea project " \
            "Untuk ikut berkontribusi terhadap pengembangan " \
            "kunjungi github : {} ."