$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

# Files are recognized by SHA-256, not by name, so copies from older zips land in the new layout too.
$self = $env:ORG_SELF
$root = [IO.Path]::GetDirectoryName($self)
$trashName = '_قديم أو مكرر - راجعه وامسحه'
$trash = [IO.Path]::Combine($root, $trashName)

function LP([string]$p) { if ($p.StartsWith('\\?\')) { return $p }; return '\\?\' + $p }
function Parent([string]$p) { return [IO.Path]::GetDirectoryName($p) }
function Rel([string]$p) { return $p.Substring($root.Length).TrimStart('\') }

$text = [IO.File]::ReadAllText($self, [Text.Encoding]::UTF8)
$data = $text.Substring($text.IndexOf('#DA' + 'TA') + 5)
$manifest = New-Object System.Collections.Generic.List[object]
$want = @{}
$obsolete = @{}
$embed = @{}
$sizes = New-Object 'System.Collections.Generic.HashSet[long]'
foreach ($line in $data -split "`r?`n") {
    if (-not $line) { continue }
    $p = $line.Split("`t")
    switch ($p[0]) {
        'M' { $manifest.Add([pscustomobject]@{ Hash = $p[1]; Rel = $p[3] }); $want[$p[1]] = $true; [void]$sizes.Add([long]$p[2]) }
        'O' { $obsolete[$p[1]] = $true; [void]$sizes.Add([long]$p[2]) }
        'E' { $embed[$p[1]] = $p[2] }
    }
}

Write-Host ''
Write-Host "  الفولدر: $root"
Write-Host "  هرتب $($manifest.Count) ملف. مش همسح أي حاجة: المكرر والقديم هيتنقل لفولدر «$trashName»."
Write-Host '  الملفات اللي مش من Claude مش هلمسها.'
Write-Host ''
Read-Host '  اضغط Enter عشان أبدأ' | Out-Null

$sha = [Security.Cryptography.SHA256]::Create()
function HashOf([string]$p) {
    $fs = [IO.File]::OpenRead((LP $p))
    try { return ([BitConverter]::ToString($sha.ComputeHash($fs)) -replace '-', '').ToLower() } finally { $fs.Dispose() }
}

Write-Host '  بفحص الملفات...'
$byHash = @{}
$hashOfPath = @{}
$n = 0
foreach ($f in [IO.Directory]::EnumerateFiles((LP $root), '*', [IO.SearchOption]::AllDirectories)) {
    $p = $f.Substring(4)
    if ($p -eq $self) { continue }
    if (-not $sizes.Contains((New-Object IO.FileInfo $f).Length)) { continue }
    $h = HashOf $p
    if (-not ($want.ContainsKey($h) -or $obsolete.ContainsKey($h))) { continue }
    if (-not $byHash.ContainsKey($h)) { $byHash[$h] = New-Object System.Collections.Generic.List[string] }
    $byHash[$h].Add($p)
    $hashOfPath[$p] = $h
    $n++
    if ($n % 100 -eq 0) { Write-Host "  $n ملف..." }
}

$touched = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
function TrashPath([string]$p) {
    $r = Rel $p
    $t = [IO.Path]::Combine($trash, $r)
    $i = 2
    while ([IO.File]::Exists((LP $t))) { $t = [IO.Path]::Combine($trash, "$i", $r); $i++ }
    return $t
}
function Relocate([string]$src, [string]$dst) {
    [void][IO.Directory]::CreateDirectory((LP (Parent $dst)))
    [IO.File]::Move((LP $src), (LP $dst))
    [void]$touched.Add((Parent $src))
    $h = $hashOfPath[$src]
    if ($h) {
        $l = $byHash[$h]
        for ($i = 0; $i -lt $l.Count; $i++) { if ([string]::Equals($l[$i], $src, [StringComparison]::OrdinalIgnoreCase)) { $l[$i] = $dst } }
        $hashOfPath.Remove($src)
        $hashOfPath[$dst] = $h
    }
}

$used = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
$ok = 0; $moved = 0; $written = 0; $extras = 0
$missing = New-Object System.Collections.Generic.List[string]
foreach ($m in $manifest) {
    $dst = [IO.Path]::Combine($root, $m.Rel)
    $list = $byHash[$m.Hash]
    if ($list -and ($list -contains $dst)) { [void]$used.Add($dst); $ok++; continue }
    if ([IO.File]::Exists((LP $dst))) { Relocate $dst (TrashPath $dst) }
    $src = $null
    if ($list) { foreach ($c in $list) { if (-not $used.Contains($c) -and -not $c.StartsWith($trash + '\', [StringComparison]::OrdinalIgnoreCase)) { $src = $c; break } } }
    if (-not $src -and $list) { $src = $list[0] }
    if ($src) { Relocate $src $dst; [void]$used.Add($dst); $moved++ }
    elseif ($embed.ContainsKey($m.Rel)) {
        [void][IO.Directory]::CreateDirectory((LP (Parent $dst)))
        [IO.File]::WriteAllBytes((LP $dst), [Convert]::FromBase64String($embed[$m.Rel]))
        [void]$used.Add($dst); $written++
    }
    else { $missing.Add($m.Rel) }
}

foreach ($h in @($byHash.Keys)) {
    foreach ($p in @($byHash[$h])) {
        if ($used.Contains($p)) { continue }
        if ($p.StartsWith($trash + '\', [StringComparison]::OrdinalIgnoreCase)) { continue }
        Relocate $p (TrashPath $p); $extras++
    }
}

# Remove only the folders this run emptied, walking up toward the root.
foreach ($d in ($touched | Sort-Object { $_.Length } -Descending)) {
    $x = $d
    while ($x -and $x.Length -gt $root.Length -and [IO.Directory]::Exists((LP $x)) -and [IO.Directory]::GetFileSystemEntries((LP $x)).Length -eq 0) {
        [IO.Directory]::Delete((LP $x)); $x = Parent $x
    }
}

$rep = New-Object System.Collections.Generic.List[string]
$rep.Add("الترتيب خلص في: $root")
$rep.Add('')
$rep.Add("كانت في مكانها: $ok")
$rep.Add("اتنقلت لمكانها: $moved")
$rep.Add("اتكتبت من الأمر نفسه (الفهارس وصفحات HTML): $written")
$rep.Add("مكرر أو نسخة قديمة، اتنقل لفولدر «$trashName»: $extras")
$rep.Add("ناقصة: $($missing.Count)")
if ($missing.Count) {
    $rep.Add('')
    $rep.Add('الملفات الناقصة (فك ملفات الـ zip في الفولدر ده وشغل الأمر تاني):')
    foreach ($r in $missing) { $rep.Add("  $r") }
}
$repPath = [IO.Path]::Combine($root, 'تقرير الترتيب.txt')
[IO.File]::WriteAllLines($repPath, $rep, (New-Object Text.UTF8Encoding $true))
Write-Host ''
$rep | ForEach-Object { Write-Host "  $_" }
Start-Process notepad.exe -ArgumentList "`"$repPath`""
