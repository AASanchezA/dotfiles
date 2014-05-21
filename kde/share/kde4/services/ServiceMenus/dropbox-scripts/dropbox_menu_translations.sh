#Translations for notifications/kdialogs
#If you want to translate this, then copy&paste load_language_en function and change en to your language code

load_language_en () {
	publicurl_error="You can generate public URL only for files and directories that are in your Dropbox Public folder."
	revisions_error="You can only view previous versions of files that are in your Dropbox folder."
	share_error="You can only share directories that are in your Dropbox folder."
	encrypt_dropbox_error="You can encrypt folder listing only for directories that are in your Dropbox Public folder."
	link_available="Public URL is now available in Klipper."
	encrypt_finish=`echo -e "Folder listing for folder &quot;"${fileurl##*/}"&quot; encrypted."`
	url_error="You can generate public URL only for files and directories that are in your Dropbox folder."
	dependency_error="It looks like you are missing one of the dependencies of this servicemenu. Make sure that sqlite3, python, kdialog and klipper are installed."
#Kdialogs
	mailurl_subject="Dropbox Public URL"
	file_exists_text=`echo "File or directory "$dropbox_path"/Public/"${fileurl##*/}" exists. Do you want to overwrite it?"`
	encrypt_password="Enter password:"
	encrypt_rePassword="Re-enter password:"
	encrypt_match_error="The passwords you entered do not match. Please enter them again."
}

load_language_de () {
	publicurl_error="Nur Dateien in Ihrem öffentlichen Dropbox-Verzeichnis haben eine öffentliche URL."
	revisions_error="Sie können nur für Dateien in Ihrem öffentlichen Dropbox-Verzeichnis ältere Versionen betrachten."
	share_error="Sie können nur Verzeichnisse in Ihrem Dropbox-Verzeichnis freigeben."
	encrypt_dropbox_error="Sie können nur Dateilisten in Ihrem öffentlichen Dropbox-Verzeichnis verschlüsseln."
	link_available="Öffentliche URL ist jetzt in der Zwischenablage."
	encrypt_finish=`echo -e "Dateiliste für Verzeichnis &quot;"${fileurl##*/}"&quot; verschlüsselt."`
	url_error="Sie können nur für Verzeichnisse und Dateien in Ihrem Dropbox-Verzeichnis eine öffentliche URL generieren."
	dependency_error="Anscheinend sind nicht alle Abhängigkeiten für dieses Servicemenü installiert. Bitte stellen Sie sicher, dass sqlite3, python, kdialog und klipper installiert sind."

#Kdialogs
	mailurl_subject="Dropbox URL"
	file_exists_text=`echo "Datei oder Ordner "$dropbox_path"/Public/"${fileurl##*/}" existiert bereits. Wollen Sie das Ziel überschreiben?"`
	encrypt_password="Passwort eingeben:"
	encrypt_rePassword="Passwort erneut eingeben:"
	encrypt_match_error="Passwörter stimmen nicht überein. Bitte nochmals eingeben."
}

load_language_pl () {
	publicurl_error="Możesz utworzyć publiczny adres URL tylko dla plików i katalogów znajdujących się w folderze publicznym Dropboxa."
	revisions_error="Możesz przeglądać wcześniejsze wersje tylko plików znajdujących się w folderze Dropboxa."
	share_error="Możesz udostępniać tylko foldery znajdujące się w folderze Dropboxa."
	encrypt_dropbox_error="Możesz zaszyfrować listę plików tylko dla katalogów znajdujacych się w folderze publicznym Dropboxa."
	link_available="Publiczny adres URL został skopiowany do schowka."
	encrypt_finish=`echo -e "Lista plików w katalogu &quot;"${fileurl##*/}"&quot; została zaszyfrowana."`
	url_error="Możesz utworzyć publiczny adres URL tylko dla plików i katalogów znajdujących się w folderze Dropboxa."
	dependency_error="Wygląda na to, że nie masz zainstalowanych wszystkich zależności wymaganych przez to menu. Upewnij się, że pakiety sqlite3, python, kdialog i klipper są zainstalowane."
#Kdialogs
	mailurl_subject="Dropbox - publiczny adres URL."
	file_exists_text=`echo "Plik lub folder "$dropbox_path"/Public/"${fileurl##*/}" istnieje. Czy chcesz go nadpisać?"`
	encrypt_password="Podaj hasło:"
	encrypt_rePassword="Podaj hasło ponownie:"
	encrypt_match_error="Podane hasła nie są takie same. Proszę, wprowadź je ponownie."
}

