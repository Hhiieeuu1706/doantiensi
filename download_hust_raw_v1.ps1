param(
    [string]$Output = "external_data\raw\HUST\our_data.zip"
)

$url = "https://data.mendeley.com/public-files/datasets/nsc7hnsg4s/files/5ca0ac3e-d598-4d07-8dcb-879aa047e98b/file_downloaded"
$target = [IO.Path]::GetFullPath($Output)
New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($target)) -Force | Out-Null
Write-Host "Downloading HUST dataset from DOI 10.17632/nsc7hnsg4s.2"
Invoke-WebRequest -Uri $url -OutFile $target -UseBasicParsing
$hash = Get-FileHash -LiteralPath $target -Algorithm SHA256
$bytes = (Get-Item -LiteralPath $target).Length
if ($bytes -lt 500MB) { throw "Downloaded file is unexpectedly small ($bytes bytes); inspect the official source response." }
$record = [PSCustomObject]@{
    dataset_doi = "10.17632/nsc7hnsg4s.2"
    source_url = $url
    local_path = $target
    bytes = $bytes
    sha256 = $hash.Hash
}
$record | Export-Csv -Path (Join-Path ([IO.Path]::GetDirectoryName($target)) 'HUST_ARCHIVE_DOWNLOAD_MANIFEST.csv') -NoTypeInformation -Encoding UTF8
Write-Host "Saved $target"
Write-Host "SHA256: $($hash.Hash)"
