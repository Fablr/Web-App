#!/bin/bash
xcode-select --install
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install pyenv
brew install pyenv-virtualenv
brew install unixodbc
brew install freetds --with-unixodbc
brew install postgresql
brew install openssl
pyenv install 3.4.3
pyenv rehash
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
exec $SHELL
pyenv global 3.4.3
pyenv virtualenv VFABLER_WEB
env CRYPTOGRAPHY_OSX_NO_LINK_FLAGS=1 LDFLAGS="$(brew --prefix openssl)/lib/libssl.a $(brew --prefix openssl)/lib/libcrypto.a" CFLAGS="-I$(brew --prefix openssl)/include" pip install -r requirements.txt