load_language_es () {
	publicurl_error="Puede generar direcciones URL públicas sólo para archivos y directorios en su carpeta pública de Dropbox."
	revisions_error="Sólo puede ver las versiones anteriores de un fichero en su carpeta de Dropbox."
	share_error="Sólo puede compartir directorios en su carpeta Dropbox."
	encrypt_dropbox_error="Sólo puede cifrar el listado de carpetas en los directorios dentro de su carpeta Dropbox."
	link_available="La URL pública ya está disponible en Klipper."
	encrypt_finish=`echo -e "Se ha cifrado el listado de carpetas para la carpeta &quot;"${fileurl##*/}"&quot;."`
	url_error="La generación de URLs públicas es solamente para archivos y carpetas dentro de la carpeta de DropBox."
	#dependency_error=
#Kdialogs
	mailurl_subject="Dirección URL pública de Dropbox"
	file_exists_text=`echo "El fichero o directorio "$dropbox_path"/Public/"${fileurl##*/}" ya existe. ¿Desea sobreescribirlo?"`
	encrypt_password="Introduzca la contraseña:"
	encrypt_rePassword="Introduzca la contraseña otra vez:"
	encrypt_match_error="Las contraseñas introducidas no coinciden.	Introdúzcalas otras vez."
}

load_language_it () {
	publicurl_error="Puoi generare indirizzi pubblici (URL) solo per file e cartelle che sono nella tua Cartella Pubblica di DropBox."
	revisions_error="Puoi vedere solo le versioni precedenti dei file che sono nella cartella di Dropbox."
	share_error="Puoi condividere solo cartelle che sono nella tua cartella di DropBox."
	encrypt_dropbox_error="Puoi criptare la cartella attiva solo per le cartelle che sono nella Cartella Pubblica di DropBox."
	link_available="L'Indirizzo Pubblico (URL) è ora disponibile in Klipper."
	encrypt_finish=`echo -e "La Cartella in ascolto per la cartella &quot;"${fileurl##*/}"&quot; è criptata."`
	url_error="Puoi generare URL Pubblici solo per file e cartelle che sono nella tua cartella Dropbox."
	#dependency_error=
#Kdialogs
	mailurl_subject="Indirizzo Pubblico (URL) Dropbox"
	file_exists_text=`echo "File o cartella "$dropbox_path"/Public/"${fileurl##*/}" gia' esistente. Vuoi sovrascriverlo?"`
	encrypt_password="Inserisci la password:"
	encrypt_rePassword="Inserisci nuovamente la password:"
	encrypt_match_error="La password inserita non combacia. Si prega di inserirla nuovamente"
}

