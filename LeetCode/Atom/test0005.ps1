# 保存为 .ps1 文件，例如 Set-DocumentTitle.ps1
$folderPath = "D:\BaiduNetdiskDownload\Movies\日剧\行骗天下JP"  # 替换为实际路径
$exePath = "C:\Program Files\MKVToolNix\mkvpropedit.exe"  # 替换为 mkvpropedit.exe 的实际路径
$files = Get-ChildItem -Path $folderPath -Include *.mp4, *.mkv -Recurse

foreach ($file in $files) {
    $filenameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    
    if ($file.Extension -eq ".mkv") {
        & "$exePath" --set "title=$filenameWithoutExt" $file.FullName
    }
    else {
        # 对于 mp4 文件，可以使用 ffmpeg 来修改标题
        & "C:\Users\yongk\Downloads\exiftool-13.55_64\exiftool.exe" -Title="$filenameWithoutExt" -Overwrite_Original $file.FullName
    }
}
