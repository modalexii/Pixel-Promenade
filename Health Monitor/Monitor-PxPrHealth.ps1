<#
.SYNOPSIS
    Collects and mails health information for the Pixel Promenade controller
.SYNTAX
    .\Monitor-PxPrHealth.ps1
.DESCRIPTION
    Maybe some day
.PARAMETERS
    None
#>

$ErrorActionPreference = "Stop"

Function Send-Report {
    "$(get-date -format '%H:%m:%s'): Send-Report"
    $Server = "smtp.gmail.com"
    $Port = "587"
    $User = "pxpr@unsecu.re"
    $Pass = "XXXXXXXXXXXXXX"
    $From = "Pixel Promenade Control pxpr@unsecu.re"
    $To = "3016132783@messaging.sprintpcs.com" 
    $Message = New-Object System.Net.Mail.MailMessage($From, $To)
    $Message.Subject = "Health Report $(Get-Date -Format '%H:%m:%s')"
    $Message.IsBodyHtml = $False
    $Message.Body = "
SYS CPU: $(Print-CPULoad) MBytes Free: $(Print-MemAvail)
MADRIX: $(Print-MADRIXInfo)
Art-Net UDP $(Print-UDPInfo)
Controller ARP/Ping:
$(Print-ControllerLANPresence)
Ping Twitter: $(Get-TwitterConnection)
Ticker src last-modified: $(Get-TickerLastModified)
"
    #$SMTPClient = New-Object System.Net.Mail.SmtpClient($Server , $Port)
    #$SMTPClient.EnableSsl = $true
    #$SMTPClient.Credentials = New-Object System.Net.NetworkCredential($User , $Pass);
    #$SMTPClient.Send($Message)
    echo $Message.Body 
    
}   

Function Print-CPULoad {
    "$(get-date -format '%H:%m:%s'): Print-CPULoad"
    $PTimeCounter = Get-Counter '\Processor(_Total)\% Processor Time'
    $Sample = ($PTimeCounter.CounterSamples)[0].CookedValue
    $Load = [math]::Round($Sample,2)
    If($Load -gt 75) {
        $StateChar = $WarnStateChar
    } Else {
        $StateChar = $GoodStateChar
    }
    "$StateChar $Load%"
}

Function Print-MemAvail {
    "$(get-date -format '%H:%m:%s'): Print-MemAvail"
    $MBytesCounter = Get-Counter '\Memory\Available MBytes'
    $MBytes = $MBytesCounter.CounterSamples[0].CookedValue
    If($MBytes -lt 1024*3) {
        $StateChar = $WarnStateChar
    } Else {
        $StateChar = $GoodStateChar
    }
    "$StateChar $MBytes"
}

Function Print-MADRIXInfo {
    "$(get-date -format '%H:%m:%s'): Print-MADRIXInfo"
    Try {
        $Proc = Get-Process MADRIX -ErrorAction Stop
        $StartTime = ($Proc.StartTime -Split " ")[1]
        $StartedText = "Started $StartTime"
        $Responding = $Proc.Responding
        If($Responding) {
            $StateChar = $GoodStateChar
            $RespondingText = ""
        } Else {
            $StateChar = $BadStateChar
            $RespondingText = ", NOT RESPONDING"
        }
    } Catch [System.Management.Automation.ActionPreferenceStopException] {
        $StateChar = $BadStateChar
            $RespondingText = " NOT FOUND"
    }
    "$StateChar $StartedText $RespondingText"
}

Function Print-UDPInfo {
    "$(get-date -format '%H:%m:%s'): Print-UDPInfo"
    $UDPStats = (netsh interface ipv4 show udpstats)
    $UDPInDatagrams = (($UDPStats | Select-String "In Datagrams") -Split " ")[-1]
    $UDPOutDatagrams = (($UDPStats | Select-String "Out Datagrams") -Split " ")[-1]
    If($UDPInDatagrams -eq 0 -or $UDPOutDatagrams -eq 0) {
        $StateChar = ""
    } Else {
        $StateChar = $WarnStateChar
    }
    "$StateChar In: $UDPInDatagrams Out: $UDPOutDatagrams"
}

Function Print-ControllerLANPresence {
    "$(get-date -format '%H:%m:%s'): Print-ControllerLANPresence"
    # Create array of bad chars, to overwrite with good chars as tests are passed
    # Tuple is (found in arp table, can be pinged)
    $B = @($BadStateChar, $BadStateChar)
    $Controllers = @{
        101=$B; 102=$B; 103=$B; 104=$B; 105=$B; 106=$B; 107=$B;
        108=$B; 109=$B; 110=$B; 111=$B; 112=$B; 113=$B
    }
    $Arp = (arp -a) # get ARP table *before* pinging
    $Controllers.keys | ForEach {
        If([bool](Test-Connection -Count 2 -Quiet 10.0.1.$_)) {
            $Controllers[$_][1] = $GoodStateChar
        }
        If([bool]($Arp -Match "10.0.1.$_")) {
            $Controllers[$_][0] = $GoodStateChar
        }
    }
    
    $C = $Controllers
    A: $($C[101][0])/$($C[101][1]) B: $($C[102][0])/$($C[102][1]) C: $($C[103][0])/$($C[103][1])
    D: $($C[104][0])/$($C[104][1]) E: $($C[105][0])/$($C[105][1]) F: $($C[106][0])/$($C[106][1])
    G: $($C[107][0])/$($C[107][1]) H: $($C[108][0])/$($C[108][1]) I: $($C[109][0])/$($C[109][1])
    J: $($C[110][0])/$($C[110][1]) K: $($C[111][0])/$($C[111][1])
}

Function Get-TwitterConnection {
    "$(get-date -format '%H:%mm:%s'): Get-TwitterConnection"
    If(Test-Connection -Quiet twitter.com) {
        "$GoodStateChar"
    } Else {
        "$BadStateChar"
    }
}

Function Get-TickerLastModified {
    "$(get-date -format '%H:%m:%s'): Get-TickerLastModified"
    $TickerFile = Get-Item "C:\Users\j19311\Desktop\Monitor-PxPrHealth.ps1"
    ($TickerFile.LastWriteTime -Split " ")[-1]
}

Function Main {
    "$(get-date -format '%H:%m:%s'): Main"
    $GoodStateChar = "✅" # 'WHITE HEAVY CHECK MARK' (U+2705)
    $WarnStateChar = "❕" # 'WHITE EXCLAMATION MARK ORNAMENT' (U+2755)
    $BadStateChar = "❎" # 'NEGATIVE SQUARED CROSS MARK' (U+274E)
    Send-Report
}

Main