load_language_cs () {
	publicurl_error="Veřejnou adresu (URL) můžete vytvořit pouze pro soubory a adresáře, které jsou ve vaší veřejné dropboxové složce."
	revisions_error="Můžete se podívat pouze na ty předchozí verze souborů, které jsou ve vaší veřejné dropboxové složce."
	share_error="Můžete sdílet pouze ty adresáře, které jsou ve vaší dropboxové složce."
	encrypt_dropbox_error="Můžete zašifrovat seznam souborů pouze u těch adresářů, které jsou ve vaší veřejné dropboxové složce."
	link_available="Veřejná adresa (URL) je nyní dostupná v Klipperu."
	encrypt_finish=`echo -e "Seznam souborů ve složce &quot;"${fileurl##*/}"&quot; zašifrován."`
	url_error="Veřejnou adresu (URL) můžete vytvořit pouze pro ty soubory a adresáře, které jsou ve vaší dropboxové složce."
	#dependency_error=
#Kdialogs
	mailurl_subject="Veřejná dropboxová adresa (URL)"
	file_exists_text=`echo "Soubor nebo adresář "$dropbox_path"/Public/"${fileurl##*/}" existuje. Chcete jej přepsat?"`
	encrypt_password="Zadejte heslo:"
	encrypt_rePassword="Zadejte heslo znovu:"
	encrypt_match_error="Hesla, která jste zadal, se neshodují. zadejte je, prosím, znovu."
}


load_language_fr () {
    publicurl_error="Vous pouvez générer une URL publique seulement pour les fichiers et dossiers du répertoire public de Dropbox."
    revisions_error="Vous pouvez voir les versions précédentes seulement pour les fichiers de votre répertoire Dropbox."
    share_error="Vous ne pouvez partager que les dossiers de votre répertoire Dropbox."
    encrypt_dropbox_error="Vous pouvez crypter seulement la liste du contenu des dossiers dans votre répertoire public de Dropbox."
    link_available="L'URL publique est disponible dans Klipper."
    encrypt_finish=`echo -e "La liste du contenu du dossier &quot;"${fileurl##*/}"&quot; a bien été cryptée."`
    url_error="Vous pouvez générer une URL publique seulement pour les fichiers et dossiers dans votre répertoire Dropbox."
    #dependency_error=
#Kdialogs
    mailurl_subject="URL publique Dropbox"
    file_exists_text=`echo "Le fichier ou le dossier "$dropbox_path"/Public/"${fileurl##*/}" existe déjà.\nVoulez-vous l'écraser?"`
    encrypt_password="Entrez le mot de passe:"
    encrypt_rePassword="Ré-entrez le mot de passe:"
    encrypt_match_error="Les mots de passe que vous avez entrés sont différents.\nRecommencez l'opération."
}


load_language_zh_TW () {
	publicurl_error="您只能夠針對您 Dropbox Public 資料夾中的 檔案和目錄產生公開的 URL。"
	revisions_error="您只能檢視在您 Dropbox 資料夾中檔案的較早版本。"
	share_error="您只能分享在您 Dropbox 資料夾中的目錄。"
	encrypt_dropbox_error="您只能夠針對您 Dropbox Public 資料夾中的目錄進行 資料夾清單的加密。"
	link_available="公開的 URL 現在已在您的 Klipper 剪貼簿中。"
	encrypt_finish=`echo -e "資料夾 &quot;"${fileurl##*/}"&quot; 的資料夾清單已加密。"`
	url_error="您只能夠針對您 Dropbox 資料夾中的檔案和 目錄產生公開的 URL。"
	#dependency_error=
#Kdialogs
	mailurl_subject="Dropbox 公開的 URL"
	file_exists_text=`echo "檔案或目錄 "$dropbox_path"/Public/"${fileurl##*/}" 已存在，您想要覆蓋過它嗎？"`
	encrypt_password="輸入密碼:"
	encrypt_rePassword="再次輸入密碼:"
	encrypt_match_error="您輸入的密碼不符，請再重新輸入一次。"
}

