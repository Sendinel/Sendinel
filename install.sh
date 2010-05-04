#!/bin/bash

targetDir="/opt/sendinel"
configureAsterisk=true
configureLighttpd=true
installInitScripts=true
user='sendinel'
group='sendinel'
requiredPackages='asterisk festival lighttpd sudo build-essential python-setuptools wget' # wget only for django install
requiredPythonPackages='python-daemon lockfile'
pythonVersion='python2.6' # name of the binary that should exist in PATH
tempDir="/tmp"

# targetDir="./installTest"

sourceDir=$(readlink -f "$0")
sourceDir=$(dirname "$sourceDir")
targetParentDir="$(dirname $targetDir)"
# timestamp in form 2010-05-03-16-27-15
timestamp=$(date +%F-%k-%M-%S)


error() {
    echo -e "ERROR: $errorMessage"
    echo "Sendinel installation aborted."
    exit 1
}

warning() {
    # todo ask user wether he wants to continue
    echo -e "WARNING: $errorMessage"
    read -p "Do you want to continue anyway - this may not work? (y/n)"
    if [ "$REPLY" != "y" ]; then
        echo "Sendinel installation aborted."
        exit 1
    fi
    echo "Sendinel installation continued despite warning."
}

message_done() {
    echo -e "\tdone"
}

backup_file() {
    file="$1"
    backupFile="$file.sendinel-backup-$timestamp"
    echo "Backing up file $file to $backupFile"
    errorMessage='File backup failed.'
    cp -a "$file" "$backupFile" || warning
}

check_file_exists_and_backup() {
    # test wether file already exists - if yes do a backup
    file="$1"
    if [ -e "$file" ]; then
        errorMessage="Configuration file already exists: '$file'. A backup file will be created if you choose to proceed."
        warning
        backup_file "$file"
        return 1
    fi
    return 0
}

remove_or_warning() {
    file="$0"
    errorMessage="The following file could not be removed: '$file'"
    rm "$file" || warning
}

symlink_or_warning() {
    source="$0"
    target="$1"
    check_file_exists_and_backup "$source"
    remove_or_warning "$source"

    errorMessage="Failed to create symlink from '$source' to '$target'"
    ln -sfv "$target" "$source" || warning
}

replace_in_file() {
    file="$1"
    searchFor="$2"
    replaceWith="$3"
    sed -i "s/$searchFor/$replaceWith/g" "$file"
}

# test wether target dir already exists
if [ -e "$targetDir" ]; then
    errorMessage="Installation target directory already exists: '$targetDir'"
    errorMessage="$errorMessage\n\tWe don't want to possibly overwrite existing files."
    warning
fi


# test wether we have write permissions to parent of target dir
if  test ! -w "$targetParentDir"; then
    errorMessage="Your user doesn't have write permissions on $targetParentDir. "
    errorMessage="$errorMessage\n\tRun $0 as root: sudo $0"
    error
fi


# TODO check which python versions work
# eventually write scripts to start sendinel using python2.6
# $pythonVersion
if type -P "$pythonVersion" > /dev/null; then
    pythonPath=$(type -P "$pythonVersion")
    echo "Python found: $pythonPath"
else
    errorMessage="The python executable '$pythonVersion' was not found in PATH."
    warning
fi


# package installs
echo "Installing required packages: $requiredPackages..."
errorMessage='Installing required packages failed. You may manually install them.'
apt-get install $requiredPackages || warning
message_done

# python package installs
echo "Installing required python packages: $requiredPythonPackages"
errorMessage='Installing required python packages failed. You may manually install them.'
easy_install $requiredPythonPackages || warning
message_done

# django 1.2 beta until final release is available
url="http://www.djangoproject.com/download/1.2-beta-1/tarball/"
tarball="$tempDir/django.tar.gz"
wget -O "$tarball" "$url"
tar xvzf "$tarball" -C "$tempDir"

djangoDir="$tempDir/Django-1.2-beta-1"
errorMessage="Could not cd to directory '$djangoDir'. You may manually install django > 1.2 beta 1."
cd "$djangoDir" || warning

errorMessage="Django installation failed. Look for errors above."
python setup.py install || warning

# sendinel user and group
echo "Creating user '$user' and group '$group'..."

errorMessage="Group '$group' could not be created. Look for errors above."
groupadd "$group" || warning

errorMessage="User '$user' could not be created. Look for errors above."
useradd -N -G "$group,asterisk" $user || warning
message_done


echo "Copying files to $targetDir... "
mkdir -p "$targetDir/sendinel"
if [ "$?" -ne "0" ]; then
    errorMessage="Creating directory '$targetDir/sendinel' failed. Look for errors above."
    error
fi


cp -a "$sourceDir/sendinel" "$targetDir/sendinel"
if [ "$?" -ne "0" ]; then
    errorMessage="Copying files failed. Look for errors above."
    error
fi
message_done



# sudo
# TODO check wether sudoers already contains sendinel line
# TODO fix python path
echo "Configuring permissions for phone authentication in /etc/sudoers..."
sudoersFile="/etc/sudoers"
backup_file "$sudoersFile"
sudoLine="asterisk      ALL = ($user)NOPASSWD: /usr/bin/python '$targetDir/sendinel/asterisk/log_call.py'"

errorMessage='Writing the sudoers file failed. You can try to add the following line manually using visudo:'
errorMessage="$errorMessage\n$sudoLine"
echo "\n\n#This line was added by the sendinel install script." >> $sudoersFile
echo "$sudoLine" >> $sudoersFile
message_done


# asterisk config
asteriskDir="/etc/asterisk"
echo "Configuring Asterisk telephony server..."
asteriskConfigsDir="$targetDir/configs/asterisk"

# replace extensions.conf
extensionsTarget="$asteriskDir/extensions.conf"
backup_file "$extensionsTarget"
errorMessage="Failed to replace asterisk configuration file '$extensionsTarget'"
cp -a "$asteriskConfigsDir/extensions.conf" "$extensionsTarget" || warning

# copy datacard.conf
dataCardTarget="$asteriskDir/datacard.conf"
if [ -e "$dataCardTarget" ]; then
    backup_file "$dataCardTarget"
fi
errorMessage="Failed to install asterisk configuration file '$dataCardTarget'"
cp -a "$asteriskConfigsDir" "$dataCardTarget" || warning



# call_log agi script symlink
agiFileName="call_log.agi"
agiLinkSource="/usr/share/asterisk/agi-bin"

symlink_or_warning "$agiLinkSource/$agiFileName" "$asteriskConfigsDir/$agiFileName"

backup_file "$file"
replace_in_file "$agiLinkTarget" '%targetDir%' "$targetDir" 
replace_in_file "$agiLinkTarget" '%user%' "$user"
message_done


# asterisk permissions
# TODO warning about security issues - /var/spool/asterisk/outgoing 
# /var/spool/asterisk/outgoing 770


# download and compile datacard

# restart asterisk



# lighttpd config
# 







