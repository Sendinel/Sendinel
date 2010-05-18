#!/bin/bash

#localSettings="./local_settings_test.py"
if [ ! -n "$1" ]; then
    echo "Usage: $0 <settings file>"
    echo " settings file: e.g. sendinel/local_settings.py"
    exit 1
fi

localSettings="$1"


ask_for_and_write() {
    if ask_for "$@"; then
        echo "$_settingName = $_settingValue" >> $localSettings
    fi
}

ask_for() {
    _settingName="$1"
    _settingType="$2"
    _text="$3"

    _resultFound=false
    _settingValue="undefined"
    
    while ! $_resultFound; do
        read -p "$_text"
    
        case "$_settingType" in 
            boolean)
                if echo "$REPLY" | grep -qE "^(True|False)$"; then
                    _resultFound=true
                    _settingValue=$REPLY
                fi
            ;;
            string)
                if [ -n "$REPLY" ]; then
                    _resultFound=true
                    _settingValue="'$REPLY'"
                fi
            ;;
            *)
                echo "Error: Unkown settingType: '$_settingType' for '$_settingName'"
                exit 1
        esac
    done
}





ask_for_and_write "AUTHENTICATION_ENABLED" boolean "Do you want the patient to authenticate against the system via ringing a mobile phone number (True/False)? "


if [ $_settingValue == "True" ]; then
    ask_for_and_write "AUTH_NUMBER" string "Please enter the phone number of the SIM card in the 3G stick: "
fi

ask_for_and_write "DEFAULT_HOSPITAL_NAME" string "Please enter the clinic's name: "

ask_for_and_write "COUNTRY_CODE_PHONE" string "Please enter your country's calling code prefixed with two zeros (e.g. 0049 for Germany): "

ask_for "_BLUETOOTH_ENABLED" boolean "Do you want to enable the bluetooth functionality - this requires Bluetooth hardware on client computers (True/False)? "
bluetoothEnabled="$_settingValue"




python "$(dirname $0)/initial_settings_helper.py" "$bluetoothEnabled"