load_language_lt () {
	publicurl_error="Viešuosius URL galima generuoti tik failams ir aplankams, esantiems viešajame Dropbox aplanke „Public“."
	revisions_error="Ankstesnes failų versijas galite pamatyti tik tuo atveju, jei jie yra Dropbox aplanke."
	share_error="Dalintis galite tik tomis direktorijomis, kurios yra Dropbox aplanke."
	encrypt_dropbox_error="Aplanko turinio sąrašą galite užšifruoti tik tuo atveju, jei jis yra viešajame Dropbox aplanke „Public“."
	link_available="Viešasis URL dabar yra Iškarpinėje."
	encrypt_finish=`echo -e "Aplanko „"${fileurl##*/}"“ turinio sąrašas dabar yra užšifruotas."`
	url_error="Viešuosius URL galite generuoti tik tiems failams ar aplankams, kurie yra Dropbox aplanke."
	#dependency_error=
#Kdialogs
	mailurl_subject="Dropbox viešasis URL"
	file_exists_text=`echo "Failas arba aplankas "$dropbox_path"/Public/"${fileurl##*/}" jau yra. Ar norite jį perrašyti?"`
	encrypt_password="Įveskite slaptažodį:"
	encrypt_rePassword="Įveskite slaptažodį iš naujo:"
	encrypt_match_error="Jūsų įrašyti slaptažodžiai neatitinka. Prašome įrašyti juos iš naujo."
}

load_language_ru () {
        publicurl_error="Вы можете создать URL только для тех файлов и папок, которые расположены в директории Dropbox Public."
        revisions_error="Вы можете просматривать предыдущие версии только тех файлов, которые расположены в директории Dropbox."
        share_error="Вы можете делать общими только те директории, которые находятся в директории Dropbox."
        encrypt_dropbox_error="Вы можете шифровать список файлов в только для директорий, расположенных в каталоге Dropbox Public."
        link_available="Общедоступный URL доступен в Klipper."
        encrypt_finish=`echo -e "Список файлов для директории &quot;"${fileurl##*/}"&quot; зашифрован."`
        url_error="Вы можете создать общедоступный URL только для файлов и папок, расположенных в директории Dropbox."
        #dependency_error=
#Kdialogs
        mailurl_subject="Dropbox Public URL"
        file_exists_text=`echo "Файл или директория "$dropbox_path"/Public/"${fileurl##*/}" уже существует. Вы хотите его переписать?"`
        encrypt_password="Введите пароль:"
        encrypt_rePassword="Повторите ввод пароля:"
        encrypt_match_error="Пароли не совпадают. Пожалуйста, введите их повторно."
}

load_language_pt () {
	publicurl_error="Só pode gerar URL públicos para os ficheiros e directorias que estão na pasta pública do Dropbox"
	revisions_error="Só pode ver versões anteriores dos ficheiros que estão na pasta Dropbox."
	share_error="Só pode partilhar directorias que estão na pasta Dropbox."
	encrypt_dropbox_error="Pode cifrar a listagem de pastas apenas para directorias que estão dentro da pasta pública do Dropbox."
	link_available="O URL público está agora disponível no Klipper."
	encrypt_finish=`echo -e "Listagem de pastas para a pasta &quot;"${fileurl##*/}"&quot; cifrada."`
	url_error="Pode gerar URLs públicos apenas para ficheiros e directorias que estão na sua pasta Dropbox."
	dependency_error="Parece que está a faltar uma das depedências deste menu de serviços. Certifique-se que as dependências sqlite3, python, kdialog e klipper estão instaladas."
#Kdialogs
	mailurl_subject="URL Pública do Dropbox"
	file_exists_text=`echo "Ficheiro ou directoria "$dropbox_path"/Public/"${fileurl##*/}" existe. Quer substituí-la?"`
	encrypt_password="Insira a palavra-passe:"
	encrypt_rePassword="Reinsira palavra-passe:"
	encrypt_match_error="As palavras-passe que inseriu não estão de acordo. Por favor, insira-as novamente."
}

