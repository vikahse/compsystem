param(
  [Parameter()]
  [int]$MaxBlockSize,
  [string]$Address
)

if (-not $MaxBlockSize) {
  Write-Host "The argument MaxBlockSize was not specified. The test value of this argument is 1500"
  $MaxBlockSize = 1500
} else {
  if ($MaxBlockSize -le 0) {
    Write-Host "The argument MaxBlockSize is negative" -ForegroundColor Red
    exit
  }
}

if (-not $Address) {
  Write-Host "The argument Address was not specified. The test value of this argument is www.abs.ru"
  $Address = "www.abs.ru"
}

$MinBlockSize = 0

Write-Host "Address: $Address, MaxBlockSize: $MaxBlockSize"

try {
  $PingTest = ping $Address -c 1
} catch {
  Write-Host "Failed to connect to the destination address. Chech that the entered address is correct" -ForegroundColor Red
  exit
}

if (-not $PingTest) {
  Write-Host "ICMP packets are blocked to the destination address" -ForegroundColor Red
  exit
}

$LastMinBlockSize=$MinBlockSize
$LastMaxBlockSize=$MaxBlockSize
$Flag=$false
[int]$BlockSize = $MaxBlockSize / 2

while(-not $Flag){
        $Response = ping $Address -n 1 -f -l $BlockSize
        if ($Response -like "*fragmented*") {
            Write-Host "MTU = $BlockSize is too large" -ForegroundColor Red
            $LastMaxBlockSize = $BlockSize
            if (($LastMaxBlockSize - $LastMinBlockSize) -le 5) {
                $BlockSize = $BlockSize - 1
            } else {
                $BlockSize = $LastMinBlockSize + (($LastMaxBlockSize - $LastMinBlockSize) / 2)
            }
        } else {
            if ($LastMinBlockSize -eq $BlockSize) {
                $Flag = $true
            } else {
                Write-Host "$BlockSize can be increased" -ForegroundColor Green
                $LastMinBlockSize = $BlockSize
                $BlockSize = $BlockSize + (($LastMaxBlockSize - $LastMinBlockSize) / 2)
            }
        }
}

Write-Host "Final MTU: $BlockSize" -ForegroundColor Blue
