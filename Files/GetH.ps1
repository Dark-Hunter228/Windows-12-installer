# Удаляем приложение Microsoft.Windows.GetHelp с помощью AppxPackage

# Получаем список пакетов GetHelp
$packageName = "*Microsoft.Windows.GetHelp*"
$packages = Get-AppxPackage | Where-Object { $_.Name -like $packageName }

if ($packages.Count -gt 0) {
    foreach ($pkg in $packages) {
        try {
            # Пытаемся удалить каждый найденный пакет
            Remove-AppxPackage -Package $pkg.PackageFullName -ErrorAction Stop
            Write-Host "Пакет $($pkg.Name) успешно удалён." -ForegroundColor Green
        }
        catch {
            Write-Warning "Ошибка при удалении пакета $($pkg.Name): $_"
        }
    }
} else {
    Write-Host "Приложение GetHelp не найдено." -ForegroundColor Yellow
}