load_language_hu () {
	publicurl_error="Publikus URL-t csak a DropBox könyvtáron belül lévő fájlokhoz és könyvtárakhoz hozhatsz létre."
	revisions_error="You can only view previous versions of files that are in your Dropbox folder."
	share_error="Csak olyan könyvtárakat oszthatsz meg, amelyek a DropBox könyvtáradon belül van."
	encrypt_dropbox_error="Titkosított könyvtárat csak a DropBox könyvtáradon belül hozhatsz létre."
	link_available="Publikus URL most már elérhető Klipper-ben."
	encrypt_finish=`echo -e "Könyvtár &quot;"${fileurl##*/}"&quot; titkosított."`
	url_error="Publikus URL-t csak a DropBox könyvtáron belül lévő fájlokhoz és könyvtárakhoz hozhatsz létre."
	dependency_error="Úgy tűnik hiányzik pár programok, könyvtár a servicemenu telepítéséhez  Szükséges programok: sqlite3, python, kdialog, klipper"
#Kdialogs
	mailurl_subject="Dropbox Publikus URL"
	file_exists_text=`echo "Fájl vagy könyvtár "$dropbox_path"/Public/"${fileurl##*/}" létezik. Felülírja?"`
	encrypt_password="Jelszó:"
	encrypt_rePassword="Jelszó megerősítése:"
	encrypt_match_error="A megadott jelszó hibás. Kérem próbálja újra!"
}

load_language_nl () {
	publicurl_error="Publieke URLs kunt u enkel verkrijgen voor bestanden en mappen in de Public-map van Dropbox."
	revisions_error="Het bekijken van vorige versies van bestanden is enkel mogelijk voor bestanden in uw Dropbox-map."
	share_error="U kunt enkel mappen delen die in uw Dropbox-map aanwezig zijn."
	encrypt_dropbox_error="U kunt de oplijsting van de mapinhoud enkel versleutelen voor mappen die in uw Dropbox-map zitten."
	link_available="Publieke URL is nu beschikbaar in Klipper."
	encrypt_finish=`echo -e "Oplijsting mapinhoud van map &quot;"${fileurl##*/}"&quot; versleuteld."`
	url_error="Het maken van een publieke URL is enkel mogelijk voor mappen en bestanden in uw Dropbox map."
	dependency_error="Blijkbaar is er een afhankelijkheid niet aanwezig voor dit servicemenu. Controleer of sqlite3, python, kdialog en klipper geïnstalleerd zijn."
#Kdialogs
	mailurl_subject="Publieke URL Dropbox"
	file_exists_text=`echo "Bestand of map "$dropbox_path"/Public/"${fileurl##*/}" bestaat reeds. Overschrijven?"`
	encrypt_password="Paswoord invoeren:"
	encrypt_rePassword="Paswoord opnieuw invoeren:"
	encrypt_match_error="De ingevoerde paswoorden komen niet overeen. Voer ze opnieuw in."
}

load_language_da () {
	publicurl_error="Du kan kun lave offentlige URL for filer og mapper der er i din Public mappe in din Dropbox mappe."
	revisions_error="Du kan kun vise tidligere versioner for filer der er i din Dropbox mappe."
	share_error="Du kan kun dele mapper der er i din DropBox mappe."
	encrypt_dropbox_error="Du kan kun krytere mapper der er i din Dropbox Public mappe."
	link_available="Offentlig URL er nu tilgængelig i Klipper."
	encrypt_finish=`echo -e "Datalister for mappen &quot;"${fileurl##*/}"&quot; er krypteret."`
	url_error="Du kan kun lave offentlige URLs for filer eller mapper der er i din Dropbox mappe."
	dependency_error="Det ligner at du mangler en afhængighed der kræves af denne servicemenu. Sikre dig at du har sqlite3, python, kdialog og klipper installeret."
#Kdialogs
	mailurl_subject="Dropbox Offentlig URL"
	file_exists_text=`echo "Fil eller mappe "$dropbox_path"/Public/"${fileurl##*/}" findes. Vil du overskrive den?"`
	encrypt_password="Indtast kodeord:"
	encrypt_rePassword="Bekræft kodeord:"
	encrypt_match_error="Kodeorderne du indtastede stemte ikke overens. Prøv venligst igen."
}